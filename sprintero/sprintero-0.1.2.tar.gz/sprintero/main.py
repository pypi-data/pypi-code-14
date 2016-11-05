# -*- coding: utf-8 -*-

import click

from sprintero.commands import top_level

cli = click.CommandCollection(
    sources=[top_level]
)


def main():
    cli(obj={})
