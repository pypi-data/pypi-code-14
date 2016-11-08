# Copyright 2014-2016 Insight Software Consortium.
# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt


class elaborated_info(object):

    """

    """

    def __init__(self, elaborated):
        self._elaborated = elaborated

    @property
    def elaborated(self):
        """
        """
        return self._elaborated

    @elaborated.setter
    def elaborated(self, elaborated):
        """
        """
        self._elaborated = elaborated
