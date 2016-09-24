from ..cli import *
from ..api import *
import sys
import click
import logging


logger = logging.getLogger(__name__)


@cli.group('tail')
def tail():
    """tails events"""
