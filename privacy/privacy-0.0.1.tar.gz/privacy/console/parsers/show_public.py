import argparse

parser = argparse.ArgumentParser(
    prog='privacy public',
    description='prints the public key of the given email')

parser.add_argument('recipient', metavar='<recipient>', help='any identification for the key: fingerprint, id or email')
