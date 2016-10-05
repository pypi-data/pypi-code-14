import json
import pygtrie as trie

def populate_trie_reducer(t=trie.CharTrie(), v=""):
    t[v] = v
    return t

def populate_trie(names):
    t = reduce(populate_trie_reducer, iter(names), trie.CharTrie())
    return t