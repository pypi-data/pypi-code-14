import yaml

from pkg_resources import iter_entry_points
from jinja2 import Environment, FileSystemLoader

class RecipeRenderer:
    def __init__(self, template_filename):
        jinja_env = Environment(loader=FileSystemLoader(''))

        plugins = {}
        for entry_point in iter_entry_points(group='restipy.renderer.plugins', name=None):
            plugins[entry_point.name] = entry_point.load()

        jinja_env.globals.update(plugins)

        self.template = jinja_env.get_template(template_filename)

    def render(self, params):
        recipe_str = self.template.render(params)
        return yaml.load(recipe_str)
