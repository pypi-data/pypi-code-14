import json

class ConsolePrinter:
    def __init__(self, quiet = False, format_type = 'pretty', verbose=False):
        self.quiet = quiet
        self.format_type = format_type
        self.verbose = verbose
        self.format_map = {
            'pretty': ConsolePrinter.get_pretty,
            'none': ConsolePrinter.get_none
        }
        
    def out(self, result):
        recipe = result.recipe
        response = result.response
        
        quiet = self.quiet
        format_type = self.format_type
        
        if 'output' in recipe:
            if 'quiet' in recipe['output']:
                quiet = recipe['output']['quiet']
            
            if 'format' in recipe['output']:
                format_type = recipe['output']['format']
            
        if quiet: return
        
        if self.verbose:
            recipe_id = recipe['id'] if 'id' in recipe else 'Unknown recipe <id>'
            print('{}:'.format(recipe_id))
        
        if response:
            print self.format_map[format_type](response)
        else:
            print response

    @staticmethod
    def get_none(response):
        return response.text
    
    @staticmethod        
    def get_pretty(response):
        try:
            json_data = response.json()
            return json.dumps(json_data, indent=2)
        except ValueError:
            return response.text