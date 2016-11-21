# coding=utf-8
""" List of Stopwords of english
"""

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

from corefgraph.resources.lambdas import list_checker, equality_checker, matcher, fail

# List extracted from Stanford CoreNLP

stop_words = list_checker(('unas', 'una', 'unos', 'un', 'del', 'al', 'el', 'la', 'los', 'lo', 'las', 'de', 'en',
                           'sobre', 'por', 'dentro', 'hacia', 'desde', 'fuera', 'como', 'así', 'tal', 'o', 'y', 'esos',
                           'esas', 'este', 'esta', 'aquellas', 'aquellos', 'ese', 'esa', 'para', ',', 'es', 'fue',
                           'era', 'soy', 'eres', 'sido', 'eras'))

extended_stop_words = list_checker(("el", "la",  "sñr", "sñra", "dr", "ms.", "s.", "s.l.",
                                    "s.a", ",", "."))  # , "..", "..", "-", "''", '"', "-"))
# all pronouns are added to stop_word

common_NE_subfixes = list_checker(("s.a.", "s.l.", "s.a.l.", "s.l.l.", "s.c.", "s.com", "s.coop"))

non_words = list_checker(('ejem', 'ajá', 'hm', 'jo'))


_invalid = list_checker(("sa", "sl", "etc", "dólares", "pesetas", ))
invalid_words = lambda x: _invalid(x)

location_modifiers = list_checker(("norte", "sur", "este", "oeste", "arriba", "abajo"))
