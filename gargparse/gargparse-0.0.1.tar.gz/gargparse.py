import argparse



_PARSER = argparse.ArgumentParser()


def add_argument(*args, **kwargs):
  _PARSER.add_argument(*args, **kwargs)


def parse_args(*args, **kwargs):
  return _PARSER.parse_args(*args, **kwargs)
