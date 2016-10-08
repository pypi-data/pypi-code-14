import os


def get_yourtool_path(path="~/.yourtool"):
    return os.path.expanduser(path)
