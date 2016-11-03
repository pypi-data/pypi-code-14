class Service(object):
    required_parameters = []
    name = 'Service Name'

    def _validate_parameters(self, parameters):
        for p in self.required_parameters:
            if p not in parameters:
                raise Exception(
                    'expected parameter `{0}` to be present'.format(p))

    def run(self, parameters):
        self._validate_parameters(parameters)
        return self._execute(parameters)

    def _execute(self, parameter):
        pass


class App(Service):
    required_parameters = []
    name = 'Application Name'

    def run(self, parameters):
        self._validate_parameters(parameters)
        return self._render(self._execute(parameters))

    def _render(self, layout):
        rendered = []
        for row in layout:
            rendered.append([x.render() for x in row])

        return {
            'name': self.name,
            'layout': rendered
        }
