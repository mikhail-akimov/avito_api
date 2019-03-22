# -*- coding: utf-8 -*-

"""Config for 'avito_api' application."""
import os
import yaml
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = os.path.join(BASE_DIR, 'config', 'api.yaml')


def get_config(path):
    """Get settings from yaml-file."""
    with open(path) as yf:
        conf = yaml.safe_load(yf)
    return conf


config = get_config(config_path)
