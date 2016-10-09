# -*- coding: utf-8 -*-
"""Functional way to populate trie"""
import pygtrie as trie


def __populate_trie_reducer(trie_accumulator=trie.CharTrie(), value=""):
    """Adds value to trie accumulator"""
    trie_accumulator[value] = value
    return trie_accumulator


def populate_trie(values):
    """Takes a list and inserts its elements into a new trie and returns it"""
    return reduce(__populate_trie_reducer, iter(values), trie.CharTrie())
