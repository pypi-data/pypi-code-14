from __future__ import absolute_import
import progressbar as pbm
from time import time
import sys

class ProgressBar(object):
    """Wrapper around `progressbar.Progressbar` to make it easier to use."""
    def __init__(self, n):
        self._pb = pbm.ProgressBar(widgets=[pbm.Percentage(), pbm.Bar()],
                                   maxval=n).start()

    def update(self, i):
        self._pb.update(i)

    def finish(self):
        self._pb.finish()

class BeginEnd(object):
    """Prints message before and after the end of block of code."""
    def __init__(self, task, silent=False):
        self._task = str(task)
        self._start = None
        self._silent = silent

    def __enter__(self):
        self._start = time()
        if not self._silent:
            print('-- %s start --' % self._task)
            sys.stdout.flush()

    def __exit__(self, *args):
        elapsed = time() - self._start
        if not self._silent:
            print('-- %s end (%.2f s) --' % (self._task, elapsed))
            sys.stdout.flush()

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
