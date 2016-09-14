import pkg_resources


def get_path(filename: str)-> str :
    return pkg_resources.resource_filename(__name__, filename)
