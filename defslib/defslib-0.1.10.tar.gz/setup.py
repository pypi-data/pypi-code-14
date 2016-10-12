from distutils.core import setup
from fs.osfs import OSFS
import yaml
import json
import os

sdir = os.path.join(os.path.dirname(__file__), 'defslib/spec/schemas')
sfs = OSFS(sdir)

for x in sfs.walkfiles(wildcard='*.json-schema'):
  with sfs.open(x, "r+") as f:
    a = yaml.safe_load(f.read())
    f.seek(0)
    f.write(json.dumps(a))
    f.truncate()


setup(
  name = 'defslib',
  packages = ['defslib'],
  version = '0.1.10',
  description = 'Baserock definitions parser',
  author = 'Daniel Firth',
  author_email = 'locallycompact@gmail.com',
  url = 'https://gitlab.com/baserock/spec',
  keywords = [],
  classifiers = [],
  package_data={'defslib': ['spec/schemas/*.json-schema', 'spec/schemas/*.json-schema']}
)
