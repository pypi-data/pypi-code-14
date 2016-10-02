import sys

from contextlib import ContextDecorator
from inhoj.classes import GracefulDeath


class gracefuldeath(ContextDecorator):

    def __enter__(self):
        self.killer = GracefulDeath()
        return self

    def __exit__(self, *exc):
        if self.killer.kill_now:
            sys.exit(0)
        return False
