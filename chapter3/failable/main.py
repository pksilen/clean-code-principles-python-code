from get_config import get_config

config_file_path_names = ['config1.json', 'config2.json']
maybeConfig = get_config(config_file_path_names)
print(maybeConfig.or_raise(RuntimeError))
# Prints {'foo': 1, 'bar': 2, 'xyz': 3}
