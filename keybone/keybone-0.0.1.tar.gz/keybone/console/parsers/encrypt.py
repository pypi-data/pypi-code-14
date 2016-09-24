import argparse

parser = argparse.ArgumentParser(
    prog='keybone encrypt',
    description='encrypts the data to a known recipient')

parser.add_argument('recipient', metavar='<recipient>', help='the recipient to encrypt the data to')
parser.add_argument('plaintext', metavar='<plaintext>', help='the content to be encrypted')
parser.add_argument('--sign', action='store_true', default=False, help='whether to sign the final ciphertext')
parser.add_argument('--secret', metavar='<passphrase>', help='a passphrase')
