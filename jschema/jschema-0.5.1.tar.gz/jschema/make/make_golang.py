# -*- coding: utf-8 -*-
import os
from jschema.errors import JrsMakeError
from jschema.make._options import Options
from jschema.make._dump_methods import dump_methods
from jschema.make._jinja2_env import jinja2_env


def make_golang(schema, options):
    opts = Options(options)
    template = jinja2_env.get_template("method_meta_golang.j2")

    for key, sch in schema.schemas.iteritems():
        if sch["type"] != "method":
            continue

        key_split = key.split(".")
        if len(key_split) == 1:
            ns = self._opts.ns
            name = key_split[0]
        elif len(key_split) == 2:
            ns = key_split[0]
            name = key_split[1]
        else:
            raise JrsMakeError("Expect zero or one dot in schema id")

        sch_dir = os.path.join(opts.dst_dir, schema.schemas_dirs[key])
        if not os.path.exists(sch_dir):
            os.makedirs(sch_dir)

        sch_path = "{}/{}_meta.go".format(sch_dir, name)
        with open(sch_path, "w") as fstream:
            fstream.write(template.render({
                "ns": ns,
                "name": name,
                "schema": sch
            }))
        print(" - Created: {}".format(sch_path))
