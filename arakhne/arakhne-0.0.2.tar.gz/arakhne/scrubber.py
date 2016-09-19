# -*- coding: utf-8 -*-
#
# ===============
# David J. Thomas
#  thePortus.com
# ===============

import re
from collections import UserString


class Scrubber(UserString):
    """ Scrubber

    String extended with text-scrubbing methods

    Extends:
        UserString
    """

    def to_string(self):
        # Converts back to plain string
        return str(self.data)

    def remove_endlines(self):
        # Returns new instance of self with endlines removed
        return self.__class__(
            self.data
                .replace('-\n ', '').replace('- \n', '').replace('-\n', '')
                .replace(' - ', '').replace('- ', '').replace(' -', '')
                .replace('\n', ' ')
        )

    def remove_editorials(self):
        # Nested regex substitutions to remove all text between editor marks
        return self.__class__(
            re.sub("\〚(.*?)\〛", "", re.sub("\{(.*?)\}", "", re.sub(
                "\((.*?)\)", "", re.sub("\<(.*?)\>", "", re.sub(
                    "\[(.*?)\]", "", self.data)))))
        )

    def remove_numerics(self):
        # Remove all numbers from the text
        return self.__class__(re.sub("\d+", "", self.data))

    def remove_non_language(self, language='greek'):
        # Regex search and rejoin language-specific chars
        if language == 'greek':
            clean_text = "".join(re.findall("([ʹ-Ϋά-ϡἀ-ᾯᾰ-῾ ])", self.data))
        return self.__class__(clean_text)

    def remove_extra_spaces(self):
        # Setting regex compiler to blocks of whitespaces
        rexr = re.compile(r'\W+')
        clean_text = rexr.sub(' ', self.data)
        # Stripping leading/trailing spaces and returning
        return self.__class__(clean_text.strip())

    def scrub(self, language='greek'):
        # Performs all the basic operations in order to safely clean
        return (
            self.remove_endlines().remove_editorials()
            .remove_non_language(language).remove_extra_spaces().to_string()
        )
