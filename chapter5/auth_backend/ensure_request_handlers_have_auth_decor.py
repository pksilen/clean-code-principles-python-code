import os


class AuthDecorNotSpecifiedException(Exception):
    def __init__(self, file_name: str, line_number: int):
        self.__file_name = file_name
        self.__line_number = line_number

    def __str__(self):
        return f'Auth decorator not specified in file {self.__file_name} line {self.__line_number}'


def ensure_request_handlers_have_auth_decor():
    for path, _, file_names in os.walk('./'):
        for file_name in file_names:
            if file_name.endswith('.py'):
                file_path_name = os.path.join(path, file_name)
                with open(file_path_name) as file:
                    lines = file.readlines()
                prev_line = ''
                for line_index, line in enumerate(lines):
                    line = line.strip()
                    if any(
                        [
                            prev_line.startswith(decorator)
                            for decorator in [
                                '@app.get',
                                '@app.put',
                                '@app.patch',
                                '@app.post',
                                '@app.delete',
                            ]
                        ]
                    ):
                        if not line.startswith('@allow_'):
                            line_number = line_index + 1
                            raise AuthDecorNotSpecifiedException(
                                file_name, line_number
                            )
                    prev_line = line


if os.environ.get('ENV') == 'DEVELOPMENT':
    ensure_request_handlers_have_auth_decor()