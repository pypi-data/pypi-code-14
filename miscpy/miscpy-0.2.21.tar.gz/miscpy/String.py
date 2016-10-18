#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Functions and classes for easier string processing.
:author: Manuel Tuschen
:license: FreeBSD

License
----------
Copyright (c) 2016, Manuel Tuschen
All rights reserved.
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


from __future__ import division, absolute_import, unicode_literals, print_function
import re


__all__ = ["hstr"]


class hstr(str):
    """
    String subclasses which compares after intuitive human behaviour if it
    contains integers, too.
    """

    def __lt__(self, other):
        seq_s = re.split('([0-9]+)', self)
        seq_o = re.split('([0-9]+)', other)

        # remove empty strings
        for i in range(seq_s.count('')):
            seq_s.remove('')
        for i in range(seq_o.count('')):
            seq_o.remove('')

        # can we already make a decision?
        # the smaller string always wins
        if len(seq_s) < len(seq_o):
            return True
        elif len(seq_o) < len(seq_s):
            return False
        else:
            # if both are ints:
            try:

                if int(seq_s[0]) < int(seq_o[0]):
                    return True
            except ValueError:
                if seq_s[0] < seq_o[0]:
                    return True
            # if one character is left for both
            if len(seq_s) == 1:
                return False

            return hstr(self.lstrip(seq_s[0])) < hstr(other.lstrip(seq_o[0]))

    def __le__(self, other):
        return not other < self

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return not self < other

    def __eq__(self, other):
        seq_s = re.split('([0-9]+)', self)
        seq_o = re.split('([0-9]+)', other)

        # remove empty strings
        for i in range(seq_s.count('')):
            seq_s.remove('')
        for i in range(seq_o.count('')):
            seq_o.remove('')

        # can we already make a decision?
        # if they have different length:
        if len(seq_s) != len(seq_o):
            return False
        # if both are ints:
        try:
            if int(seq_s[0]) != int(seq_o[0]):
                return False
        except ValueError:
            # if not
            if seq_s[0] != seq_o[0]:
                return False
        # if there is only one element left
        if len(seq_s) == 1:
            # and those are equal
            try:
                if int(seq_s[0]) == int(seq_o[0]):
                    return True
            except ValueError:
                if seq_s[0] == seq_o[0]:
                    return True
            else:
                return False
        # if there are more elements left
        else:
            return hstr(self.lstrip(seq_s[0])) == hstr(other.lstrip(seq_o[0]))

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(str(self))
