# based on django's old implementation
import os, sys, time
from subprocess import Popen
import _thread

# This import does nothing, but it's necessary to avoid some race conditions
# in the threading module. See http://code.djangoproject.com/ticket/2330 .
import threading

RUN_RELOADER = True

_mtimes = {}
_win = (sys.platform == "win32")

def code_changed():
    global _mtimes, _win
    for filename in filter(None, [getattr(m, "__file__", None) for m in list(sys.modules.values())]):
        if not os.path.exists(filename):
            continue # File might be in a zip file
        stat = os.stat(filename)
        mtime = stat.st_mtime
        if _win:
            mtime -= stat.st_ctime
        if filename not in _mtimes:
            _mtimes[filename] = mtime
            continue
        if mtime != _mtimes[filename]:
            _mtimes = {}
            return True
    return False

def ensure_echo_on():
    # pdb redirects stdio. if autoreload had happened when a pdb break had been activated, echo would be lost.
    if sys.platform.startswith("linux"):
        Popen(('stty', 'echo')) 

def python_reloader(main_func, args, kwargs):
    if os.environ.get("RUN_MAIN") == "true":
        _thread.start_new_thread(main_func, args, kwargs)
        try:
            while RUN_RELOADER:
                if code_changed():
                    sys.exit(3) # force reload
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    else:
        try:
            while True:
                args = [sys.executable] + sys.argv
                if sys.platform == "win32":
                    args = ['"%s"' % arg for arg in args]
                new_environ = os.environ.copy()
                new_environ["RUN_MAIN"] = 'true'
                exit_code = os.spawnve(os.P_WAIT, sys.executable, args, new_environ)
                ensure_echo_on()
                if exit_code != 3:
                    print('-' * 8, 'exit code: ', exit_code, '-' * 8, '\n')
                    time.sleep(4)
                    #sys.exit(exit_code)
        except KeyboardInterrupt:
            ensure_echo_on()

def main(main_func, args=None, kwargs=None):
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}
    python_reloader(main_func, args, kwargs)

