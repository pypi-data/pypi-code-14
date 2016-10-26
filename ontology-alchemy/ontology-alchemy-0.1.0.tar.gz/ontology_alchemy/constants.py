"""Constant definitions used by the framework."""
from rdflib import Literal
from six import string_types


# Default tag to use as a language tag for literal assigments of text strings
DEFAULT_LANGUAGE_TAG = "en"

# These are all the Python types which are considered valid to be used directly
# as assigments on Literal properties (of type rdfs:Literal)
LITERAL_PRIMITIVE_TYPES = string_types + (
    Literal,
    int,
    float,
    bool,
)
