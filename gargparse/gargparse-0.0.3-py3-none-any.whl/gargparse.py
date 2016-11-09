import argparse



_PARSER = argparse.ArgumentParser()


def add_argument(*args, **kwargs):
  _PARSER.add_argument(*args, **kwargs)


def parse_args(*args, **kwargs):
  global ARGS
  ARGS = _PARSER.parse_args(*args, **kwargs)
