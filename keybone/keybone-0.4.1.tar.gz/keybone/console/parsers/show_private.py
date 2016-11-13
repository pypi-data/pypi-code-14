import argparse

parser = argparse.ArgumentParser(
    prog='keybone private',
    description='prints the private key of the given recipient')

parser.add_argument('recipient', metavar='<recipient>', help='any identification for the key: fingerprint, id or email')
