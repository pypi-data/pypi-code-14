import jinja2
from flask import request, Flask
import inspect
import os

DEFAULT_TEMPLATE = """
<html>
<body>
<h1>{{title}}</h1>
<form method="POST" action="/">
<dl>
{% for field in form %}
    <dt>{{ field.label }}</dt><dd>{{ field() }}</dd>
{% endfor %}
</dl>
    <input type="submit" value="Go">
</form>
{% if result %}
<hr/>
{{ result|safe }}
{% endif %}
</body>
</html>"""

def load_template(filename, action=None):
    path = "./" if action is None else os.path.dirname(inspect.getfile(action))
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(path or './'))
    #fn = os.path.join(path, filename); print(fn, os.path.exists(fn))
    return env.get_template(filename)

def run_server(action, template=None, **kargs):
    if template is None:
        template = getattr(action, 'default_template', DEFAULT_TEMPLATE)
    if isinstance(template, str):
        if template.endswith(".html"):
            template = load_template(template, action)
        else:
            template = jinja2.Template(template)
    
    app = Flask(action.__name__)
    @app.route('/', methods=['GET'])
    def get():
        form = action.get_form_class()()
        title = action.__name__
        return template.render(**locals())

    @app.route('/', methods=['POST'])
    def post():
        form = action.get_form_class()(request.form)
        a = action(form)
        result = a.run()
        if hasattr(a, 'render_result'):
            return a.render_result(result, template, locals())
        else:
            title = action.__name__
            return template.render(**locals())

    app.run(**kargs)
