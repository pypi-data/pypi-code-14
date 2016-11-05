# -*- coding: utf-8 -*-

import click

from sprintero.constants import NamesCollectionsE
from sprintero.generator import NameGenerator
from sprintero.names_collection.picker import CollectionPicker


@click.group()
def top_level():
    pass


@top_level.command()
@click.option('--badass/--no-badass', default=False)
@click.option('--collection', default=NamesCollectionsE.MARVEL)
def generate(badass, collection):

    if collection not in [NamesCollectionsE.MARVEL]:
        click.echo()
        click.echo('Only Marvel supported now. Setting `marvel` as default.')
        collection = NamesCollectionsE.MARVEL

    sprint_name = NameGenerator(
        CollectionPicker(collection).read_collection(),
        badass
    ).choose_name()

    click.echo()
    click.echo(sprint_name)
    click.echo()
