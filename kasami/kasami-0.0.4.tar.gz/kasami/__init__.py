"""
This library contains a set of utilities for building probabilistic
context-free grammars (:class:`pcfg.TreeScorer`) from parsed sentence
trees and then using those PCFGs to score new sentence trees.
"""
from configparser import ConfigParser
import os

from .tree_scorer import TreeScorer
from .productions import Production, SymbolProduction, TerminalProduction
from .nodes import Node, SymbolNode, TerminalNode

__all__ = [TreeScorer,
           Production, SymbolProduction, TerminalProduction,
           Node, SymbolNode, TerminalNode]


def get_version(fname):
    cp = ConfigParser()
    cp.read(os.path.join(os.path.dirname(__file__), fname))
    return cp.get("VERSION", "version")

__version__ = get_version("vars.cfg")
