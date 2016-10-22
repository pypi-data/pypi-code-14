#!/usr/bin/env pyhton
# -*- coding: utf-8 -*-

import click
import hashlib


@click.command(options_metavar='<options>')
@click.option('--cksum', '-c',
        type=click.Choice(['md5', 'sha1', 'sha224', 'sha256','sha384', 'sha512']),
        default='md5')
@click.argument('org_hash', metavar='org_hash')
@click.argument('filename', type=click.Path(exists=True),
        metavar='filename')
def cli(cksum, filename, org_hash):
        if cksum == 'md5':
            hash = hashlib.md5()
        elif cksum == 'sha1':
            hash = hashlib.sha1()
        elif cksum == 'sha224':
            hash = hashlib.sha224()
        elif cksum == 'sha256':
            hash = hashlib.sha256()
        elif cksum == 'sha384':
            hash = hashlib.sha384()
        elif cksum == 'sha512':
            hash = hashlib.sha512()

        with click.open_file(filename, 'rb') as file:
            for block in iter(lambda: file.read(65536), b""):
                hash.update(block)

        if org_hash == hash.hexdigest():
            click.echo('file path: %s' % click.format_filename(filename))
            click.echo('original hash: %s' % org_hash)
            click.echo('checksum: %s' % cksum)
            click.echo(click.style('[+] hashes match!', fg='cyan'))
        else:
            click.echo('file path: %s' % click.format_filename(filename))
            click.echo('original hash: %s' % org_hash)
            click.echo('checksum: %s' % cksum)
            click.echo(click.style('[-] hashes do not match!', fg='red'))

if __name__ == '__main__':
    cli()
