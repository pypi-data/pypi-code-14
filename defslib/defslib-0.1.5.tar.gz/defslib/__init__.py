import yaml
import glob
import sys
import jsonschema
import os
from fs.osfs import OSFS
import contextlib
from subprocess import call, check_output
import tempfile
import string
import shutil
import requests
import json
import hashlib

class MorphologyResolver():

  def __init__(self, directory):
    self._dfs = OSFS(directory)
    self._sdir = os.path.join(os.path.dirname(__file__), 'spec/schemas')
    self._sfs = OSFS(self._sdir) 
    self._database = {}
    self._schemas = { 'assemblage': self.load_schema('assemblage.json-schema'),
                      'chunk': self.load_schema('chunk.json-schema') }
    self._resolver = resolver = jsonschema.RefResolver('file://%s/' % self._sdir, self._schemas['assemblage'])

  def database(self):
    return self._database

  def evaluate_all(self, regex='*.morph'):
    for x in self._dfs.walkfiles(wildcard=regex):
      a = self.lookup(x)

  def load_morph(self, filename):
    with self._dfs.open(filename) as f:
      return yaml.safe_load(f.read())

  def load_schema(self, filename):
    with self._sfs.open(filename) as f:
      return yaml.safe_load(f.read())

  def lookup(self, filename):
    if not filename in self._database:
      a = self._database[filename] = self.parse_morph(filename)
      self._database[filename] = a

    return self._database[filename]
    
  def resolve_morph(self, yaml):
    if yaml.get('kind', '') == 'assemblage':
      return self.resolve_assemblage(yaml)
    else:
      return yaml

  def resolve_assemblage(self, yaml):
    for x in yaml['contents']:
      if 'morph' in x:
        a = self.lookup(x['morph'])
        x.update(a)
        del(x['morph'])
    return yaml

  def validate_assemblage(self, yaml):
    for x in yaml['contents']:
      try:
        if x.get('kind') == 'assemblage':
          self.validate_assemblage(x)
        else:
          self.validate_chunk(x)
      except Exception as e:
        if sys.version_info >= (3, 0):
          raise Exception("Failed to validate %s" % yaml['name']) from e
    schema = self._schemas['assemblage']
    jsonschema.validate(yaml, schema, resolver=self._resolver)

  def validate_chunk(self, yaml):
    jsonschema.validate(yaml, self._schemas['chunk'])
    return yaml

  def parse_morph(self, filename):
    a = self.load_morph(filename)
    return self.resolve_morph(a) 


class Actuator():

  def __init__(self, directories, aliases, tree_server=None):
    self._directories = directories
    self._aliases = aliases
    self._tree_server = tree_server

  def _normalize_repo_url(self, repo):
    for alias, url in self._aliases.items():
      repo = repo.replace(alias, url)
    if repo.startswith("http") and not repo.endswith('.git'):
      repo = repo + '.git'
    return repo

  def _normalize_repo_url_to_name(self, repo):
    def transl(x):
      return x if x in valid_chars else '_'

    valid_chars = string.digits + string.ascii_letters + '%_'
    url = self._normalize_repo_url(repo)
    if url.endswith('.git'):
      url = url[:-4]
    return ''.join([transl(x) for x in url])

  @contextlib.contextmanager
  def chdir(self, dirname=None):
      currentdir = os.getcwd()
      try:
          if dirname is not None:
              os.chdir(dirname)
          yield
      finally:
          os.chdir(currentdir)

  def mirror_chunk(self, chunk):
    tmpdir = tempfile.mkdtemp()
    repo_url = self._normalize_repo_url(chunk['repo'])
    repo_name = self._normalize_repo_url_to_name(chunk['repo'])
    gitdir = os.path.join(self._directories['gits'], repo_name)
    if os.path.exists(gitdir):
      with self.chdir(gitdir): 
        if call(['git', 'fetch', repo_url, '+refs/*:refs/*', '--prune']):
          raise Exception("Failed to update mirror for %s" % repo)

    if call(['git', 'clone', '--mirror', '-n', repo_url, tmpdir]):
      raise Exception("Failed to clone %s" % repo_url)

    with self.chdir(tmpdir):
      if call(['git', 'rev-parse']):
        raise Exception("Problem mirroring git repo at %s" % tmpdir)
 
    shutil.move(tmpdir, gitdir)

  def get_tree_for_chunk(self, chunk):
    ref = str(chunk['ref'])
    repo_url = self._normalize_repo_url(chunk['repo'])
    repo_name = self._normalize_repo_url_to_name(chunk['repo'])
    gitdir = os.path.join(self._directories['gits'], repo_name)
    if not os.path.exists(gitdir) and self._tree_server is not None:
      try:
        params = {'repo': repo_url, 'ref': ref}
        r = requests.get(url=self._tree_server, params=params)
        return r.json()['tree']
      except:
        pass
  
      self.mirror_chunk(chunk)
    with self.chdir(gitdir), open(os.devnull, "w") as fnull:
      if call(['git', 'rev-parse', ref + '^{object}'], stdout=fnull, stderr=fnull):
        self.mirror_chunk(chunk)
      try:
        tree = check_output(['git', 'rev-parse', ref + '^{tree}'],
                              universal_newlines=True)[0:-1]
        return tree
      except:
        raise Exception("No tree for ref %s in %s" % (ref, gitdir))

  def hash_thing_in_assemblage(self, thing, assemblage, parent_factors={}, global_factors={}):
    hash_factors = {}
    for x in thing.get('build-depends', []):
      a = list(filter(lambda y: y['name'] == x, assemblage['contents']))[0]
      if not 'cache' in a:
        a['cache'] = self.hash_thing_in_assemblage(a, assemblage, parent_factors, global_factors)
      hash_factors[x] = a
    if thing.get('kind', None) == 'assemblage':
      return self.get_assemblage_hash(thing, hash_factors, global_factors)
    else:
      tree = self.get_tree_for_chunk(thing)
      thing.update({ 'tree': tree })
      factors = thing.copy()
      factors.update( {
        'hash_factors' : hash_factors,
        'parent_factors' : parent_factors,
        'global_factors' : global_factors
      })
      return hashlib.sha256(json.dumps(factors, sort_keys=True).encode('utf-8')).hexdigest()

  def get_assemblage_hash(self, assemblage, parent_factors={}, global_factors={}):
    for x in assemblage['contents']:
      if not 'cache' in x:
        x['cache'] = self.hash_thing_in_assemblage(x, assemblage, parent_factors, global_factors)
    factors = assemblage.copy()
    factors.update( { 'parent_factors' : parent_factors,
                      'global_factors' : global_factors })
    return hashlib.sha256(json.dumps(factors, sort_keys=True).encode('utf-8')).hexdigest()
