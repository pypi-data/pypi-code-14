# selectionrule.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Game selection rule parser.
"""

import re

from .constants import (
    NAME_DELIMITER,
    )

_error = 1


class SelectionRule(object):
    """Game selection rule parser.

    Parse text for a game selection rule specification.
    
    """

    def __init__(self):
        """"""
        super(SelectionRule, self).__init__()

        # Support using where.Where or where_dpt.Where depending on database
        # engine being used.
        # This attribute should not be used for anything else.
        self.__database = None

        self._state = None
        self.textok = ''
        self.texterror = ''
        #self.description = '' # selection rule name displayed in record list
        self._description_string = ''
        self._selection_rule_string = ''
        self.where = None

    def extract_selection_rule(self, text, delimiter='\n'):#NAME_DELIMITER):
        """Return True if rule name and rule in text (two lines or more)."""
        # delimiter argument while database and display delimiters different
        position = [t.strip() for t in text.split(delimiter, 1)]
        if not len(position[0]):
            return False
        if len(position) == 1:
            self._description_string = position[0]
            self._selection_rule_string = ''
        else:
            self._description_string = position[0]
            self._selection_rule_string = position[1]
        return True

    def process_selection_rule(self):
        """Extract selection rule name and rules from text."""
        self._selectiontext_valid = True
        self._process_description()
        self._state = False
        self._process_selectiontext()

    def get_name_text(self):
        """Return name text."""
        return self._description_string

    def get_name_selection_rule_text(self):
        """Return name and position text."""
        return '\n'.join(
            (self._description_string,
             self._selection_rule_string,
             ))

    def get_selection_rule_text(self, delimiter=''):
        """Return position text."""
        return self._selection_rule_string

    def is_error(self):
        """Return True if parser is in error state."""
        return self._state == _error

    def is_selection_rule(self):
        """Return True if parser is in position found state."""
        return self._state == False

    def _process_description(self):
        """"""

    def _process_selectiontext(self):
        """"""
        self._set_selection_data()

    def _set_selection_data(self):
        """"""
        self.parse_selection_rule()
        self.textok = self._selection_rule_string
        self.texterror = ''

    def parse_selection_rule(self):
        """"""
        if self.__database is None:
            return
        w = self.__database.record_selector(self._selection_rule_string)

        # Maybe lex and parse later.
        w.lex()
        w.parse()
        
        self.where = w

    def set_database(self, database=None):
        """Set Database instance to which selection rule is applied."""
        self.__database = database

