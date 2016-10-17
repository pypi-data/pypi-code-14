import contextlib
import glob
import hashlib
import json
import jsonschema
import os
import requests
import sandboxlib
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
    self._schemas = { 'assemblage': self.load_schema('assemblage.json-schema'),
                      'chunk': self.load_schema('chunk.json-schema') ,
                      'defaults': self.load_schema('defaults.json-schema') }
    
    self.database = {}
    self.defaults = self.load_morph('DEFAULTS')
    self.validate_defaults(self.defaults)

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
    if not filename in self.database:
      a = self.database[filename] = self.parse_morph(filename)
      self.database[filename] = a

    return self.database[filename]

  def resolve_morph(self, yaml):
    if yaml.get('kind', '') == 'assemblage':
      return self.resolve_assemblage(yaml)
    else:
      if 'build-system' in yaml:
        x = deepcopy(self.defaults['build-systems'][yaml['build-system']])
        x.update(yaml)
        x.pop('build-system')
        return x
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
    resolver = jsonschema.RefResolver('file://%s/' % self._sdir, schema)
    jsonschema.validate(yaml, schema, resolver=resolver)

  def validate_chunk(self, yaml):
    jsonschema.validate(yaml, self._schemas['chunk'])
    return yaml

  def validate_defaults(self, yaml):
    schema = self._schemas['defaults']
    resolver = jsonschema.RefResolver('file://%s/' % self._sdir, schema)
    jsonschema.validate(yaml, self._schemas['defaults'], resolver=resolver)
    return yaml

  def parse_morph(self, filename):
    a = self.load_morph(filename)
    return self.resolve_morph(a)


class Actuator():

  def __init__(self, directories, aliases, defaults, executor="chroot"):
    self._directories = directories
    for x in list(directories.values()):
     os.makedirs(x, exist_ok=True)
    self._aliases = aliases
    self._defaults = defaults
    self._executor = executor
    self.arch = 'x86_64'
    self.cpu = 'i686'
    self.abi = ''
    if self.arch.startswith(('armv7', 'armv5')):
        self.abi = 'eabi'
    elif self.arch.startswith('mips64'):
        self.abi = 'abi64'

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
          raise Exception("Failed to update mirror for %s" % repo_url)

    elif call(['git', 'clone', '--mirror', '-n', repo_url, tmpdir]):
      raise Exception("Failed to clone %s" % repo_url)

    with self.chdir(tmpdir):
      if call(['git', 'rev-parse']):
        raise Exception("Problem mirroring git repo at %s" % tmpdir)

    shutil.move(tmpdir, gitdir)

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

  def copytree(self, src, dst, symlinks = False, ignore = None):
    if not os.path.exists(dst):
      os.makedirs(dst)
      shutil.copystat(src, dst)

    try:
      lst = os.listdir(src)
    except FileNotFoundError as e:
      print("copytree({},{}) on {}".format(src,dst,os.getcwd()))
      raise e

    if ignore:
      excl = ignore(src, lst)
      lst = [x for x in lst if x not in excl]
    for item in lst:
      s = os.path.join(src, item)
      d = os.path.join(dst, item)
      if symlinks and os.path.islink(s):
        if os.path.lexists(d):
          os.remove(d)
        os.symlink(os.readlink(s), d)
        try:
          st = os.lstat(s)
          mode = stat.S_IMODE(st.st_mode)
          os.lchmod(d, mode)
        except:
          pass # lchmod not available
      elif os.path.isdir(s):
        self.copytree(s, d, symlinks, ignore)
      else:
        shutil.copy2(s, d)

  def build_assemblage(self, assemblage):
    tempfile.tempdir = self._directories['tmp']
    os.environ['TMPDIR'] = self._directories['tmp']

    artifact_store = lambda x: os.path.join(self._directories['artifacts'], "%s.%s" % (x['name'], x['cache']))
    build = deepcopy(assemblage)
    self.flatten_assemblage(build)
    self.toposort_contents(build['contents'])

    for x in build['contents']:
      target_artifact = artifact_store(x)
      if os.path.exists(target_artifact):
        continue
      lens = self.lens(x, build['contents'])
      sandbox = tempfile.mkdtemp()
      checkout = "%s.build" % x['name']
      install = "%s.install" % x['name']
      baserockdir = 'baserock'

      for a in [install, baserockdir]:
        os.makedirs(os.path.join(sandbox,a))

      for y in lens['supports']:
        p = artifact_store(y)
        self.copytree(p, sandbox)

      self.mirror_chunk(x)

      repo_url = self._normalize_repo_url(x['repo'])
      repo_name = self._normalize_repo_url_to_name(x['repo'])
      gitdir = os.path.join(self._directories['gits'], repo_name)

      call(['git', 'clone', gitdir, os.path.join(sandbox,checkout)])
      call(['git', 'checkout', x['ref']], cwd=os.path.join(sandbox,checkout))

      print("Building %s" % x['name'])
      for z in self._defaults.get('build-steps', []):
        for c in x.get(z, []):
          bootstrapped=(x['build-mode'] == 'bootstrap')
          env = self.setup_env(DESTDIR="%s/%s.install" % (os.path.abspath(sandbox) if bootstrapped else '/', x['name']),PREFIX=x.get('prefix', '/usr'))
          self.run_sandbox(c, root_fs=sandbox, name=x['name'], env=env, bootstrapped=bootstrapped)
      self.copytree(os.path.join(sandbox,install), artifact_store(x))
      shutil.rmtree(sandbox)

  def setup_env(self, **kwargs):
    env = { 'MAKEFLAGS' : "-j {}".format(1),
            'PATH' : '/tools/bin:/usr/bin:/bin:/usr/sbin:/sbin',
            'TERM' : 'dumb',
            'SHELL' : '/bin/sh',
            'USER' : 'tomjon',
            'USERNAME' : 'tomjon',
            'LC_ALL' : 'C',
            'HOME' : '/tmp',
            'TZ' : 'UTC',
            'TARGET' : "%s-baserock-linux-gnu%s" % (self.cpu, self.abi),
            'TARGET_STAGE1' : "%s-bootstrap-linux-gnu%s" % (self.cpu, self.abi),
            'MORPH_ARCH' : self.arch
          }
    env.update(kwargs)
    return env

  def run_sandbox(self, command, root_fs, name, env=None, bootstrapped=False):
    mounts = []
    writables = ["%s/%s.build" % (os.path.abspath(root_fs) if bootstrapped else '/', name),
                 "%s/%s.install" % (os.path.abspath(root_fs) if bootstrapped else '/', name),
                 "/tmp"]
    if not bootstrapped:
      mounts.extend([('tmpfs', '/tmp', 'tmpfs'),
                     ('proc', '/proc', 'proc')])

    config = { 'mounts': 'isolated',
               'network': 'isolated',
               'cwd': "%s/%s.build" % (os.path.abspath(root_fs) if bootstrapped else '/', name),
               'filesystem_root': '/' if bootstrapped else os.path.abspath(root_fs),
               'filesystem_writable_paths': writables,
               'extra_mounts': mounts }

    executor=sandboxlib.get_executor(self._executor)
    config = executor.degrade_config_for_capabilities(config, warn=False)
    print("Running command %s" % command)
    argv = ['sh', '-c', '-e', command]
    exit, out, error = executor.run_sandbox(argv, env=env, **config)

    print(out.decode('unicode-escape'))
    if exit != 0:
      print(error.decode('unicode-escape'))
      exit(1)
