import yaml
import glob
import sys
import jsonschema
import os

def load_yaml(filename):
  with open(filename) as f:
    text = f.read()
  contents = yaml.safe_load(text)
  return contents

def parse_system(system):
  a = load_yaml(system)
  jsonschema.validate(a, load_yaml(os.path.join(os.path.join(os.path.dirname(__file__), 'spec/schemas/system.json-schema'))))
  for x in a['strata']:
    x['chunks'] = parse_stratum(x['morph'])['chunks']
    del(x['morph'])
  return a

def parse_stratum(stratum):
  a = load_yaml(stratum)
  jsonschema.validate(a, load_yaml(os.path.join(os.path.join(os.path.dirname(__file__), 'spec/schemas/stratum.json-schema'))))
  for x in a['chunks']:
    if 'morph' in x:
      c = load_yaml(x['morph'])
      del(x['morph'])
      x.update(c)
  return a

def parse_chunk(chunk):
  a = load_yaml(chunk)
  jsonschema.validate(a, load_yaml(os.path.join(os.path.join(os.path.dirname(__file__), 'spec/schemas/chunk.json-schema'))))
  return a
