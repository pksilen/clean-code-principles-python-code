# This is free and unencumbered software released into the public domain
# by its author, Ben Hodgson <ben@benhodgson.com>.

# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.

# In jurisdictions that recognise copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

# For more information, please refer to <http://unlicense.org/>

from google.protobuf.descriptor import FieldDescriptor

EXTENSION_CONTAINER = '___X'


TYPE_CALLABLE_MAP = {
    FieldDescriptor.TYPE_DOUBLE: float,
    FieldDescriptor.TYPE_FLOAT: float,
    FieldDescriptor.TYPE_INT32: int,
    FieldDescriptor.TYPE_INT64: int,
    FieldDescriptor.TYPE_UINT32: int,
    FieldDescriptor.TYPE_UINT64: int,
    FieldDescriptor.TYPE_SINT32: int,
    FieldDescriptor.TYPE_SINT64: int,
    FieldDescriptor.TYPE_FIXED32: int,
    FieldDescriptor.TYPE_FIXED64: int,
    FieldDescriptor.TYPE_SFIXED32: int,
    FieldDescriptor.TYPE_SFIXED64: int,
    FieldDescriptor.TYPE_BOOL: bool,
    FieldDescriptor.TYPE_STRING: str,
    FieldDescriptor.TYPE_BYTES: lambda b: b.encode('base64'),
    FieldDescriptor.TYPE_ENUM: int,
}


def repeated(type_callable):
    return lambda value_list: [
        type_callable(value) for value in value_list
    ]


def enum_label_name(field, value):
    return field.enum_type.values_by_number[int(value)].name


def proto_to_dict(
    pb, type_callable_map=TYPE_CALLABLE_MAP, use_enum_labels=False
):
    result_dict = {}
    extensions = {}
    for field, value in pb.ListFields():
        type_callable = _get_field_value_adaptor(
            pb, field, type_callable_map, use_enum_labels
        )
        if field.label == FieldDescriptor.LABEL_REPEATED:
            type_callable = repeated(type_callable)

        if field.is_extension:
            extensions[str(field.number)] = type_callable(value)
            continue

        result_dict[field.name] = type_callable(value)

    if extensions:
        result_dict[EXTENSION_CONTAINER] = extensions
    return result_dict


def _get_field_value_adaptor(
    pb, field, type_callable_map=TYPE_CALLABLE_MAP, use_enum_labels=False
):
    if field.type == FieldDescriptor.TYPE_MESSAGE:
        # recursively encode protobuf sub-message
        return lambda pb: proto_to_dict(
            pb,
            type_callable_map=type_callable_map,
            use_enum_labels=use_enum_labels,
        )

    if use_enum_labels and field.type == FieldDescriptor.TYPE_ENUM:
        return lambda value: enum_label_name(field, value)

    if field.type in type_callable_map:
        return type_callable_map[field.type]

    raise TypeError(
        'Field %s.%s has unrecognised type id %d'
        % (pb.__class__.__name__, field.name, field.type)
    )


def get_bytes(value):
    return value.decode('base64')


REVERSE_TYPE_CALLABLE_MAP = {
    FieldDescriptor.TYPE_BYTES: get_bytes,
}


def _get_field_mapping(pb, dict_value, strict):
    field_mapping = []
    for key, value in dict_value.items():
        if key == EXTENSION_CONTAINER:
            continue
        if key not in pb.DESCRIPTOR.fields_by_name:
            if strict:
                raise KeyError(
                    '%s does not have a field called %s' % (pb, key)
                )
            continue
        field_mapping.append(
            (
                pb.DESCRIPTOR.fields_by_name[key],
                value,
                getattr(pb, key, None),
            )
        )

    for ext_num, ext_val in dict_value.get(
        EXTENSION_CONTAINER, {}
    ).items():
        try:
            ext_num = int(ext_num)
        except ValueError:
            raise ValueError('Extension keys must be integers.')
        if ext_num not in pb._extensions_by_number:
            if strict:
                raise KeyError(
                    '%s does not have a extension with number %s. Perhaps you forgot to import it?'
                    % (pb, key)
                )
            continue
        ext_field = pb._extensions_by_number[ext_num]
        pb_val = None
        pb_val = pb.Extensions[ext_field]
        field_mapping.append((ext_field, ext_val, pb_val))

    return field_mapping


def _string_to_enum(field, input_value):
    enum_dict = field.enum_type.values_by_name
    try:
        input_value = enum_dict[input_value].number
    except KeyError:
        raise KeyError(
            '`%s` is not a valid value for field `%s`'
            % (input_value, field.name)
        )
    return input_value
