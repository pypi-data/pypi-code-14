import contextlib
import glob
import hashlib
import json
import jsonschema
import os
import requests
import shutil
import string
import sys
import tempfile
import toposort
import yaml

from copy import deepcopy
from fs.osfs import OSFS
from subprocess import call, check_output

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

  def flatten_assemblage(self, assemblage):
    contents = assemblage['contents']
    asses = list(filter(lambda x: x.get('kind', None) == 'assemblage', contents))
    for x in asses:
      sub = self.flatten_assemblage(x)['contents']
      lens = self.lens(x, contents)
      for i in sub:
        i['build-depends'] = sorted(list(set(i.get('build-depends', []) + list(map(lambda z: z['name'], lens['supports'])))))
      for y in lens['burdens']:
        y['build-depends'].remove(x['name'])
        y['build-depends'] = sorted(list(set(y.get('build-depends', []) + list(map(lambda t: t['name'], sub)))))
      contents = self.toposort_contents(lens['supports'] + lens['burdens'] + sub + lens['noncomps'])
    assemblage['contents'] = list(filter(lambda z: z.get('kind', None) != 'assemblage', contents))
    return assemblage

  def lens(self, focus, contents):
    def comparator(x,y):
      return x['name'] in y.get('build-depends', [])

    return { 'supports': list(filter(lambda z: comparator(z, focus), contents)),
             'burdens': list(filter(lambda z: comparator(focus, z), contents)),
             'noncomps': list(filter(lambda z: not comparator(z, focus) and not comparator(focus, z), contents)) }

  def toposort_contents(self, contents):
    key_depends = dict((x['name'], set(x.get('build-depends', []))) for x in contents)
    topo = list(toposort.toposort_flatten(key_depends))
    sorted(contents, key=lambda x: topo.index(x['name']))
    return contents

  def cache_enrich_assemblage(self, assemblage, supports=[], global_factors={}):
    contents = self.toposort_contents(assemblage['contents'])
    for x in contents:
      if 'cache' in x:
        continue
      lens = self.lens(x, contents)
      if x.get('kind', None) == 'assemblage':
        self.cache_enrich_assemblage(x, lens['supports'] + supports, global_factors)
      else:
        tree = self.get_tree_for_chunk(x)
        x.update({ 'tree': tree })
        factors = deepcopy(x)
        factors.update( {
          'supports' : supports + lens['supports'],
          'global_factors' : global_factors
        })
        x['cache'] = hashlib.sha256(json.dumps(factors, sort_keys=True).encode('utf-8')).hexdigest()

      factors = deepcopy(assemblage)
      factors.update( { 'supports': supports,
                        'global_factors' : global_factors })
      assemblage['cache'] = hashlib.sha256(json.dumps(factors, sort_keys=True).encode('utf-8')).hexdigest()
