import argparse

parser = argparse.ArgumentParser(
    prog='keybone keyid',
    description='prints the keyid of the given recipient')

parser.add_argument('recipient', metavar='<recipient>', help='any identification for the key: fingerprint, id or email')
# parser.add_argument('--private', action='store_true', default=False, help='show only private keys')
# parser.add_argument('--public', action='store_true', default=True, help='show only public keys')
