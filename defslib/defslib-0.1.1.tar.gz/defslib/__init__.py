import yaml
import glob
import sys
import jsonschema
import os
from fs.osfs import OSFS

def generate_manifest_from_directory(directory):
  fs = OSFS(directory)
  morphs = fs.walkfiles(path=directory, wildcard="*.morph")
  return {x.rpartition('.morph')[0]: parse_morph(os.path.join(directory, x)) for x in morphs}

def parse_morph(filename):
  a = load_yaml(filename)
  getattr(__import__(__name__), "resolve_%s" % a['kind'])(a)

def load_yaml(filename):
  with open(filename) as f:
    text = f.read()
  contents = yaml.safe_load(text)
  return contents

def parse_cluster(filename):
  return resolve_cluster(load_yaml(filename))

def parse_system(filename):
  return resolve_system(load_yaml(filename))
  
def parse_stratum(filename):
  return resolve_stratum(load_yaml(filename))
  
def parse_chunk(filename):
  return resolve_chunk(load_yaml(filename))
  
def resolve_cluster(yaml):
  jsonschema.validate(yaml, load_yaml(os.path.join(os.path.join(os.path.dirname(__file__), 'spec/schemas/cluster.json-schema'))))
  return yaml

def resolve_system(yaml):
  jsonschema.validate(yaml, load_yaml(os.path.join(os.path.join(os.path.dirname(__file__), 'spec/schemas/system.json-schema'))))
  for x in yaml['strata']:
    x['chunks'] = parse_stratum(x['morph'])['chunks']
    del(x['morph'])
  return yaml

def resolve_stratum(yaml):
  jsonschema.validate(yaml, load_yaml(os.path.join(os.path.join(os.path.dirname(__file__), 'spec/schemas/stratum.json-schema'))))
  for x in yaml['chunks']:
    if 'morph' in x:
      c = load_yaml(x['morph'])
      del(x['morph'])
      x.update(c)
  return yaml

def resolve_chunk(yaml):
  jsonschema.validate(yaml, load_yaml(os.path.join(os.path.join(os.path.dirname(__file__), 'spec/schemas/chunk.json-schema'))))
  return yaml
