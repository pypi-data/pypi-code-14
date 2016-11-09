import argparse

parser = argparse.ArgumentParser(
    prog='privacy import',
    description='imports a key')

parser.add_argument('key', metavar='<key>', help='as string, with linebreaks')
