import os 
import tempfile
import string
from subprocess import call, check_output
import contextlib
import shutil
from io import StringIO
from configparser import RawConfigParser
import re
from tempfile import TemporaryDirectory

class GitMachine():

    def __init__(self, gitdir, tempdir, aliases, tar_url=None):
        self._gitdir = gitdir
        self._tmpdir = tempdir
        os.makedirs(self._gitdir, exist_ok=True)
        os.makedirs(self._tmpdir, exist_ok=True)
        self._aliases = aliases
        self._tar_url = tar_url

    def normalize_repo_url(self, repo):
        for alias, url in self._aliases.items():
            repo = repo.replace(alias, url)
        if repo.startswith("http") and not repo.endswith('.git'):
            repo = repo + '.git'
        return repo

    def normalize_repo_name(self, repo):
        def transl(x):
            return x if x in valid_chars else '_'
  
        valid_chars = string.digits + string.ascii_letters + '%_'
        url = self.normalize_repo_url(repo)
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

    def get_transport_info(self, repo):
        i = { 'url': self.normalize_repo_url(repo),
              'name': self.normalize_repo_name(repo) }
        i.update({'dir': os.path.join(self._gitdir, i['name'])})
        return i

    def get_submodule_details(self, checkout):
        with self.chdir(checkout):
            if os.path.exists('.gitmodules'):
                with open('.gitmodules', "r") as gitfile:
                    content = '\n'.join([l.strip() for l in gitfile.read().splitlines()])
                io = StringIO(content)
                parser = RawConfigParser()
                parser.readfp(io)
                return parser

    def submodule_info(self, repo, ref, submodule_mask={}, acc=''):
        self.mirror_repository(repo)
        with TemporaryDirectory() as tmpdir:
            it = self.get_transport_info(repo)
            call(['git', 'clone', it['dir'], tmpdir])
            with self.chdir(tmpdir):
               call(['git', 'checkout', ref])
            p = self.get_submodule_details(tmpdir)
            if not p:
               return
            for x in p.sections():
                submodule = re.sub(r'submodule "(.*)"', r'\1', x)
                path = p.get(x, 'path')
                try:
                    url = submodule_mask[path]['url']
                except:
                    url = p.get(x, 'url')

                with self.chdir(tmpdir):
                    commit = check_output(['git', 'ls-tree', ref, path]).split()
                fields = list(map(lambda x: x.decode('unicode-escape'), commit))
                if len(fields) >= 2 and fields[1] == 'commit':
                    submodule_commit = fields[2]

                    yield { 'path': os.path.join(acc, path), 'url': url, 'commit': submodule_commit } 
                    yield from self.submodule_info(url, submodule_commit, submodule_mask.get(path, {}).get('submodules', {}), path)

    def arrange_into_folder(self, repo, ref, submodule_mask, folder):
        tree = [ { 'path': '', 'url': repo, 'commit': ref } ] + list(self.submodule_info(repo, ref, submodule_mask))
        os.makedirs(folder, exist_ok=True)
        for x in tree:
            it = self.get_transport_info(x['url']) 
            call(['git', 'clone', '--quiet', '--no-hardlinks', it['dir'], os.path.join(folder, x['path'])])
            with self.chdir(os.path.join(folder, x['path'])):
               call(['git', 'checkout', x['commit']])

    def mirror_repository(self, repo):
        it = self.get_transport_info(repo)
        tar_file = it['name'] + '.tar'
        if not os.path.exists(it['dir']) and self._tar_url is not None:
            try:
                tmpdir = tempfile.mkdtemp()
                with self.chdir(tmpdir), open(os.devnull, "w") as fnull:
                    t = os.path.join(self._tar_url, tar_file)
                    print("Getting %s" % t)
                    call(['wget', t], stdout=fnull, stderr=fnull)
                    call(['tar', 'xf', tar_file], stderr=fnull)
                    call(['git', 'config', 'gc.autodetach', 'false'], stderr=fnull)
                    os.remove(tar_file)
                shutil.move(tmpdir, it['dir'])
            except:
                pass

        if os.path.exists(it['dir']):
            with self.chdir(it['dir']):
                if call(['git', 'fetch', it['url'], '+refs/*:refs/*', '--prune']):
                    raise Exception("Failed to update mirror for %s" % it['url'])
    
        else:
            tmpdir = tempfile.mkdtemp()
            print("Cloining %s" % it['url'])
            if call(['git', 'clone', '--mirror', '-n', it['url'], tmpdir]):
                raise Exception("Failed to clone %s" % it['url'])
            shutil.move(tmpdir, it['dir'])
