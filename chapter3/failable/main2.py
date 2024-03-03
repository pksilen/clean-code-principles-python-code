from get_config import get_config

config_file_path_names = ['config1_error.json', 'config3.json']
maybeConfig = get_config(config_file_path_names)
print(maybeConfig.or_raise(RuntimeError))
# Raises a RuntimeError with the following message:
# config1.json: Expecting ',' delimiter: line 3 column 3 (char 16)
# config3.json: [Errno 2] No such file or directory: 'config3.json'
