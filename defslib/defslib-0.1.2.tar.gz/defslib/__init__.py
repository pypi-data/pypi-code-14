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
    strat = parse_stratum(x['morph'])
    x['chunks'] = strat['chunks']
    del(x['morph'])
  return yaml

def resolve_stratum(yaml):
  jsonschema.validate(yaml, load_yaml(os.path.join(os.path.join(os.path.dirname(__file__), 'spec/schemas/stratum.json-schema'))))
  for x in yaml['chunks']:
    if 'morph' in x:
      c = parse_chunk(x['morph'])
      del(x['morph'])
      x.update(c)
  return yaml

def resolve_chunk(yaml):
  jsonschema.validate(yaml, load_yaml(os.path.join(os.path.join(os.path.dirname(__file__), 'spec/schemas/chunk.json-schema'))))
  return yaml

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
