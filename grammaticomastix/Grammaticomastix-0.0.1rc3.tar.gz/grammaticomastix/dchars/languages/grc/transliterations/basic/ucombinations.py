#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
#    DChars Copyright (C) 2012 Suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of DChars.
#    DChars is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    DChars is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with DChars.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    ❏DChars❏ : dchars/languages/grc/transliterations/basic/ucombinations.py
"""
from dchars.dchars import new_dstring
from dchars.languages.grc.dcharacter import DCharacterGRC
from dchars.languages.grc.transliterations.basic.basic import dchar__get_translit_str

import itertools

#///////////////////////////////////////////////////////////////////////////
def get_usefull_combinations():
    """
            get_usefull_combinations()

            Return a (str)string with all the usefull combinations of characters,
            i.e. only the 'interesting' characters (not punctuation if it's too simple
            by example).

            NB : this function has nothing to do with linguistic or a strict
                 approach of the language. This function allows only to get the
                 most common and/or usefull characters of the writing system.

            NB : function required by the dchars-fe project.
    """
    res = []

    dstring = new_dstring( 'grc' )()

    # base_char : we don't use the list stored in symbols.py
    # since we would lost the character's order.
    base_characters  = ( 'α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι',
                         'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ',
                         'τ', 'υ', 'φ', 'χ', 'ψ', 'ω',
                         'ϝ', 'ϗ', 'ϡ', 'ϛ', 'ϙ', )

    #-----------------------------------------------------------------------
    # (1/2) simple characters
    #-----------------------------------------------------------------------
    for base_char in base_characters:
        for capital_letter in (False, True):
            dchar = DCharacterGRC( dstring_object = dstring,
                                   base_char = base_char,
                                   contextual_form = "initial+medium+final",
                                   punctuation = False,
                                   capital_letter = capital_letter,
                                   tonos = None,
                                   pneuma = None,
                                   hypogegrammene = False,
                                   dialutika = False,
                                   mekos = None )

            txt = dchar__get_translit_str(dstring_object = dstring,
                                          dchar = dchar)

            res.append( str(dchar) + "{" + txt + "} " )

    #-----------------------------------------------------------------------
    # (2/2) complex characters
    #-----------------------------------------------------------------------
    combinations = (itertools.product(
                                       # base_chars
                                       ( 'α', ),

                                       # contextual_form
                                       ("initial", "medium", "final",
                                        "initial+medium", "medium+final",
                                        "initial+medium+final"),

                                       # capital_letter
                                       (False, True),

                                       # tonos
                                       ( None, "ὀξεῖα", "βαρεῖα", "περισπωμένη" ),

                                       # pneuma
                                       ( None, "ψιλὸν",  "δασὺ" ),

                                       # hypogegrammene
                                       (False, True),

                                       # dialutika
                                       (False, True),

                                       # mekos
                                       ( None, "βραχύ", "μακρόν" ),
                                       ))

    for base_char, contextual_form, capital_letter, \
        tonos, pneuma, hypogegrammene, dialutika, mekos in combinations:

        add_this_dchar = True

        if base_char == 'ρ':
            if contextual_form != "initial+medium+final" or \
               tonos is not None or \
               hypogegrammene == True or \
               dialutika == True or \
               mekos is not None:

                add_this_dchar = False

        elif base_char in ('β', 'σ'):
            if tonos is not None or \
               pneuma is not None or \
               hypogegrammene == True or \
               dialutika == True or \
               mekos is not None:

                add_this_dchar = False

        elif base_char in ('α', 'η', 'ω'):
            if contextual_form != "initial+medium+final" or \
               dialutika == True or \
               mekos is not None:

                add_this_dchar = False

        elif base_char in ('ε', 'ο'):
            if contextual_form != "initial+medium+final" or \
               hypogegrammene == True or \
               tonos == "περισπωμένη" or \
               hypogegrammene == True or \
               dialutika == True or \
               mekos is not None:

                add_this_dchar = False

        elif base_char in ('ι', 'υ'):
            if contextual_form != "initial+medium+final" or \
               hypogegrammene == True or \
               mekos is not None:

                add_this_dchar = False

        else:
            if contextual_form != "initial+medium+final" or \
               tonos is not None or \
               pneuma is not None or \
               hypogegrammene == True or \
               dialutika == True or \
               mekos is not None:

                add_this_dchar = False

        if add_this_dchar:
            dchar = DCharacterGRC( dstring_object = dstring,
                                   base_char = base_char,
                                   contextual_form = contextual_form,
                                   punctuation = False,
                                   capital_letter = capital_letter,
                                   tonos = tonos,
                                   pneuma = pneuma,
                                   hypogegrammene = hypogegrammene,
                                   dialutika = dialutika,
                                   mekos=mekos)

            txt = dchar__get_translit_str(dstring_object = dstring,
                                          dchar = dchar)

            res.append( str(dchar) + "{" + txt + "} " )

    return "".join(res)
