"""
Common schema definition types that should be mapped to corresponding Python objects.

Some of the primary mappings of interest include:

* the rdfs:Class type which should be mapped to Python class
* the rdfs:subClassOf property type which should be mapped to an inheritance relation

"""
from rdflib import RDF, RDFS, OWL, XSD, Literal
from six import string_types


def is_a_class(uri):
    return uri in (
        RDFS.Class,
        OWL.Class,
    )


def is_a_property(uri):
    return uri in (
        RDF.Property,
    )


def is_a_literal(uri):
    return (uri in (RDFS.Literal,) or
            uri.startswith(XSD))


def is_literal_value(value):
    return (
        isinstance(value, Literal) or
        isinstance(value, string_types)
    )


def is_comment_predicate(predicate):
    return predicate in (
        RDFS.comment,
    )


def is_domain_predicate(predicate):
    return predicate in (
        RDFS.domain,
    )


def is_label_predicate(predicate):
    return predicate in (
        RDFS.label,
    )


def is_range_predicate(predicate):
    return predicate in (
        RDFS.range,
    )


def is_type_predicate(predicate):
    return predicate in (
        RDF.type,
    )


def is_sub_class_predicate(predicate):
    return predicate in (
        RDFS.subClassOf,
        RDFS.subPropertyOf,
    )
