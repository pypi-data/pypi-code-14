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
    ❏DChars❏ : dchars/name2symbols.py

    E.g :

    .. code-block:: none

        SYMB_DIACRITICS_NAME2NUM = Name2Symbols(
        {"τόνος.βαρεῖα"          : ( chr(0x300),),        # ὰ
         "τόνος.ὀξεῖα"           : ( chr(0x301), chr(0x030D)),  # ά, α̍
         "μῆκος.μακρόν"          : ( chr(0x304),),        # ᾱ
         "μῆκος.βραχύ"           : ( chr(0x306),),        # ᾰ
         "τόνος.περισπωμένη"     : ( chr(0x342),),        # ᾶ
         "πνεῦμα.ψιλὸν"          : ( chr(0x313),),        # ἀ
         "πνεῦμα.δασὺ"           : ( chr(0x314),),        # ἁ
         "ὑπογεγραμμένη"         : ( chr(0x345),),        # ᾳ
         "διαλυτικά"             : ( chr(0x308),),        # ϋ
         })
"""
import re

################################################################################
class Name2Symbols(dict):
    """
        class Name2Symbols : associate a name with several symbols, the first
        of these symbols being the default symbol.

        E.g. : "τόνος.ὀξεῖα" : (chr(0x301), chr(0x030D))  # ά, α̍
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self, src):
        """
                Name2Symbols.__init__

                Initialize <self>, create the reversed dictionary of self (<defaultsymbol2name>)
                and initialize self.substitutions in order to speed up the function
                replace_by_the_default_symbols().
        """

        #.......................................................................
        # initialisation of the dictionary in <self> :
        #.......................................................................
        dict.__init__(self, src)

        #.......................................................................
        # creation of self.defaultsymbol2name :
        #.......................................................................
        # defaultsymbol2name[ chr(0x301) ] = "τόνος.ὀξεῖα"
        self.defaultsymbol2name = dict(zip(self.default_symbols(),
                                  self.keys()))

        #.......................................................................
        # creation of self.symbol2name :
        #.......................................................................
        self.symbol2name = dict()
        for key in self:
            for value in self[key]:
                self.symbol2name[value] = key

        #.......................................................................
        # initialisation of self.substitutions, a list used by
        # self.replace_by_the_default_symbols() :
        #.......................................................................
        self.substitutions = [] # ( (str)source, (str)dest) )
                                # <source> will be replaced by <dest> by
                                # calling self.replace_by_the_default_symbols()

        for name in self:
            for index, symbol in enumerate(self[name]):

                # if index == 0 we get the default value when in fact we want
                # fake values.
                if index == 0:
                    default_value = symbol
                else:
                    self.substitutions.append( (symbol, default_value) )

    #///////////////////////////////////////////////////////////////////////////
    def are_these_symbols_in_a_string(self, name, string):
        """
                Name2Symbols.are_these_symbols_in_a_string

                Return True if <string> contains one of the symbols defined
                in self[name].
        """
        if string is None:
            return False

        res = False

        for symbol in self[name]:
            if symbol in string:
                res = True
                break

        return res

    #///////////////////////////////////////////////////////////////////////////
    def default_symbols(self):
        """
                Name2Symbols.default_symbols

                Return all default symbols.
        """
        res = [ self.get_default_symbol(name) for name in self ]

        return res

    #///////////////////////////////////////////////////////////////////////////
    def default_symbols__pattern(self):
        """
                Name2Symbols.default_symbols__pattern

                Return all default symbols, special function for regex since
                some symbols have to be treated apart.
        """
        d_symbols = map( re.escape, self.default_symbols() )
        return list(d_symbols)

    #///////////////////////////////////////////////////////////////////////////
    def get_default_symbol(self, name):
        """
                Name2Symbols.get_default_symbol

                Return the default symbol of self[name].
        """
        return self[name][0]

    #///////////////////////////////////////////////////////////////////////////
    def replace_by_the_default_symbols(self, src):
        """
                Name2Symbols.replace_by_the_default_symbols
        """
        for substitution_src, substitution_dest in self.substitutions:
            src = src.replace( substitution_src, substitution_dest )

        return src

    #///////////////////////////////////////////////////////////////////////////
    def get_the_name_for_this_symbol(self, symbol):
        """
                Name2Symbols.get_the_name_for_this_symbol

                Return either a string either None, if symbol doesn't belong
                to self.
        """

        if symbol in self.symbol2name:
            return self.symbol2name[symbol]
        else:
            return None
