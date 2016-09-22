import os
from ..templates import Jinja2

_template_dir = os.path.abspath(os.path.join(__file__, '..', 'templates'))
template = Jinja2(_template_dir).file
