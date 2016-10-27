import jmespath, json

from . import PostExecutor

class StorePostExecutor(PostExecutor):

    def process(self, result):
        recipe = result.recipe
        response = result.response

        if 'save' in recipe:
            key = recipe['save']['dest']

            try:
                data = response.json()

                if 'path' in recipe['save']:
                    path = recipe['save']['path']
                    data = jmespath.search(path, data)

                result.data['vars'].update({
                    key: data
                })
            except ValueError:
                pass
