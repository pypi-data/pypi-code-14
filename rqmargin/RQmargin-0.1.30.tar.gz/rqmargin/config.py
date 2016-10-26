from json import load
import os


def get_config_one(path=None):
    if path is None:
        path =os.path.join(os.path.dirname(__file__),'config.json')
    with open(path, mode="rt", encoding="utf8") as f:
        config_dict = load(f)
    return config_dict

print(os.path.abspath(''))