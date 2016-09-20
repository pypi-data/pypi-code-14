import sys

from bintraypy_cli.cmd import BintrayPyCLI


def main(*argv, exitAfter=True):
  try:
    if not argv:
      argv = sys.argv
    _, ret = BintrayPyCLI.run(argv=argv, exit=exitAfter)
    return ret
  except KeyboardInterrupt as ex:
    print(ex)
