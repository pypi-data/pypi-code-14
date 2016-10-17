import sys

from contextlib import ContextDecorator
from inhoj.classes import GracefulDeath


class gracefuldeath(ContextDecorator):

    def __init__(self, message_for_kill=''):
        self.message_for_kill = message_for_kill

    def __enter__(self):
        self.killer = GracefulDeath(self.message_for_kill)
        return self

    def __exit__(self, *exc):
        if self.killer.kill_now:
            sys.exit(0)
        return False
