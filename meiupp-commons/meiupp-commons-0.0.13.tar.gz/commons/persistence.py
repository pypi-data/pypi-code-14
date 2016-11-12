# encoding:utf-8
"""Persistence layer"""
from py2neo import Node, Relationship, remote
from py2neo.compat import ustr
from py2neo.util import relationship_case
from asterix import get_component
from flask import current_app


def create(label, **kwargs):
    graph = get_component("neo4j", current_app)
    node = Node(label, **kwargs)
    graph.create(node)
    return node


def get(label, unique_key, unique_value):
    graph = get_component("neo4j", current_app)
    return graph.find_one(label, unique_key, unique_value)


def get_all(label, key=None, value=None):
    graph = get_component("neo4j", current_app)
    return graph.find(label, key, value)


def get_or_create(label, unique):
    node = get(label, *unique)
    if node is None:
        node = create(label, **{unique[0]: unique[1]})
    return node


def push(subgraph):
    graph = get_component("neo4j", current_app)
    if remote(subgraph) is None:
        graph.create(subgraph)
    else:
        graph.push(subgraph)
    return subgraph


def _match(node, r, single=True, bidirectional=False):
    graph = get_component("neo4j", current_app)
    rel = (
        isinstance(r, type) and ustr(relationship_case(r.__name__))
        or isinstance(r, Relationship) and r.type()
        or r
    )
    match = getattr(graph, "match_one" if single else "match")
    return match(node, rel, bidirectional=bidirectional)


def has_relation(node, relationship):
    return _match(node, relationship) is not None


def get_related(node, relationship):
    return _match(node, relationship).end_node()


def get_all_related(node, relationship, bidirectional=False):
    return (i.end_node() for i in _match(node, relationship, False,
                                         bidirectional))


def upsert(node, **kwargs):
    for k, v in kwargs.items():
        node[k] = v

    return push(node)


def clean_upsert(node, **kwargs):
    for k in node.keys():
        del node[k]

    return upsert(node, **kwargs)
