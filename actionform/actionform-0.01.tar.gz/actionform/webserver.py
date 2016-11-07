from jinja2 import Template
from flask import request, Flask

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

def run_server(action, template=DEFAULT_TEMPLATE, **kargs):

    if isinstance(template, str):
        template = Template(template)
    
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
        result = a.render_result(a.run())
        title = action.__name__
        return template.render(**locals())

    app.run(**kargs)
