from messenger_sdk.templates import Template


class FbResponse:
    def __init__(self, template=None):
        self._send = False
        self._templates = list()
        if template:
            self.add_template(template)

    def add_template(self, template: Template):
        self._throw_if_not_valid_type(template)
        self._templates.append(template)

    def _throw_if_not_valid_type(self, template):
        if not isinstance(template, Template):
            raise TypeError(
                'Invalid template type. Expected {expected}, given {given}.'.format(
                    expected=Template.__class__.__name__,
                    given=type(template).__name__))

    @property
    def templates(self):
        return self._templates

    @property
    def send(self):
        return self._send

    @send.setter
    def send(self, condition: bool):
        self._send = condition
