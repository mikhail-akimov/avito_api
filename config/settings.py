import os
import yaml
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = os.path.join(BASE_DIR, 'config', 'api.yaml')


def get_config(path):
    with open(path) as f:
        conf = yaml.load(f)
    return conf


config = get_config(config_path)
