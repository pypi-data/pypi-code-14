import imp
import json
import os
import sys

import python_agent.init
from python_agent import admin, config


boot_directory = os.path.dirname(__file__)
root_directory = os.path.dirname(os.path.dirname(boot_directory))

path = list(sys.path)

if boot_directory in path:
    del path[path.index(boot_directory)]

try:
    (file, pathname, description) = imp.find_module('sitecustomize', path)
except ImportError:
    pass
else:
    imp.load_module('sitecustomize', file, pathname, description)


if root_directory not in sys.path:
    sys.path.insert(0, root_directory)

try:
    args = None
    with open(boot_directory + "/args.json", 'r') as f:
        args = f.read()
    new_args = json.loads(args) if args else {}
except BaseException as e:
    sys.stdout.write("Failed Reading Args From File. Error: %s" % str(e))
    sys.exit(3)

try:
    # python_agent.init.bootstrap()
    config.app["is_initial_color"] = True
    admin.cli(args=new_args["sl_args"], prog_name=new_args["prog_name"])
except SystemExit as e:
    if getattr(e, "code", 1) != 0:
        sys.exit(4)
except BaseException as e:
    sys.exit(5)

