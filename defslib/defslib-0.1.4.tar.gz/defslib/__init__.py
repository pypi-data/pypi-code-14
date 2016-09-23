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
import networkx

class MorphologyResolver():

  def __init__(self, directory):
    self._dfs = OSFS(directory)
    self._sdir = os.path.join(os.path.dirname(__file__), 'spec/schemas')
    self._sfs = OSFS(self._sdir) 
    self._database = {}

  def database(self):
    return database

  def evaluate_all(self, regex='*.morph'):
    for x in self._dfs.walkfiles(wildcard=regex):
      a = self.lookup(x)
      if a.get('kind') == 'assemblage':
        self.validate_assemblage(a)

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
    schema = self.load_schema('assemblage.json-schema')
    resolver = jsonschema.RefResolver('file://%s/' % self._sdir, schema)
    jsonschema.validate(yaml, schema, resolver=resolver)

  def validate_chunk(self, yaml):
    jsonschema.validate(yaml, self.load_schema('chunk.json-schema'))
    return yaml

  def parse_morph(self, filename):
    a = self.load_morph(filename)
    return self.resolve_morph(a) 

def normalize_repo_url(aliases, repo):
  for alias, url in aliases.items():
    repo = repo.replace(alias, url)
  if repo.startswith("http") and not repo.endswith('.git'):
    repo = repo + '.git'
  return repo

def normalize_repo_url_to_name(aliases, repo):
  def transl(x):
    return x if x in valid_chars else '_'

  valid_chars = string.digits + string.ascii_letters + '%_'
  url = normalize_repo_url(aliases, repo)
  if url.endswith('.git'):
    url = url[:-4]
  return ''.join([transl(x) for x in url])

@contextlib.contextmanager
def chdir(dirname=None):
    currentdir = os.getcwd()
    try:
        if dirname is not None:
            os.chdir(dirname)
        yield
    finally:
        os.chdir(currentdir)

def mirror_chunk(chunk, git_directory, aliases={}):
  tmpdir = tempfile.mkdtemp()
  repo_url = normalize_repo_url(aliases, chunk['repo'])
  repo_name = normalize_repo_url_to_name(aliases, chunk['repo'])
  gitdir = os.path.join(git_directory, repo_name)
  if os.path.exists(gitdir):
    with chdir(gitdir): 
      if call(['git', 'fetch', repo_url, '+refs/*:refs/*', '--prune']):
        raise Exception("Failed to update mirror for %s" % repo)

  if call(['git', 'clone', '--mirror', '-n', repo_url, tmpdir]):
    raise Exception("Failed to clone %s" % repo_url)

  with chdir(tmpdir):
    if call(['git', 'rev-parse']):
      raise Exception("Problem mirroring git repo at %s" % tmpdir)

  gitdir = os.path.join(git_directory, repo_name)
  shutil.move(tmpdir, gitdir)

def get_tree_for_chunk(chunk, git_directory, aliases={}, tree_server=None):
  ref = str(chunk['ref'])
  repo_url = normalize_repo_url(aliases, chunk['repo'])
  repo_name = normalize_repo_url_to_name(aliases, chunk['repo'])
  gitdir = os.path.join(git_directory, repo_name)
  if not os.path.exists(gitdir):
    params = {'repo': repo_url, 'ref': ref}
    r = requests.get(url=tree_server, params=params)
    return r.json()['tree']

    mirror_chunk(chunk, aliases, git_directory)
  with chdir(gitdir), open(os.devnull, "w") as fnull:
    if call(['git', 'rev-parse', ref + '^{object}'], stdout=fnull,
             stderr=fnull):
      mirror_chunk(chunk, git_directory, aliases)
    try:
      tree = check_output(['git', 'rev-parse', ref + '^{tree}'],
                            universal_newlines=True)[0:-1]
      return tree
    except:
      raise Exception("No tree for ref %s in %s" % (ref, gitdir))

def get_chunk_hash(chunk, git_directory, aliases={}, extra_factors={}):
  tree = get_tree_for_chunk(chunk, git_directory, aliases)
  chunk['tree'] = tre
  factors = json.dumps(chunk, sort_keys=True).encode('utf-8')
  return hashlib.sha256(factors.update(extra_factors))

def get_stratum_bd_graph(stratum):
  G = networkx.DiGraph()
  for y in stratum['chunks']:
    G.add_node((stratum['name'], y['name']), chunk=y)
  for y in stratum['chunks']:
    for z in y.get('build-depends', []):
      G.add_edge((stratum['name'], y['name']), (stratum['name'], z))
  return G

def get_system_bd_graph(system):
  H = networkx.DiGraph()
  strat_graphs = dict((x['name'], get_stratum_bd_graph(x)) for x in system['strata'])
  for x in system['strata']:
    H.add_node(strat_graphs[x['name']], stratum=x)
    for y in x.get('build-depends', []):
      H.add_edge(strat_graphs[x['name']], strat_graphs[y]) 
  return H
