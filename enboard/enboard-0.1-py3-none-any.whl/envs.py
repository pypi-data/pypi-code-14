import os
from pathlib import Path
import shutil

_PKGDIR = Path(__file__).parent.resolve()

class MenuItem:
    def __init__(self, display, *, data=None):
        self.display = display
        self.data = data
    
    def __repr__(self):
        p = [type(self).__name__, '(', repr(self.display)]
        if self.data is not None:
            p += [', data=', repr(self.data)]
        p += [')']
        return ''.join(p)

class CondaEnv:
    def __init__(self, path):
        self.path = path
        self.display = path.name
    
    def __repr__(self):
        return 'CondaEnv(%r)' % self.path
    
    def delete(self):
        shutil.rmtree(str(self.path))

    def activate(self):
        e = os.environ
        e['PATH'] = str(self.path / 'bin') + ':' + e['PATH']
        e['CONDA_DEFAULT_ENV'] = self.path.name
        e['CONDA_PREFIX'] = str(self.path)
        print("Launching bash with conda environment: %s" % self.path.name)
        print("Press Ctrl-D to exit.", flush=True)
        os.execvp('bash', ['bash', '--rcfile', str(_PKGDIR / 'conda-bashrc.sh')])

def find_conda_envs():
    env_dir = Path('~/miniconda3/envs').expanduser()
    for f in env_dir.iterdir():
        if f.is_dir():
            yield CondaEnv(f)
    

def find_envs():
    envs = list(find_conda_envs())
    return sorted(envs, key=lambda x: x.display.lower())
