import imp

buku = imp.load_source('buku', 'buku')

import buku

def entry_point():
    buku.entry_point()

if __name__ == "__main__":
    entry_point()