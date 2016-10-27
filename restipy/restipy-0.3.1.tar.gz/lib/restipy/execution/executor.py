import jmespath

from restipy.renderer import RecipeRenderer
from request_executor import RecipeRequestExecutor

from pkg_resources import iter_entry_points
from collections import namedtuple

ExecutionResult = namedtuple('ExecutionResult', ['recipe', 'response', 'data'])

class CookbookExecutor:
    def __init__(self, filter_func = None):
        self.filter_func = filter_func

        self.pre_processors = {}
        for entry_point in iter_entry_points(group='restipy.execution.pre', name=None):
            Processor = entry_point.load()
            self.pre_processors[entry_point.name] = Processor()

        self.post_processors = {}
        for entry_point in iter_entry_points(group='restipy.execution.post', name=None):
            Processor = entry_point.load()
            self.post_processors[entry_point.name] = Processor()

    def execute(self, cookbook_file, input_data):
        recipe_renderer = RecipeRenderer(cookbook_file)
        request_executor = RecipeRequestExecutor()

        index = 0
        while True:
            recipes = self.render_recipes(recipe_renderer, input_data)
            if self.filter_func:
                recipes = filter(filter_func, recipes)

            if index >= len(recipes):
                break

            recipe = recipes[index]

            for (key, processor) in self.pre_processors.iteritems():
                processor.process(recipe=recipe, data=input_data)

            response = request_executor.execute(recipe)
            result = ExecutionResult(
                recipe=recipe,
                response=response,
                data=input_data
            )

            for (key, processor) in self.post_processors.iteritems():
                processor.process(result)

            yield result
            index += 1

    def render_recipes(self, recipe_renderer, input_data):
        cookbook = recipe_renderer.render(input_data)
        recipes = cookbook['recipes']
        return recipes
