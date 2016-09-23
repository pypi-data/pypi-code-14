# -*- coding: utf-8 -*-
"""Command-line tool package."""

import click
import logging

from steenzout import barcode
from steenzout.barcode import writer


LOGGER = logging.getLogger(__name__)


@click.group()
@click.version_option(version=barcode.__version__)
def cli():
    pass


@cli.command()
@click.option('-v', '--verbose', 'verbosity', count=True, help='Enables verbosity.')
@click.option('-c', '--code', 'code', type=click.STRING)
@click.option('-i', '--input', 'input', type=click.File('rb'))
@click.option('-e', '--encoding', 'encoding', default='code39', type=click.Choice(barcode.encodings()))
@click.option('-f', '--format', 'format', default='SVG', type=click.Choice(barcode.formats()))
@click.option('-u', '--unit', 'unit', type=click.STRING)
@click.argument('output', type=click.File('wb'))
def generate(verbosity, code, input, encoding, format, unit, output):
    """Generates the bar code."""
    LOGGER.debug('generate(): %s, %s, %s, %s, %s, %s', verbosity, encoding, format, unit, input, output)

    if format == 'SVG':
        opts = dict(compress=False)
        writer_instance = writer.SVG()
    else:
        opts = dict(format=format)
        writer_instance = writer.ImageWriter()

    if code is not None:
        bar_code = code
    else:
        bar_code = input.read()

    barcode.generate(encoding, bar_code, writer_instance, output, opts)


@cli.command()
def encodings():
    """List the available bar codes."""
    LOGGER.debug('encodings()')

    for fmt in barcode.encodings():
        click.echo(fmt)


@cli.command()
def formats():
    """List the available image formats."""
    LOGGER.debug('formats()')

    for fmt in barcode.formats():
        click.echo(fmt)
