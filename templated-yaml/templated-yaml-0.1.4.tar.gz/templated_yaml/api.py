import os, yaml
from . import resolver


def render_from_path(path, context={}, globals=[]):
    """
    Renders a templated yaml document from file path.

    :param path: A path to the yaml file to process.
    :param context: A context to overlay on the yaml file.  This will override any yaml values.
    :param globals: A dictionary of globally-accessible objects within the rendered template.
    :return: A dict with the final overlayed configuration.
    """
    abs_source = os.path.abspath(os.path.expanduser(path))
    yaml_resolver = resolver.TYamlResolver.new_from_path(abs_source)

    return yaml_resolver.resolve(context, globals)


def render_from_string(content, context={}, globals=[]):
    """
    Renders a templated yaml document from a string.

    :param content: The yaml string to evaluate.
    :param context: A context to overlay on the yaml file.  This will override any yaml values.
    :param globals: A dictionary of globally-accessible objects within the rendered template.
    :return: A dict with the final overlayed configuration.
    """
    yaml_resolver = resolver.TYamlResolver.new_from_string(content)

    return yaml_resolver.resolve(context, globals)