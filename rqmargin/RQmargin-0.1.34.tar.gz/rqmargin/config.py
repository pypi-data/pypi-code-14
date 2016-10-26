from json import load
import os


def get_config_one(config_path=None):
    if config_path is None:
        config_path =os.path.join(os.path.dirname(__file__),'config.json')
    with open(config_path, mode="rt", encoding="utf8") as f:
        config_dict = load(f)
    return config_dict

