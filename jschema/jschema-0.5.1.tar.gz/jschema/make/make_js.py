# -*- coding: utf-8 -*-
from jschema.make._options import Options
from jschema.make._dump_methods import dump_methods
from jschema.make._jinja2_env import jinja2_env


def make_js(schema, options):
    opts = Options(options)
    template = jinja2_env.get_template("schema_js.j2")

    with open(opts.dst_path, "w") as fstream:
        fstream.write(template.render({"schemas": dump_methods(schema)}))
