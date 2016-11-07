from .webserver import run_server

class ActionForm(object):
    form_class = None

    @classmethod
    def run_webserver(cls, **args):
        run_server(cls, **args)
    
    @classmethod
    def get_form_class(cls):
        return cls.form_class

    def __init__(self, form=None, **kargs):
        if form is None:
            form = self.get_form_class()(**kargs)
        self.form = self.validate(form)

    def validate(self, form):
        if not form.validate():
            raise ValidationError(form.errors)
        return form 
        
    def run(self):
        return self._run(**self.form.data)

    def render_result(self, result):
        return str(result)
