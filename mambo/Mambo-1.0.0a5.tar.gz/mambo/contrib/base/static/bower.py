"""
Mambo Bower

It's a dev tool for 3rd party assets using bower.

Its main purpose to only keep the necessary files of the 3rd party.

3rdparty vendors are place under /assets/Mambo/vendor

Do not put non bower files in the /assets/Mambo/vendor directory.

Place your files in /assets/Mambo/lib

Dependencies: Bower

To run this file: python mambo-bower.py

"""

import os
import sh
import json
from mambo import utils

VERSION = "0.1.0"

DEPENDENCIES = {
    "jquery": {
        "version": "~2.2.4",
        "copy": ["dist/jquery.min.js"]
    },
    "bootstrap": {
        "version": "~3.3",
        "copy": ["dist/css",
                 "dist/fonts",
                 "dist/js"]
    },
    "font-awesome": {
        "version": "~4.6",
        "copy": ["css/", "fonts/"]
    },
    "jquery-form-validator": {
        "version": "~2.2.8",
        "copy": ["form-validator/"]
    },
    "jquery-lazy": {
        "version": "~1.6.5",
        "copy": ["jquery.lazy.min.js"]
    },
    "js-cookie": {
        "version": "~2.1.0",
        "copy": ["src/js.cookie.js"]
    },
    "jssocials": {
        "version": "~1.1.0",
        "copy": ["dist/jssocials.js",
                 "dist/jssocials.css",
                 "dist/jssocials-theme-flat.css"]
    },
    "bootstrap-social": {
        "version": "~4.9.0",
        "copy": ["bootstrap-social.css"]
    },
    "eonasdan-bootstrap-datetimepicker": {
        "version": "~4.17.37",
        "copy": ["build/css/bootstrap-datetimepicker.min.css",
                 "build/js/bootstrap-datetimepicker.min.js"]
    },
    "moment": {
        "version": "~2.8",
        "copy":["moment.js"]
    },
    "moment-timezone": {
        "version": "~0.4",
        "copy": ["moment-timezone.js",
                 "moment-timezone-utils.js"]
    }

}

# ------------------------------------------------------------------------------
# DO NOT CHANGE BELOW
# ------------------------------------------------------------------------------

CWD = os.getcwd()
VENDOR_DIR = "%s/Mambo/vendor" % CWD
BOWER_COMPONENTS_DIR = "%s/bower_components" % CWD

print("-" * 80)
print("Mambo Bower")
print("")

bower = {
    "name": "Mambo",
    "version": VERSION,
    "dependencies": {d:v["version"] for d, v in DEPENDENCIES.items()}
}

if os.path.exists(VENDOR_DIR):
    utils.remove_dir(VENDOR_DIR)

if not os.path.exists(VENDOR_DIR):
    utils.make_dirs(VENDOR_DIR)

print("Saving bower.json ...")
with open("./bower.json", "w+") as f:
    f.write(json.dumps(bower))

print("Running bower install ...")
with sh.pushd(CWD):
    #sh.bower("cache", "clean")
    sh.bower("install", "--force-latest")
    #sh.bower("prune")

print("Copying files to vendor directories ...")
for name, v in DEPENDENCIES.items():
    vendor_dir = "%s/%s" % (VENDOR_DIR, name)
    if not os.path.exists(vendor_dir):
        utils.make_dirs(vendor_dir)
    if "copy" in v:
        for f in v["copy"]:
            source = "%s/%s/%s" % (BOWER_COMPONENTS_DIR, name, f)
            dest = "%s/%s" % (vendor_dir, f)
            f = f.rsplit("/", 1)[1] if "/" in f else f
            dest = "%s/%s" % (vendor_dir, f)
            if f.endswith(".css") or f.endswith(".js"):
                utils.copy_file(source, dest)
            else:
                utils.copy_dir(source, dest)
                pass

#-----

# FONT AWESOME
# Cleanup font awesome to make sure it points to the right fonts
print("Copying Font-Awesome...")
fa_src = "%s/font-awesome" % VENDOR_DIR
for _ in ["font-awesome.css", "font-awesome.min.css"]:
    with open("%s/%s" % (fa_src, _), "r+") as f:
        content = f.read().replace("../fonts/", "./")
        f.seek(0)
        f.write(content)
        f.truncate()

# Copy Font-awesome to the skeleton.
# It is needed since it will be loaded from static
fa_dest = "../../../skel/assets/static/vendor/font-awesome"
if not os.path.exists(fa_dest):
    utils.make_dirs(fa_dest)
utils.copy_dir(fa_src, fa_dest)


print("Cleaning up...")
if os.path.exists(BOWER_COMPONENTS_DIR):
    utils.remove_dir(BOWER_COMPONENTS_DIR)

print("Done!")

