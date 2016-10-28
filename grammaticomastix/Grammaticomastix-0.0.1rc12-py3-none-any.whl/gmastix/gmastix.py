#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
#    Gmastix Copyright (C) 2016 Suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of Gmastix.
#    Gmastix is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Gmastix is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Gmastix.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    ❏Gmastix❏ : gmastix.py

    main file of the Gmastix file.

    See the main page at https://github.com/suizokukan/gmastix .
    ____________________________________________________________________________

    coding standards:
    ˮ ▶ class docstring : normal classes
    ˮ
    ˮ For each class, give the following informations :
    ˮ class attribute(s), instance attribute(s), method(s)
    ˮ Sort the elements of these three lists alphabetically.
    ˮ Specify if an element is inherited or added to the mother
    ˮ class, using the special characters ●, ◐ and ○ :
    ˮ         ● method/attribute added in comparison from parent classes (=1st definition)
    ˮ         ◐ method/attribute inherited and redifined
    ˮ         ○ method/attribute inherited and not modified
    ˮ
    ˮ For each function or method give the list of the arguments, each
    ˮ one beginning with the ▪ symbol :
    ˮ         ARGUMENTS:
    ˮ         ▪ prefix    : (str)
    ˮ         ▪ src       : (str)
    ˮ
    ˮ         RETURNED VALUE : the expected string
    ˮ
    ˮ ▶ class docstring : namedtuple classes
    ˮ
    ˮ For each class, give only the instance attribute(s).
    ˮ Sort the elements of these three lists alphabetically.
    ˮ Specify if an element is inherited or added to the mother
    ˮ class, using the special characters ●, ◐ and ○ :
    ˮ         ● method/attribute added in comparison from parent classes (=1st definition)
    ˮ         ◐ method/attribute inherited and redifined
    ˮ         ○ method/attribute inherited and not modified
    ˮ
    ˮ For each function or method give the list of the arguments, each
    ˮ one beginning with the ▪ symbol :
    ˮ         ARGUMENTS:
    ˮ         ▪ prefix    : (str)
    ˮ         ▪ src       : (str)
    ˮ
    ˮ         RETURNED VALUE : the expected string
    ˮ
    ˮ
    ˮ ▶ __init__()
    ˮ
    ˮ The arguments of an __init__() method have to be written one
    ˮ argument by line. If a __init__() method is called inside
    ˮ a __init__() method, the arguments have also to be be written
    ˮ one argument by line.

    how the Process*** and the Rhp*** classes work:
    ˮ ▪ a Rhp0 object is created with the raw input text
    ˮ
    ˮ ▪ ProcessFRA0 reads Rhp0 -- cuts the text, divides it into "words" -- and creates RhpFRA1
    ˮ ▪ ProcessFRA1 reads RhpFRA1 -- normalizes the text -- and creates RhpFRA2
    ˮ ▪ ProcessFRA2 reads RhpFRA2 -- get the morphological analysis -- and creates RhpFRA3
    ˮ ▪ ProcessFRA3 reads RhpFRA3 -- group together Pyxis into sentences -- and creates RhpFRA4
    ˮ ▪ ProcessFRA4 reads RhpFRA4 -- Pyxis1FRAword > Pyxis2FRA*** -- and creates RhpFRA5
    ˮ
    ˮ ▪ ProcessGRC0 reads Rhp0 -- cuts the text, divides it into "words" -- and creates RhpGRC1
    ˮ ▪ ProcessGRC1 reads RhpGRC1 -- normalizes the text -- and creates RhpGRC2
    ˮ ▪ ProcessGRC2 reads RhpGRC2 -- get the morphological analysis -- and creates RhpGRC3
    ˮ ▪ ProcessGRC3 reads RhpGRC3 -- group together Pyxis into sentences -- and creates RhpGRC4
    ˮ ▪ ProcessGRC4 reads RhpGRC4 -- Pyxis1GRCword > Pyxis2GRC*** -- and creates RhpGRC5
"""
import collections
import hashlib
import logging

from gmastixmorpho import gmastixmorpho
from gmastix.reportsymbols import RHP_SYMB, PROCESS_SYMB, PYXIS1_SYMB, PYXIS2_SYMB

LOGGER = logging.getLogger(__name__)

# current version of Gmastix :
VERSION = "0.2.1"

# hasher used trough out the program :
HASHER = hashlib.md5

GMORPHO = gmastixmorpho.GmastixMorpho(["fra", "grc"])
GMORPHO.enter()

# let's log various informations about the versions' numbers :
LOGGER.info("Gmastix version:"+str(VERSION))
LOGGER.info("Gmastixmorpho version: %s",
            gmastixmorpho.VERSION)
LOGGER.info(GMORPHO.infos(full_details=False))

#///////////////////////////////////////////////////////////////////////////////
def stop():
    """
        exit()
        ________________________________________________________________________

        function to be called after this module has been used.
        ________________________________________________________________________

        no ARGUMENT, no RETURNED VALUE
    """
    GMORPHO.exit()

#///////////////////////////////////////////////////////////////////////////////
def add_prefix_before_line(prefix, src):
    """
        add_prefix_before_line()
        ________________________________________________________________________

        Add the string <prefix> before every line in <src>.
        ________________________________________________________________________

        ARGUMENTS:
        ▪ prefix    : (str)
        ▪ src       : (str)

        RETURNED VALUE : the expected string
    """
    res = []
    for line in src.split("\n"):
        res.append(prefix+line)
    return "\n".join(res)

#///////////////////////////////////////////////////////////////////////////////
def colorprint(string):
    """
        colorprint() function
        ________________________________________________________________________

        Print <string> with some colors defined by the following keywords :
        ▪ "[color1]"    : red
        ▪ "[color2]"    : white
        ▪ "[color3]"    : inversed red
        ▪ "[color4]"    : inversed white
        ▪ "[default]"
        ________________________________________________________________________

        ARGUMENT:
        ▪ string : (str) the string to be displayed

        no RETURNED VALUE
    """
    string = string.replace("[color1]", "\033[0;31;1m")
    string = string.replace("[color2]", "\033[0;37;1m")
    string = string.replace("[color3]", "\033[0;31;7m")
    string = string.replace("[color4]", "\033[0;37;7m")
    string = string.replace("[default]", "\033[0m")
    print(string)

#///////////////////////////////////////////////////////////////////////////////
def hashvalue2hex(hashvalue):
    """
        hashvalue2hex()
        ________________________________________________________________________

        Convert the (bytes)hashvalue into an hex string.
        ________________________________________________________________________

        ARGUMENT:
        ▪ hashvalue : (bytes)the hashvalue to be converted

        RETURNED VALUE : the expected string
    """
    return hex(int.from_bytes(hashvalue, byteorder="big"))

#///////////////////////////////////////////////////////////////////////////////
def improve_reportstr_readibilty(src):
    """
        improve_reportstr_readibilty()
        ________________________________________________________________________

        Improve the readibilty of the (str)src so that this string may be
        easily read in a report.
        ________________________________________________________________________

        ARGUMENT:
        ▪ src   : (str) the string to be returned, slightly modified

        RETURNED VALUE : the expected (str)string.
    """
    src = src.replace(" ", "_")
    return src

################################################################################
class ColorStr(object):
    """
        ColorStr class
        ________________________________________________________________________

        Use this class to create strings with color code inside it. Use the
        __str__ method to get the full string with the color keywords. The
        color keywords are the one recognized by the colorstr() function.

        E.g. :
                | cstr = ColorStr(srcstring="0123456789",
                |                 colors={((1,2),(3,4)):"[color1]",
                |                         ((5,6),(0,1),(9,10)):"[color2]"})
                | colorprint(str(cstr))
                |

                the beginning of <cstr> being equal to :
                        "[color2]0[default][color1]1[default]2..."
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ● colors    : (dict) ((x0, x1),(y0, y1),...) : (str)color
        ● srcstring : (str) the source string

        methods :
        ● __init__(self, srcstring, colors)
        ● __repr__(self)
        ● __str__(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 srcstring,
                 colors):
        """
            ColorStr.__init__()
            ___________________________________________________________________
            ___________________________________________________________________

            no ARGUMENT, no RETURNED VALUE
        """
        self.srcstring = srcstring
        self.colors = colors

    #///////////////////////////////////////////////////////////////////////////
    def __repr__(self):
        """
            ColorStr.__repr__()
            ____________________________________________________________________

            Return a human-readable representation of self with full informations.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : the expected (str)string
        """
        return "(ColorStr) srcstring='{0}'; colors={1}".format(self.srcstring, self.colors)

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
            ColorStr.__str__()
            ____________________________________________________________________

            Return a human-readable representation of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : the expected (str)string
        """
        res = {}

        # we break the structure of self.colors :
        #
        #       ((x0, x1),(y0, y1),...) : (str)color
        #
        # into several blocks :
        #
        #       (x0, x1) : (str)color
        #       (y0, y1) : (str)color
        blocks = {}
        for list_of_x0x1 in self.colors:
            for x0x1 in list_of_x0x1:
                blocks[x0x1] = self.colors[list_of_x0x1]

        for block in sorted(blocks, reverse=True):
            res[block] = blocks[block] + \
                         "".join(self.srcstring[i] for i in range(block[0], block[1])) + \
                         "[default]"

        for posx in range(len(self.srcstring)):
            inside_a_block = False

            for block in blocks:
                if block[0] <= posx <= block[1]-1:
                    inside_a_block = True
                    break

            if not inside_a_block:
                res[(posx, posx+1)] = self.srcstring[posx]

        strres = []
        for x0x1 in sorted(res):
            strres.append(res[x0x1])
        return "".join(strres)

################################################################################
class DictHashvalueToPyxis(collections.OrderedDict):
    """
        DictHashvalueToPyxis class
        ________________________________________________________________________

        dict: (byte)hashvalue → Pyxis object

        Not a raw dict object but an OrderedDict in order to simplify the
        presentation of the data (see e.g. the report() methods using such
        a type)

        ✓ unittests : see the DictHashvalueToPyxisTest class.
        ________________________________________________________________________

        instance attribute :
        ● _hashvalue            : (None/bytes) the hash value of self computed by
                                  self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.

        methods :
        ◐ __init__(self, src=None)
        ● __str__(self)
        ● clone(self)
        ● get_hashvalue(self)
        ● set_hashvalue(self)
    """

    #///////////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 src=None):
        """
            DictHashvalueToPyxis.__init__()
            ____________________________________________________________________

            nota bene : as expected for a class with a _hashvalue attribute,
            _hashvalue is set to None in the __init__() method.
            ____________________________________________________________________

            ARGUMENT:
            ▪ src : None or a dict

            no RETURNED VALUE
        """
        if src is None:
            collections.OrderedDict.__init__(self)
        else:
            collections.OrderedDict.__init__(self, src)

        self._hashvalue = None

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
            DictHashvalueToPyxis.__str__()
            ____________________________________________________________________

            Return a human-readable representation of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : the expected (str)string
        """
        res = []
        for pyxis_hashvalue in self:
            res.append("{0}".format(self[pyxis_hashvalue]))
        return "\n".join(res)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            DictHashvalueToPyxis.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : an independent copy of self.
        """
        res = DictHashvalueToPyxis()
        for key, value in self.items():
            res[key] = value
        return res

    #///////////////////////////////////////////////////////////////////////////
    def get_hashvalue(self):
        """
            DictHashvalueToPyxis.get_hashvalue()
            ____________________________________________________________________

            Compute the value of ._hashvalue if necessary and return it.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : self._hashvalue
        """
        if self._hashvalue is None:
            self.set_hashvalue()
        return self._hashvalue

    #///////////////////////////////////////////////////////////////////////////
    def set_hashvalue(self):
        """
            DictHashvalueToPyxis.set_hashvalue()
            ____________________________________________________________________

            Initialize the value of _set_hashvalue.
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        hasher = HASHER()
        for hashvalue in self:
            hasher.update(hashvalue)
            hasher.update(self[hashvalue].get_hashvalue())
        self._hashvalue = hasher.digest()

################################################################################
class LPyHashvalues(list):
    """
        LPyHashvalues class
        ________________________________________________________________________

        a list of Pyxis' hashvalues, i.e a list of bytes.

        ✓ unittests : see the LPyHashvaluesTest class.
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ● _hashvalue            : (None/bytes) the hash value of self computed by
                                  self.sethashvalue()
                                  Use .gethashvalue() to read its value.

        methods :
        ◐ __init__(self, src=None)
        ● __str__(self)
        ● gethashvalue(self)
        ● sethashvalue(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 src=None):
        """
            LPyHashvalues.__init__()
            ____________________________________________________________________

            nota bene : as expected for a class with a _hashvalue attribute,
            _hashvalue is set to None in the __init__() method.
            ____________________________________________________________________

            ARGUMENT:
            ▪ src   : (None/list of Pyxis objects) a list of Pyxis objetcs
                      to be stored in self.

            no RETURNED VALUE
        """
        if src is None:
            list.__init__(self)
        else:
            list.__init__(self, src)

        self._hashvalue = None

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
            LPyHashvalues.__str__()
            ____________________________________________________________________

            Return a human-readable representation of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : the expected (str)string
        """
        res = []
        for hashvalue in self:
            res.append(hashvalue2hex(hashvalue))
        return "[" + "; ".join(res) + "]"

    #///////////////////////////////////////////////////////////////////////////
    def gethashvalue(self):
        """
            LPyHashvalues.gethashvalue()
            ____________________________________________________________________

            Compute the value of ._hashvalue if necessary and return it.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : self._hashvalue
        """
        if self._hashvalue is None:
            self.sethashvalue()
        return self._hashvalue

    #///////////////////////////////////////////////////////////////////////////
    def sethashvalue(self):
        """
            LPyHashvalues.sethashvalue()
            ____________________________________________________________________

            Initialize the value of _sethashvalue.
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        hasher = HASHER()
        for hashvalue in self:
            hasher.update(hashvalue)
        self._hashvalue = hasher.digest()

################################################################################
class TextPos(list):
    """
        TextPos class
        ________________________________________________________________________

        simple wrapper around a list of [startpos, endpos].

        ✓ unittests : see the TextPosTest class.
        ________________________________________________________________________

        no class attribute

        instance attribute :
        ● _hashvalue            : (None/bytes) the hash value of self computed by
                                  self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.

        methods :
        ◐ __init__(self, src=None)
        ● addx0x1(self, startpos, endpos)
        ● get_hashvalue(self)
        ● set_hashvalue(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 src=None):
        """
            TextPos.__init__()
            ____________________________________________________________________

            nota bene : as expected for a class with a _hashvalue attribute,
            _hashvalue is set to None in the __init__() method.
            ____________________________________________________________________

            ARGUMENT:
            ▪ src   (None/list of ((int)x0, (int)x1)

            no RETURNED VALUE
        """
        if src is None:
            list.__init__(self)
        else:
            list.__init__(self, src)
        self._hashvalue = None

    #///////////////////////////////////////////////////////////////////////////
    def addx0x1(self, startpos, endpos):
        """
            TextPos.addx0x1()
            ____________________________________________________________________

            Add a couple of integers (startpos, endpos) to self.
            ____________________________________________________________________

            ARGUMENTS:
            ▪ startpos      : (integer) x0
            ▪ endpos        : (integer) x1

            RETURNED VALUE : self
        """
        self.append([startpos, endpos])
        return self

    #///////////////////////////////////////////////////////////////////////////
    def get_hashvalue(self):
        """
            TextPos.get_hashvalue()
            ____________________________________________________________________

            Compute the value of ._hashvalue if necessary and return it.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : self._hashvalue
        """
        if self._hashvalue is None:
            self.set_hashvalue()
        return self._hashvalue

    #///////////////////////////////////////////////////////////////////////////
    def set_hashvalue(self):
        """
            TextPos.set_hashvalue()
            ____________________________________________________________________

            Initialize the value of _hashvalue.
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        hasher = HASHER()
        for x0x1 in self:
            startpos, endpos = x0x1
            hasher.update(str(startpos).encode())
            hasher.update(str(endpos).encode())
        self._hashvalue = hasher.digest()

################################################################################
class LCharAndTextPos(list):
    """
        LCharAndTextPos class
        ________________________________________________________________________

        Simple wrapper around a list of CharAndTextPos objects.

        ✓ unittests : see the LCharAndTextPosTest class.
        ________________________________________________________________________

        no class attribute

        no instance attribute

        methods :
        ◐ __init__(self, src=None)
        ● __str__(self)
        ● get_hashvalue(self)
        ● set_hashvalue(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 src=None):
        """
            LCharAndTextPos.__init__()
            ____________________________________________________________________

            nota bene : as expected for a class with a _hashvalue attribute,
            _hashvalue is set to None in the __init__() method.
            ____________________________________________________________________

            ARGUMENT:
            ▪ src : None or a list of CharAndTextPos objects

            no RETURNED VALUE
        """
        if src is None:
            list.__init__(self)
        else:
            list.__init__(self, src)
        self._hashvalue = None

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
            LCharAndTextPos.__str__()
            ____________________________________________________________________

            Return a human-readable representation of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : the expected (str)string
        """
        if len(self) == 0:
            return "(nothing)"

        res = []
        # cpos : a CharAndTextPos object
        for cpos in sorted(self, key=lambda cpos: cpos.textpos):
            res.append("\"{0}\"({1})".format(cpos.characters,
                                             cpos.textpos))
        return "; ".join(res)

    #///////////////////////////////////////////////////////////////////////////
    def get_hashvalue(self):
        """
            LCharAndTextPos.get_hashvalue()
            ____________________________________________________________________

            Compute the value of ._hashvalue if necessary and return it.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : self._hashvalue
        """
        if self._hashvalue is None:
            self.set_hashvalue()
        return self._hashvalue

    #///////////////////////////////////////////////////////////////////////////
    def set_hashvalue(self):
        """
            LCharAndTextPos.set_hashvalue()
            ____________________________________________________________________

            Initialize the value of _hashvalue.
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        hasher = HASHER()
        for cpos in self: # cpos : a CharAndTextPos object
            hasher.update(cpos.get_hashvalue())
        self._hashvalue = hasher.digest()

################################################################################
class CharAndTextPos(object):
    """
        CharAndTextPos class
        ________________________________________________________________________

        Use this object to store a string and its position in another string.
        simple wrapper around (str)characters + TextPos object .

        ✓ unittests : see the CharAndTextPosTest class.
        ________________________________________________________________________

        no class attribute

        instance attribute :
        ● _hashvalue    : (None/bytes) the hash value of self computed by
                          self.set_hashvalue()
                          Use .get_hashvalue() to read its value.
        ● characters    : (str) the string to be stored
        ● textpos        : (TextPos) the position of the string in the main string

        methods :
        ● __init__(self, characters, textpos)
        ● __str__(self)
        ● get_hashvalue(self)
        ● set_hashvalue(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 characters,
                 textpos):
        """
            CharAndTextPos.__init__()
            ____________________________________________________________________

            nota bene : as expected for a class with a _hashvalue attribute,
            _hashvalue is set to None in the __init__() method.
            ____________________________________________________________________

            ARGUMENTS:
            ▪ characters    : (str) the string to be stored
            ▪ textpos        : (TextPos) the position of the string in the main string

            no RETURNED VALUE
        """
        self.characters = characters
        self.textpos = textpos
        self._hashvalue = None

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
            CharAndTextPos.__str__
            ____________________________________________________________________

            Return a human-readable representation of self.
            ____________________________________________________________________

            no ARGUMENTS
            RETURNED VALUE : the expected (str)string
        """
        return "(CharAndTextPos) \"{0}\"({1})".format(self.characters, self.textpos)

    #///////////////////////////////////////////////////////////////////////////
    def get_hashvalue(self):
        """
            CharAndTextPos.get_hashvalue()
            ____________________________________________________________________

            Compute the value of ._hashvalue if necessary and return it.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : self._hashvalue
        """
        if self._hashvalue is None:
            self.set_hashvalue()
        return self._hashvalue

    #///////////////////////////////////////////////////////////////////////////
    def set_hashvalue(self):
        """
            CharAndTextPos.set_hashvalue()
            ____________________________________________________________________

            Initialize the value of _hashvalue.
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        hasher = HASHER()
        hasher.update(self.textpos.get_hashvalue())
        hasher.update(self.characters.encode())
        self._hashvalue = hasher.digest()

################################################################################
class DictStr2LBytes(dict):
    """
        DictStr2LBytes class
        ________________________________________________________________________

        Use this class to store (key, value) for (str, list of bytes).

        dict : str→list of bytes.

        ✓ unittests : see the DictStr2LBytesTest class.
        ________________________________________________________________________

        no class attribute

        no instance attribute

        methods :
        ◐ __init__(self, src=None)
        ● __str__(self)
        ● clone(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 src=None):
        """
            DictStr2LBytes.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENT:
            ▪ src : a dict of (str, list of bytes)

            no RETURNED VALUE
        """
        dict.__init__(self)
        if src is not None:
            for key, values in src.items():
                self[key] = values

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
            DictStr2LBytes.__str__()
            ____________________________________________________________________

            Return a human-readable representation of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : the expected (str)string
        """
        if len(self) == 0:
            return "(empty)"

        res = []

        for key, values in sorted(self.items()):
            res.append("{0} :".format(key))

            if len(values) == 0:
                res.append("    ()")
            else:
                for value in values:
                    res.append("    {0}".format(hashvalue2hex(value)))

        return "\n".join(res)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            DictStr2LBytes.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : an independent copy of self.
        """
        return type(self)(src=self)

################################################################################
class DI(collections.OrderedDict):
    """
        DI class (D[ictionnary] I[nformations])
        ________________________________________________________________________

        about DI:
        ˮ A simple wrapper around a dict{str:str|float|int}.
        ˮ DI is an ordered dict since the project aimed to produce exactly the
        ˮ same results whatever the system it's running on.

        ✓ unittests : see the DITest class
        ________________________________________________________________________

        no class attribute

        instance attribute :
        ● _hashvalue            : (None/bytes) the hash value of self computed
                                  by self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.

        methods :
        ◐ __init__(self, src=None)
        ● get_hashvalue(self)
        ● set_hashvalue(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 src=None):
        """
            DI.__init__()
            ____________________________________________________________________

            nota bene : as expected for a class with a _hashvalue attribute,
            _hashvalue is set to None in the __init__() method.
            ____________________________________________________________________

            ARGUMENT:
            ▪ src : (dict or None)

            no RETURNED VALUE
        """
        self._hashvalue = None

        collections.OrderedDict.__init__(self)
        if src is not None:
            # why sorting the dict ?
            #
            # about DI:
            # ˮ A simple wrapper around a dict{str:str|float|int}.
            # ˮ DI is an ordered dict since the project aimed to produce exactly the
            # ˮ same results whatever the system it's running on.
            for key, value in sorted(src.items()):
                self[key] = value

    #///////////////////////////////////////////////////////////////////////////
    def get_hashvalue(self):
        """
            DI.get_hashvalue()
            ____________________________________________________________________

            Compute the value of ._hashvalue if necessary and return it.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : self._hashvalue
        """
        if self._hashvalue is None:
            self.set_hashvalue()
        return self._hashvalue

    #///////////////////////////////////////////////////////////////////////////
    def set_hashvalue(self):
        """
            DI.set_hashvalue()
            ____________________________________________________________________

            Initialize the value of _set_hashvalue.
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        hasher = HASHER()
        for key, value in self.items():
            hasher.update(key.encode())
            hasher.update(str(value).encode())
        self._hashvalue = hasher.digest()

################################################################################
class LPyxis(list):
    """
        LPyxis class
        ________________________________________________________________________

        A simple wrapper around a list of Pyxis objects.

        ✓ unittests : see the LPyxisTest class.
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ● _hashvalue            : (None/bytes) the hash value of self computed by
                                  self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.

        methods :
        ◐ __init__(self)
        ● __str__(self)
        ● clone(self)
        ● get_hashvalue(self)
        ● report(self)
        ● set_hashvalue(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
            LPyxis.__init__()
            ____________________________________________________________________

            nota bene : as expected for a class with a _hashvalue attribute,
            _hashvalue is set to None in the __init__() method.
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE
        """
        list.__init__(self)
        self._hashvalue = None

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
            LPyxis.__str__()
            ____________________________________________________________________

            Return a human-readable representation of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a human-readable string.
        """
        if len(self) == 0:
            return "(empty LPyxis)"

        res = ["LPyxis with {0} object(s)".format(len(self))]
        for pyxis in sorted(self, key=lambda pyxis: pyxis.get_text0pos()):
            res.append(str(pyxis))

        return "\n".join(res)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            LPyxis.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        res = type(self)()
        for pyxis in self:
            res.append(pyxis.clone())
        return res

    #///////////////////////////////////////////////////////////////////////////
    def get_hashvalue(self):
        """
            LPyxis.get_hashvalue()
            ____________________________________________________________________

            Compute the value of ._hashvalue if necessary and return it.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : self._hashvalue
        """
        if self._hashvalue is None:
            self.set_hashvalue()
        return self._hashvalue

    #///////////////////////////////////////////////////////////////////////////
    def report(self, margin=""):
        """
            LPyxis.report()
            ____________________________________________________________________

            Return a string describing self in a more friendly way than
            __str__() does, including colored segments of text.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : the expected (str) string
        """
        res = []
        for pyxis in self:
            res.append(add_prefix_before_line(margin, pyxis.report()))
        return "\n".join(res)

    #///////////////////////////////////////////////////////////////////////////
    def set_hashvalue(self):
        """
            LPyxis.set_hashvalue()
            ____________________________________________________________________

            Initialize the value of _hashvalue.
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        hasher = HASHER()
        for pyxis in self:
            hasher.update(pyxis.get_hashvalue())
        self._hashvalue = hasher.digest()

################################################################################
class Pyxis(object):
    """
        Pyxis class
        ________________________________________________________________________

        Mother-class of all the Pyxis*** classes.

        about Pyxis classes:
        ˮ The Pyxis objects are boxes where informations are stored.
        ˮ
        ˮ Methods expected : read(), export(), clone(), set_hashvalue(), get_hashvalue(), __eq__()
        ˮ
        ˮ List of the (language independant) Pyxis classes:
        ˮ
        ˮ ▪ Pyxis         : mother all Pyxis*** classes
        ˮ ▪ Pyxis1        : mother all Pyxis1*** classes
        ˮ                   a box for one word, one punctuation symbol or one
        ˮ                   unknown list of characters.
        ˮ
        ˮ ▪ Pyxis1XXXword         : a Pyxis for roughly cut words
        ˮ ▪ Pyxis1XXXpunctuation  : a Pyxis for punctuation symbols
        ˮ ▪ Pyxis1XXXunknown      : a Pyxis for unknown list of characters
        ˮ
        ˮ ▪ Pyxis2        : mother of all Pyxis2*** classes
        ˮ                   abstract elements inside a proposition
        ˮ
        ˮ ▪ Pyxis2XXXng   : a Pyxis2 object for a nominal group
        ˮ ▪ Pyxis2XXXvs   : a Pyxis2 object for a verbal syntagm
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ● _hashvalue    : (None/bytes) the hash value of self computed by
                          self.set_hashvalue()
                          Use .get_hashvalue() to read its value.
        ● _text0pos     : (Textpos or None if uninitialized)
                          extract from text0 stored in self.
                          Use .get_text0pos() to read its value.
        ● language      : (str) ISO 639-3 name of the language of self,
                          "" if irrelevant.
        ● pyxisname     : (str) string describing the type of self; may be
                          equal to the classe name.

        methods :
        ● __eq__(self, other)
        ● __init__(self, language, pyxisname)
        ● get_hashvalue(self)
        ● get_text0pos(self)
        ● set_hashvalue(self) (faked method, raises an NotImplementedError)
        ● set_text0pos(self)   (faked method, raises an NotImplementedError)
        ● uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __eq__(self,
               other):
        """
            Pyxis.__eq__()
            ____________________________________________________________________

            Return true if self==other, False otherwise.
            ____________________________________________________________________

            ARGUMENT:
            ▪ other : a Pyxis object.

            RETURNED VALUE : the expected boolean
        """
        return self.get_hashvalue() != other.get_hashvalue()

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 pyxisname):
        """
            Pyxis.__init__()
            ____________________________________________________________________

            nota bene : as expected for a class with a _hashvalue attribute,
            _hashvalue is set to None in the __init__() method.
            ____________________________________________________________________

            ARGUMENTS:
            ▪ pyxisname             : (str)
            ▪ language              : (str) ISO 639-3 name of the language of
                                      self, "" if irrelevant.

            no RETURNED VALUE
        """
        self.language = language
        self.pyxisname = pyxisname

        self._hashvalue = None
        self._text0pos = None

    #///////////////////////////////////////////////////////////////////////////
    def get_hashvalue(self):
        """
            Pyxis.get_hashvalue()
            ____________________________________________________________________

            Compute the value of ._hashvalue if necessary and return it.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : self._hashvalue
        """
        if self._hashvalue is None:
            self.set_hashvalue()
        return self._hashvalue

    #///////////////////////////////////////////////////////////////////////////
    def get_text0pos(self):
        """
            Pyxis.get_text0pos()
            ____________________________________________________________________

            Compute the value of ._text0pos if necessary and return it.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : self.text0pos
        """
        if self._text0pos is None:
            self.set_text0pos()
        return self._text0pos

    #///////////////////////////////////////////////////////////////////////////
    def set_hashvalue(self):
        """
            Pyxis.set_hashvalue()
            ____________________________________________________________________

            Fake code, just here to avoid the following error from Pylint in the
            self.get_hashvalue() method :

              "Instance of 'Pyxis' has no 'set_hashvalue' member (no-member)"

            how to write a set_hashvalue() for a Pyxis class ? A set_hashvalue()
            method initializes the ._hashvalue instance attribute, hence :

                        hasher = HASHER()
                        hasher.update(self.pyxisname.encode())
                        hasher.update(self.text.encode())
                        ... several calls to hasher.update() ...
                        self._hashvalue = hasher.digest()
        """
        raise NotImplementedError

    #///////////////////////////////////////////////////////////////////////////
    def set_text0pos(self):
        """
            Pyxis.set_text0pos()
            ____________________________________________________________________

            Fake code.

            Compute the value of ._text0pos if necessary and return it.
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE
        """
        raise NotImplementedError

    #///////////////////////////////////////////////////////////////////////////
    def uniquename(self):
        """
            Pyxis.uniquename()
            ____________________________________________________________________

            (debug oriented method)
            Return a short identification of self
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : the expected string
        """
        return "{0}({1})".format(self.pyxisname,
                                 hashvalue2hex(self.get_hashvalue()))

################################################################################
class Pyxis1(Pyxis):
    """
        Pyxis1 class
        ________________________________________________________________________

        Mother-class of all the Pyxis1*** classes.

        Use Pyxis1*** objects to store informations about words, punctuation
        symbols and unknown characters.

        ✓ unittests : see the Pyxis1Test class.

        about Pyxis classes:
        ˮ The Pyxis objects are boxes where informations are stored.
        ˮ
        ˮ Methods expected : read(), export(), clone(), set_hashvalue(), get_hashvalue(), __eq__()
        ˮ
        ˮ List of the (language independant) Pyxis classes:
        ˮ
        ˮ ▪ Pyxis         : mother all Pyxis*** classes
        ˮ ▪ Pyxis1        : mother all Pyxis1*** classes
        ˮ                   a box for one word, one punctuation symbol or one
        ˮ                   unknown list of characters.
        ˮ
        ˮ ▪ Pyxis1XXXword         : a Pyxis for roughly cut words
        ˮ ▪ Pyxis1XXXpunctuation  : a Pyxis for punctuation symbols
        ˮ ▪ Pyxis1XXXunknown      : a Pyxis for unknown list of characters
        ˮ
        ˮ ▪ Pyxis2        : mother of all Pyxis2*** classes
        ˮ                   abstract elements inside a proposition
        ˮ
        ˮ ▪ Pyxis2XXXng   : a Pyxis2 object for a nominal group
        ˮ ▪ Pyxis2XXXvs   : a Pyxis2 object for a verbal syntagm
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ○ _hashvalue            : (None/bytes) the hash value of
                                  self computed by self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ● details               : (DI object)
        ○ language              : (str) ISO 639-3 name of the
                                  language of self, "" if irrelevant.
        ● punctuation_symb      : bool or None if self.recognized is set to
                                  False
        ○ pyxisname             : (str) string describing the type
                                  of self; may be equal to the classe name.
        ● recognized            : bool
        ● text                  : (str)source string

        methods :
        ◐ __eq__(self, other)
        ◐ __init__(self,
                   language, pyxisname,
                   text, _text0pos,
                   recognized, punctuation_symb,
                   details)
        ● __repr__(self)
        ● __str__(self)
        ● clone(self)
        ○ get_hashvalue(self)
        ○ get_text0pos(self)
        ◐ set_hashvalue(self)
        ○ set_text0pos(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __eq__(self,
               other):
        """
            Pyxis1.__eq__()
            ____________________________________________________________________

            Return true if self==other, False otherwise.
            ____________________________________________________________________

            ARGUMENT:
            ▪ other : a Pyxis1 object.

            RETURNED VALUE : the expected boolean
        """
        return self.get_hashvalue() == other.get_hashvalue()

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 pyxisname,
                 text,
                 _text0pos,
                 recognized,
                 punctuation_symb,
                 details):
        """
            Pyxis1.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ pyxisname             : (str)
            ▪ text                  : (str)source string
            ▪ _text0pos             : (TextPos)
            ▪ language              : (str) ISO 639-3 name of the language of
                                      self, "" if irrelevant.
            ▪ recognized            : (bool)
            ▪ punctuation_symb      : bool or None if self.recognized is set to
                                      False
            ▪ details               : dict(str:str) or a DI object

            no RETURNED VALUE
        """
        Pyxis.__init__(self,
                       language=language,
                       pyxisname=pyxisname)

        self.text = text
        self._text0pos = _text0pos
        self.recognized = recognized
        self.punctuation_symb = punctuation_symb
        self.details = DI(details)

    #///////////////////////////////////////////////////////////////////////////
    def __repr__(self):
        """
            Pyxis1.__repr__()
            ____________________________________________________________________

            Return a human-readable representation of self with full informations.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a human-readable string with all the informations
        """
        return "(Pyxis1-like object:{0}) recognized={1}; text={2}({3}); language={4}; " \
                "punctuation_symb={5}; details={6}".format(self.pyxisname,
                                                           self.recognized,
                                                           self.text,
                                                           self.get_text0pos(),
                                                           self.language,
                                                           self.punctuation_symb,
                                                           self.details)

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
            Pyxis1.__str__()
            ____________________________________________________________________

            Return a human-readable representation of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a human-readable string
        """
        if self.recognized:
            return "{0} (Pyxis1:{1}) text='{2}'({3}); language={4}; " \
                "punctuation_symb={5}; details={6}".format(PYXIS1_SYMB,
                                                           self.pyxisname,
                                                           self.text,
                                                           self.get_text0pos(),
                                                           self.language,
                                                           self.punctuation_symb,
                                                           self.details)
        else:
            return "{0} (Pyxis1:{1}) unrecognized string '{2}'".format(PYXIS1_SYMB,
                                                                       self.pyxisname,
                                                                       self.text)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis1.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        res = type(self)(language=self.language,
                         pyxisname=self.language,
                         text=self.text,
                         _text0pos=self.get_text0pos(),
                         details=self.details,
                         recognized=self.recognized,
                         punctuation_symb=self.punctuation_symb)

        return res

    #///////////////////////////////////////////////////////////////////////////
    def set_hashvalue(self):
        """
            Pyxis1.set_hashvalue()
            ____________________________________________________________________

            Initialize the value of _set_hashvalue.
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        hasher = HASHER()
        hasher.update(self.pyxisname.encode())
        hasher.update(self.text.encode())
        hasher.update(self.get_text0pos().get_hashvalue())
        hasher.update(self.language.encode())
        hasher.update(str(self.recognized).encode())
        hasher.update(str(self.punctuation_symb).encode())
        hasher.update(self.details.get_hashvalue())
        self._hashvalue = hasher.digest()

    #///////////////////////////////////////////////////////////////////////////
    def set_text0pos(self):
        """
            Pyxis1.set_text0pos()
            ____________________________________________________________________

            Initialize the value of _text0pos.

            Useless method, required by Pylint since Pyxis.set_text0pos() has to
            be overriden.
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        pass

################################################################################
class Pyxis1XXXword(Pyxis1):
    """
        Pyxis1XXXword class
        ________________________________________________________________________

        language independant class : Pyxis1 for words.

        ✓ unittests : see the Pyxis1XXXwordTest class
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ○ _hashvalue            : (None/bytes) the hash value of self computed
                                  by self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ○ details               : (DI object)
        ○ language              : (str) ISO 639-3 name of the language of self,
                                  "" if irrelevant.
        ○ punctuation_symb      : bool or None if self.recognized is
                                  set to False
        ○ pyxisname             : (str) string describing the type of self; may
                                  be equal to the classe name.
        ○ recognized            : bool
        ○ text                  : (str)source string

        methods :
        ○ __eq__(self, other)
        ◐ __init__(self,
                   language, pyxisname,
                   text, _text0pos,
                   details)
        ○ __str__(self)
        ○ __repr__(self)
        ◐ clone(self)
        ● report(self)
        ○ get_hashvalue(self)
        ○ get_text0pos(self)
        ○ set_hashvalue(self)
        ○ set_text0pos(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 pyxisname,
                 text,
                 _text0pos,
                 details):
        """
            Pyxis1XXXword.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ language              : (str) language name (ISO 639-3) or None if
                                      irrelevant
            ▪ pyxisname             : (str)
            ▪ text                  : (str) source string
            ▪ _text0pos             : (TextPos)
            ▪ details               : dict(str:str) or a DI object
            ▪ recognized            : (bool)
            ▪ punctuation_symb      : bool or None if self.recognized is set to
                                      False

            no RETURNED VALUE
        """
        Pyxis1.__init__(self,
                        language=language,
                        pyxisname=pyxisname,
                        text=text,
                        _text0pos=_text0pos,
                        recognized=True,
                        punctuation_symb=False,
                        details=details)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis1XXXword.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(language=self.language,
                          pyxisname=self.pyxisname,
                          text=self.text,
                          _text0pos=self.get_text0pos(),
                          details=self.details)

    #///////////////////////////////////////////////////////////////////////////
    def report(self, margin=""):
        """
            Pyxis1XXXword.report()
            ____________________________________________________________________

            Return a string describing self in a more friendly way than
            __str__() does, including colored segments of text.
            ____________________________________________________________________

            no ARGUMENT.

            RETURNED VALUE : a human-readable string
        """
        reportstr = "{0} \"{1}\" (word) {2} :\n    {3}".format(PYXIS1_SYMB,
                                                               self.text,
                                                               self.get_text0pos(),
                                                               self.details)
        return add_prefix_before_line(margin, reportstr)

################################################################################
class Pyxis1FRAword(Pyxis1XXXword):
    """
        Pyxis1FRAword class
        ________________________________________________________________________

        (French) Pyxis1 for a word.

        ✓ unittests : see the Pyxis1FRAwordTest class

        about Pyxis classes for French:
        ˮ ▪ Pyxis1FRAword       : (Ancient Greek) (roughly cut) "word" Pyxis1
        ˮ ▪ Pyxis1FRApunctuation: (Ancient Greek) "punctuation" Pyxis1
        ˮ ▪ Pyxis1FRAunknown    : (Ancient Greek) "unknown" Pyxis1
        ˮ
        ˮ ▪ Pyxis2FRAng   : (Ancient Greek) Pyxis2 for a nominal group.
        ˮ ▪ Pyxis2FRAvs   : (Ancient Greek) Pyxis2 for a verbal syntagm
        ˮ
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ○ _hashvalue            : (None/bytes) the hash value of self computed
                                  by self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ○ details               : (DI object)
        ○ language              : (str) ISO 639-3 name of the language of self,
                                  "" if irrelevant.
        ○ punctuation_symb      : bool or None if self.recognized is
                                  set to False
        ○ pyxisname             : (str) string describing the type of self; may
                                  be equal to the classe name.
        ○ recognized            : bool
        ○ text                  : (str)source string

        methods :
        ○ __eq__(self, other)
        ◐ __init__(self,
                   text, _text0pos, details)
        ○ __str__(self)
        ○ __repr__(self)
        ◐ clone(self)
        ○ report(self)
        ○ get_hashvalue(self)
        ○ get_text0pos(self)
        ○ set_hashvalue(self)
        ○ set_text0pos(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 text,
                 _text0pos,
                 details):
        """
            Pyxis1FRAword.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ text                  : (str) source string
            ▪ _text0pos             : (TextPos)
            ▪ details               : dict(str:str) or a DI object

            no RETURNED VALUE
        """
        Pyxis1XXXword.__init__(self,
                               text=text,
                               _text0pos=_text0pos,
                               details=details,
                               language="fra",
                               pyxisname="Pyxis1FRAword")

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis1FRAwordord.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(text=self.text,
                          _text0pos=self.get_text0pos(),
                          details=self.details)

################################################################################
class Pyxis1XXXpunctuation(Pyxis1):
    """
        Pyxis1XXXpunctuation class
        ________________________________________________________________________

        language independant class : Pyxis1 for punctuation symbols.

        ✓ unittests : see the Pyxis1XXXpunctuation class

        about Pyxis classes:
        ˮ The Pyxis objects are boxes where informations are stored.
        ˮ
        ˮ Methods expected : read(), export(), clone(), set_hashvalue(), get_hashvalue(), __eq__()
        ˮ
        ˮ List of the (language independant) Pyxis classes:
        ˮ
        ˮ ▪ Pyxis         : mother all Pyxis*** classes
        ˮ ▪ Pyxis1        : mother all Pyxis1*** classes
        ˮ                   a box for one word, one punctuation symbol or one
        ˮ                   unknown list of characters.
        ˮ
        ˮ ▪ Pyxis1XXXword         : a Pyxis for roughly cut words
        ˮ ▪ Pyxis1XXXpunctuation  : a Pyxis for punctuation symbols
        ˮ ▪ Pyxis1XXXunknown      : a Pyxis for unknown list of characters
        ˮ
        ˮ ▪ Pyxis2        : mother of all Pyxis2*** classes
        ˮ                   abstract elements inside a proposition
        ˮ
        ˮ ▪ Pyxis2XXXng   : a Pyxis2 object for a nominal group
        ˮ ▪ Pyxis2XXXvs   : a Pyxis2 object for a verbal syntagm
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ○ _hashvalue            : (None/bytes) the hash value of self computed
                                  by self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ○ details               : (DI object)
        ○ language              : (str) ISO 639-3 name of the
                                  language of self, "" if irrelevant.
        ○ pyxisname             : (str) string describing the type of self; may
                                  be equal to the classe name.
        ○ recognized            : bool
        ○ text                  : (str) source string

        methods :
        ○ __eq__(self, other)
        ◐ __init__(self, language, pyxisname, text, _text0pos, details)
        ○ __str__(self)
        ○ __repr__(self)
        ◐ clone(self)
        ● report(self)
        ○ get_hashvalue(self)
        ○ get_text0pos(self)
        ○ set_hashvalue(self)
        ○ set_text0pos(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 pyxisname,
                 text,
                 _text0pos,
                 details):
        """
            Pyxis1XXXpunctuation.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ language              : (str) language name (ISO 639-3) or None if
                                      irrelevant
            ▪ pyxisname             : (str)
            ▪ text                  : (str) source string
            ▪ _text0pos             : (TextPos)
            ▪ details               : dict(str:str) or a DI object

            no RETURNED VALUE
        """
        Pyxis1.__init__(self,
                        language=language,
                        pyxisname=pyxisname,
                        text=text,
                        _text0pos=_text0pos,
                        recognized=True,
                        punctuation_symb=True,
                        details=details)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis1XXXpunctuation.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(language=self.language,
                          pyxisname=self.pyxisname,
                          text=self.text,
                          _text0pos=self.get_text0pos(),
                          details=self.details)

    #///////////////////////////////////////////////////////////////////////////
    def report(self, margin=""):
        """
            Pyxis1XXXpunctuation.report()
            ____________________________________________________________________

            Return a string describing self in a more friendly way than
            __str__() does, including colored segments of text.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a human-readable string
        """
        reportstr = "{0} \"{1}\" (punctuation) {2} :\n    {3}".format(PYXIS1_SYMB,
                                                                      self.text,
                                                                      self.get_text0pos(),
                                                                      self.details)
        return add_prefix_before_line(margin, reportstr)

################################################################################
class Pyxis1FRApunctuation(Pyxis1XXXpunctuation):
    """
        Pyxis1FRApunctuation class
        ________________________________________________________________________

        (French) Pyxis1 for a punctuation symbol.

        ✓ unittests : see the Pyxis1FRApunctuationTest class.

        about Pyxis classes for French:
        ˮ ▪ Pyxis1FRAword       : (Ancient Greek) (roughly cut) "word" Pyxis1
        ˮ ▪ Pyxis1FRApunctuation: (Ancient Greek) "punctuation" Pyxis1
        ˮ ▪ Pyxis1FRAunknown    : (Ancient Greek) "unknown" Pyxis1
        ˮ
        ˮ ▪ Pyxis2FRAng   : (Ancient Greek) Pyxis2 for a nominal group.
        ˮ ▪ Pyxis2FRAvs   : (Ancient Greek) Pyxis2 for a verbal syntagm
        ˮ
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ○ _hashvalue            : (None/bytes) the hash value of self computed
                                  by self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ○ details               : (DI object)
        ○ language              : (str) ISO 639-3 name of the
                                  language of self, "" if irrelevant.
        ○ punctuation_symb      : bool or None if self.recognized is set to
                                  False
        ○ pyxisname             : (str) string describing the type of self; may
                                  be equal to the classe name.
        ○ recognized            : bool
        ○ text                  : (str) source string

        methods :
        ○ __eq__(self, other)
        ◐ __init__(self, text, _text0pos, details)
        ○ __str__(self)
        ○ __repr__(self)
        ◐ clone(self)
        ○ report(self)
        ○ get_hashvalue(self)
        ○ get_text0pos(self)
        ○ set_hashvalue(self)
        ○ set_text0pos(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 text,
                 _text0pos,
                 details):
        """
            Pyxis1FRApunctuation.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ text                  : (str) source string
            ▪ _text0pos             : (TextPos)
            ▪ details               : dict(str:str) or a DI object

            no RETURNED VALUE
        """
        Pyxis1XXXpunctuation.__init__(self,
                                      language="fra",
                                      pyxisname="Pyxis1FRApunctuation",
                                      text=text,
                                      _text0pos=_text0pos,
                                      details=details)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis1XXXpunctuation.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(text=self.text,
                          _text0pos=self.get_text0pos(),
                          details=self.details)

################################################################################
class Pyxis1XXXunknown(Pyxis1):
    """
        Pyxis1XXXunknown class
        ________________________________________________________________________

        language independant class : Pyxis1 for a list of unknown characters.

        ✓ unittests : see the Pyxis1XXXunknown class

        about Pyxis classes:
        ˮ The Pyxis objects are boxes where informations are stored.
        ˮ
        ˮ Methods expected : read(), export(), clone(), set_hashvalue(), get_hashvalue(), __eq__()
        ˮ
        ˮ List of the (language independant) Pyxis classes:
        ˮ
        ˮ ▪ Pyxis         : mother all Pyxis*** classes
        ˮ ▪ Pyxis1        : mother all Pyxis1*** classes
        ˮ                   a box for one word, one punctuation symbol or one
        ˮ                   unknown list of characters.
        ˮ
        ˮ ▪ Pyxis1XXXword         : a Pyxis for roughly cut words
        ˮ ▪ Pyxis1XXXpunctuation  : a Pyxis for punctuation symbols
        ˮ ▪ Pyxis1XXXunknown      : a Pyxis for unknown list of characters
        ˮ
        ˮ ▪ Pyxis2        : mother of all Pyxis2*** classes
        ˮ                   abstract elements inside a proposition
        ˮ
        ˮ ▪ Pyxis2XXXng   : a Pyxis2 object for a nominal group
        ˮ ▪ Pyxis2XXXvs   : a Pyxis2 object for a verbal syntagm
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ○ _hashvalue            : (None/bytes) the hash value of self computed
                                  by self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ○ details               : (DI object)
        ○ language              : (str) ISO 639-3 name of the
                                  language of self, "" if irrelevant.
        ○ punctuation_symb      : bool or None if self.recognized is set to
                                  False
        ○ pyxisname             : (str) string describing the type of self; may
                                  be equal to the classe name.
        ○ recognized            : bool
        ○ text                  : (str) source string

        methods :
        ○ __eq__(self, other)
        ◐ __init__(self, language, pyxisname, text, _text0pos, details)
        ○ __str__(self)
        ○ __repr__(self)
        ◐ clone(self)
        ● report(self)
        ○ get_hashvalue(self)
        ○ get_text0pos(self)
        ○ set_hashvalue(self)
        ○ set_text0pos(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 pyxisname,
                 text,
                 _text0pos,
                 details):
        """
            Pyxis1XXXunknown.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ language              : (str) language name (ISO 639-3) or None if
                                      irrelevant
            ▪ pyxisname             : (str)
            ▪ text                  : (str) source string
            ▪ _text0pos             : (TextPos)
            ▪ punctuation_symb      : bool or None if self.recognized is set to
                                      False
            ▪ details               : dict(str:str) or a DI object

            no RETURNED VALUE
        """
        Pyxis1.__init__(self,
                        language=language,
                        pyxisname=pyxisname,
                        text=text,
                        _text0pos=_text0pos,
                        recognized=False,
                        punctuation_symb=None,
                        details=details)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis1XXXpunctuation.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(language=self.language,
                          pyxisname=self.pyxisname,
                          text=self.text,
                          _text0pos=self.get_text0pos(),
                          details=self.details)

    #///////////////////////////////////////////////////////////////////////////
    def report(self, margin=""):
        """
            Pyxis1XXXunknown.report()
            ____________________________________________________________________

            Return a string describing self in a more friendly way than
            __str__() does, including colored segments of text.
            ____________________________________________________________________

            RETURNED VALUE : a human-readable string
        """
        reportstr = "{0} \"{1}\" (undefined) {2}".format(PYXIS1_SYMB,
                                                         self.text,
                                                         self.get_text0pos())
        return add_prefix_before_line(margin, reportstr)

################################################################################
class Pyxis1FRAunknown(Pyxis1XXXunknown):
    """
        Pyxis1FRAunknown class
        ________________________________________________________________________

        (French) Pyxis1 for a list of unrecognized characters.

        ✓ unittests : see the Pyxis1FRAunknownTest class.

        about Pyxis classes for French:
        ˮ ▪ Pyxis1FRAword       : (Ancient Greek) (roughly cut) "word" Pyxis1
        ˮ ▪ Pyxis1FRApunctuation: (Ancient Greek) "punctuation" Pyxis1
        ˮ ▪ Pyxis1FRAunknown    : (Ancient Greek) "unknown" Pyxis1
        ˮ
        ˮ ▪ Pyxis2FRAng   : (Ancient Greek) Pyxis2 for a nominal group.
        ˮ ▪ Pyxis2FRAvs   : (Ancient Greek) Pyxis2 for a verbal syntagm
        ˮ
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ○ _hashvalue            : (None/bytes) the hash value of self computed
                                  by self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ○ details               : (DI object)
        ○ language              : (str) ISO 639-3 name of the language of self,
                                  "" if irrelevant.
        ○ punctuation_symb      : bool or None if self.recognized is set to
                                  False
        ○ pyxisname             : (str) string describing the type of self; may
                                  be equal to the classe name.
        ○ recognized            : bool
        ○ text                  : (str)source string

        methods :
        ○ __eq__(self, other)
        ◐ __init__(self,
                   text, _text0pos, details=DI())
        ○ __str__(self)
        ○ __repr__(self)
        ◐ clone(self)
        ○ report(self)
        ○ get_hashvalue(self)
        ○ get_text0pos(self)
        ○ set_hashvalue(self)
        ○ set_text0pos(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 text,
                 _text0pos,
                 details=None):
        """
            Pyxis1FRAunknown.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ text                   : (str)source string
            ▪ _text0pos                : (TextPos)
            ▪ details                : None(=DI()) or dict(str:str) or a DI object

            no RETURNED VALUE
        """
        if details is None:
            details = DI()

        Pyxis1XXXunknown.__init__(self,
                                  text=text,
                                  _text0pos=_text0pos,
                                  details=details,
                                  language="fra",
                                  pyxisname="Pyxis1FRAunknown")

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis1FRAunknown.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(text=self.text,
                          _text0pos=self.get_text0pos(),
                          details=self.details)

################################################################################
class Pyxis2(Pyxis):
    """
        Pyxis2 class
        ________________________________________________________________________

        Mother-class of all the Pyxis2*** classes.

        Use Pyxis2*** objects to transform a (Pyxis1) word object into something
        grammatically more abstract : the abstract elements inside a
        proposition.

        ✓ unittests : see the Pyxis2Test class.

        about Pyxis classes:
        ˮ The Pyxis objects are boxes where informations are stored.
        ˮ
        ˮ Methods expected : read(), export(), clone(), set_hashvalue(), get_hashvalue(), __eq__()
        ˮ
        ˮ List of the (language independant) Pyxis classes:
        ˮ
        ˮ ▪ Pyxis         : mother all Pyxis*** classes
        ˮ ▪ Pyxis1        : mother all Pyxis1*** classes
        ˮ                   a box for one word, one punctuation symbol or one
        ˮ                   unknown list of characters.
        ˮ
        ˮ ▪ Pyxis1XXXword         : a Pyxis for roughly cut words
        ˮ ▪ Pyxis1XXXpunctuation  : a Pyxis for punctuation symbols
        ˮ ▪ Pyxis1XXXunknown      : a Pyxis for unknown list of characters
        ˮ
        ˮ ▪ Pyxis2        : mother of all Pyxis2*** classes
        ˮ                   abstract elements inside a proposition
        ˮ
        ˮ ▪ Pyxis2XXXng   : a Pyxis2 object for a nominal group
        ˮ ▪ Pyxis2XXXvs   : a Pyxis2 object for a verbal syntagm
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ○ _hashvalue            : (None/bytes) the hash value of self computed by
                                  self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ● _text0reportstr       : (str) report str of the extract from text0
                                  to be initialized by Rhp***.set_text0reportstr()
                                  to be used by the Pyxis***.__str__() methods
        ● _type                 : (str) "word" | "punctuation" | "unknown"
                                  Don't read directly _type : instead, use the
                                  .is_a_word(), .is_unknown(),
                                  .is_a_punctuation_symbol()
        ● details               : (DI object)
        ○ language              : (str) ISO 639-3
        ○ pyxisname             : (str) string describing the type of self; may
                                  be equal to the classe name.
        ● subpyxis              : list of the Pyxis that compose self.

        methods :
        ◐ __eq__(self, other)
        ◐ __init__(self,
                   language, pyxisname, _text0pos, details,
                   subpyxis=None,
                   _text0reportstr="")
        ● __repr__(self)
        ● __str__(self)
        ● add_a_subpyxis(self, pyxis)
        ● clone(self)
        ○ get_hashvalue(self)
        ◐ get_text0pos(self)
        ● is_a_punctuation_symbol(self)
        ● is_a_space(self)
        ● is_a_word(self)
        ● is_unknown(self)
        ● report(self)              (faked method, raises an NotImplementedError)
        ◐ set_hashvalue(self)
        ◐ set_text0pos(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __eq__(self,
               other):
        """
            Pyxis2.__eq__()
            ____________________________________________________________________

            Return true if self==other, False otherwise.
            ____________________________________________________________________

            ARGUMENT:
            ▪ other : a Pyxis2 object.

            RETURNED VALUE : the expected boolean
        """
        return self.get_hashvalue() == other.get_hashvalue()

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 pyxisname,
                 details,
                 subpyxis=None,
                 _text0reportstr="",
                 _type="word"):
        """
            Pyxis2.__init__()
            ____________________________________________________________________

            nota bene : as expected for a class with a _hashvalue attribute,
            _hashvalue is set to None in the __init__() method.
            ____________________________________________________________________

            ARGUMENTS
            ▪ language              : (str) ISO 639-3
            ▪ pyxisname             : (str)
            ▪ details               : (DI object)
            ▪ _text0reportstr       : (str) corresponding extract from text0
                                      to be initialized by Rhp***.set_text0reportstr()
                                      to be used by the Pyxis***.__str__() methods
            ▪ _type                 : (str) "word" | "punctuation" | "unknown"

            no RETURNED VALUE.
        """
        Pyxis.__init__(self,
                       language=language,
                       pyxisname=pyxisname)

        if subpyxis is None:
            self.subpyxis = []
        else:
            self.subpyxis = subpyxis

        self.details = details
        self.language = language
        self._text0reportstr = _text0reportstr
        self._type = _type

    #///////////////////////////////////////////////////////////////////////////
    def __repr__(self):
        """
            Pyxis2.__repr__()
            ____________________________________________________________________

            Return a human-readable representation of self with full informations.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a human-readable string with all the informations
        """
        return "(Pyxis2-like object:{0}, _type={1}) text={2}; language={3}; " \
               "_text0reportstr={4}; details={5}; subpyxis={6}".format(self.pyxisname,
                                                                       self._type,
                                                                       self.get_text0pos(),
                                                                       self.language,
                                                                       self._text0reportstr,
                                                                       self.details,
                                                                       self.subpyxis)

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
            Pyxis2.__str__()
            ____________________________________________________________________

            Return a human-readable representation of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a human-readable string
        """
        return "{0}({1}) \"{2}\" {3} ({4}) :\n    _text0pos={5}; " \
               "details={6} subpyxis={7}".format(PYXIS2_SYMB,
                                                 self._type,
                                                 self._text0reportstr,
                                                 hashvalue2hex(self.get_hashvalue()),
                                                 self.pyxisname,
                                                 self.get_text0pos(),
                                                 self.details,
                                                 self.subpyxis)

    #///////////////////////////////////////////////////////////////////////////
    def add_a_subpyxis(self, pyxis):
        """
            Pyxis2.add_a_subpyxis
            ____________________________________________________________________

            Add <pyxis> as a subpyxis to self.
            ____________________________________________________________________

            ARGUMENT :
            ▪ pyxis : a Pyxis object

            no RETURNED VALUE
        """
        self.subpyxis.append(pyxis)

        if self._text0pos is None:
            self._text0pos = TextPos()
        self._text0pos.extend(pyxis.get_text0pos())

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis2.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        res = type(self)(pyxisname=self.pyxisname,
                         details=self.details,
                         language=self.language,
                         _text0reportstr=self._text0reportstr,
                         subpyxis=self.subpyxis,
                         _type=self._type)
        return res

    #///////////////////////////////////////////////////////////////////////////
    def get_text0pos(self):
        """
            Pyxis2.get_text0pos()
            ____________________________________________________________________

            Compute the value of ._text0pos if necessary and return it.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : self._text0pos
        """
        if self._text0pos is None:
            self.set_text0pos()
        return self._text0pos

    #///////////////////////////////////////////////////////////////////////////
    def is_a_punctuation_symbol(self):
        """
            Pyxis2.is_a_punctuation_symbol()
            ____________________________________________________________________

            Return true if self._type is set to "punctuation", False otherwise.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : the expected boolean
        """
        return self._type == "punctuation"

    #///////////////////////////////////////////////////////////////////////////
    def is_a_space(self):
        """
            Pyxis2.is_a_punctuation_symbol()
            ____________________________________________________________________

            Return true if self._type is set to "punctuation" and if self
            has been defined in .details as "space".
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : the expected boolean
        """
        return self.is_a_punctuation_symbol() and \
               self.details["@punctuation type"] == "space"

    #///////////////////////////////////////////////////////////////////////////
    def is_a_word(self):
        """
            Pyxis2.is_a_word()
            ____________________________________________________________________

            Return true if self._type is set to "word", False otherwise.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : the expected boolean
        """
        return self._type == "word"

    #///////////////////////////////////////////////////////////////////////////
    def is_unknown(self):
        """
            Pyxis2.is_unknown()
            ____________________________________________________________________

            Return true if self._type is set to "unknown", False otherwise.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : the expected boolean
        """
        return self._type == "unknown"

    #///////////////////////////////////////////////////////////////////////////
    def report(self, report=""):
        """
            Pyxis2.report()
            ____________________________________________________________________

            Return a string describing self in a more friendly way than
            __str__() does, including colored segments of text.
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE
        """
        raise NotImplementedError

    #///////////////////////////////////////////////////////////////////////////
    def set_hashvalue(self):
        """
            Pyxis2.set_hashvalue()
            ____________________________________________________________________

            Initialize the value of _hashvalue.
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        hasher = HASHER()
        hasher.update(self.pyxisname.encode())
        hasher.update(self.get_text0pos().get_hashvalue())
        hasher.update(self.language.encode())
        hasher.update(self.details.get_hashvalue())
        for pyxis in self.subpyxis:
            hasher.update(pyxis.get_hashvalue())
        hasher.update(self._type.encode())

        self._hashvalue = hasher.digest()

    #///////////////////////////////////////////////////////////////////////////
    def set_text0pos(self):
        """
            Pyxis2.set_text0pos()
            ____________________________________________________________________

            Initialize the value of _text0pos.
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        self._text0pos = TextPos()
        for pyxis in self.subpyxis:
            self._text0pos.extend(pyxis.get_text0pos())

################################################################################
class Pyxis2XXXng(Pyxis2):
    """
        Pyxis2XXXng class
        ________________________________________________________________________

        Pyxis2n[ominal]g[roup] : a Pyxis2 object for a nominal group

        ✓ unittests : see the Pyxis2XXXngTest class.

        about Pyxis classes:
        ˮ The Pyxis objects are boxes where informations are stored.
        ˮ
        ˮ Methods expected : read(), export(), clone(), set_hashvalue(), get_hashvalue(), __eq__()
        ˮ
        ˮ List of the (language independant) Pyxis classes:
        ˮ
        ˮ ▪ Pyxis         : mother all Pyxis*** classes
        ˮ ▪ Pyxis1        : mother all Pyxis1*** classes
        ˮ                   a box for one word, one punctuation symbol or one
        ˮ                   unknown list of characters.
        ˮ
        ˮ ▪ Pyxis1XXXword         : a Pyxis for roughly cut words
        ˮ ▪ Pyxis1XXXpunctuation  : a Pyxis for punctuation symbols
        ˮ ▪ Pyxis1XXXunknown      : a Pyxis for unknown list of characters
        ˮ
        ˮ ▪ Pyxis2        : mother of all Pyxis2*** classes
        ˮ                   abstract elements inside a proposition
        ˮ
        ˮ ▪ Pyxis2XXXng   : a Pyxis2 object for a nominal group
        ˮ ▪ Pyxis2XXXvs   : a Pyxis2 object for a verbal syntagm
        ________________________________________________________________________

        no class attribute

        instance attributes:
        ○ _hashvalue            : (None/bytes) the hash value of self computed by
                                  self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ○ _text0reportstr       : (str) report str of the extract from text0
                                  to be initialized by Rhp***.set_text0reportstr()
                                  to be used by the Pyxis***.__str__() methods
        ○ _type                 : (str) "word" | "punctuation" | "unknown"
                                  Don't read directly _type : instead, use the
                                  .is_a_word(), .is_unknown(),
                                  .is_a_punctuation_symbol()
        ○ details               : (DI object)
        ○ language              : (str) ISO 639-3
        ○ pyxisname             : (str)
        ○ subpyxis              : list of the Pyxis that compose self.

        methods :
        ◐ __init__(self, language, pyxisname,
                   subpyxis=None,
                   details, _text0reportstr="")
        ○ __repr__(self)
        ○ __str__(self)
        ○ add_a_subpyxis(self, pyxis)
        ◐ clone(self)
        ○ get_hashvalue(self)
        ○ get_text0pos(self)
        ○ is_a_punctuation_symbol(self)
        ○ is_a_space(self)
        ○ is_a_word(self)
        ○ is_unknown(self)
        ○ set_hashvalue(self)
        ○ set_text0pos(self)
        ◐ report(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 pyxisname,
                 details,
                 subpyxis=None,
                 _text0reportstr=""):
        """
            Pyxis2XXXng.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ language              : (str) ISO 639-3
            ▪ pyxisname             : (str)
            ▪ details               : dict(str:str) or a DI object
            ▪ subpyxis              : None(empty list) or a list of Pyxis***
                                      objects
            ▪ _text0reportstr       : (str) corresponding extract from text0
                                      to be initialized by Rhp***.set_text0reportstr()
                                      to be used by the Pyxis***.__str__() methods

            no RETURNED VALUE
        """
        Pyxis2.__init__(self,
                        language=language,
                        pyxisname=pyxisname,
                        details=details,
                        subpyxis=subpyxis,
                        _text0reportstr=_text0reportstr,
                        _type="word")

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis2XXXng.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(language=self.language,
                          pyxisname=self.pyxisname,
                          details=self.details,
                          _text0reportstr=self._text0reportstr,
                          subpyxis=self.subpyxis)

    #///////////////////////////////////////////////////////////////////////////
    def report(self, margin=""):
        """
            Pyxis2XXXng.report()
            ____________________________________________________________________

            Return a string describing self in a more friendly way than
            __str__() does, including colored segments of text.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a human-readable string
        """
        res = []

        res.append("{0} \"{1}\" (nominal group) {2}:".format(PYXIS2_SYMB,
                                                             self._text0reportstr,
                                                             self.get_text0pos()))
        res.append("    {0}".format(self.details))

        for pyxis in self.subpyxis:
            res.append("    {0}".format(pyxis.report(margin=" ")))

        return add_prefix_before_line(margin, "\n".join(res))

################################################################################
class Pyxis2FRAng(Pyxis2XXXng):
    """
        Pyxis2FRAng class
        ________________________________________________________________________

        (French) Pyxis2 for a nominal group.

        ✓ unittests : see the Pyxis2FRAngTest class.

        about Pyxis classes for French:
        ˮ ▪ Pyxis1FRAword       : (Ancient Greek) (roughly cut) "word" Pyxis1
        ˮ ▪ Pyxis1FRApunctuation: (Ancient Greek) "punctuation" Pyxis1
        ˮ ▪ Pyxis1FRAunknown    : (Ancient Greek) "unknown" Pyxis1
        ˮ
        ˮ ▪ Pyxis2FRAng   : (Ancient Greek) Pyxis2 for a nominal group.
        ˮ ▪ Pyxis2FRAvs   : (Ancient Greek) Pyxis2 for a verbal syntagm
        ˮ
        ________________________________________________________________________

        no class attribute

        instance attributes:
        ○ _hashvalue            : (None/bytes) the hash value of self computed by
                                  self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ○ _text0reportstr       : (str) report str of the extract from text0
                                  to be initialized by Rhp***.set_text0reportstr()
                                  to be used by the Pyxis***.__str__() methods
        ○ _type                 : (str) "word" | "punctuation" | "unknown"
                                  Don't read directly _type : instead, use the
                                  .is_a_word(), .is_unknown(),
                                  .is_a_punctuation_symbol()
        ○ details               : (DI object)
        ○ language              : (str) ISO 639-3
        ○ pyxisname             : (str)
        ○ subpyxis              : list of the Pyxis that compose self.

        methods :
        ◐ __init__(self,
                   subpyxis=None,
                   details, _text0reportstr="")
        ○ __repr__(self)
        ○ __str__(self)
        ○ add_a_subpyxis(self, pyxis)
        ◐ clone(self)
        ○ get_hashvalue(self)
        ○ get_text0pos(self)
        ○ is_a_punctuation_symbol(self)
        ○ is_a_space(self)
        ○ is_a_word(self)
        ○ is_unknown(self)
        ○ report(self)
        ○ set_hashvalue(self)
        ○ set_text0pos(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 details,
                 subpyxis=None,
                 _text0reportstr=""):
        """
            Pyxis2FRAng.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ details               : dict(str:str) or a DI object
            ▪ subpyxis              : None(empty list) or a list of Pyxis***
                                      objects
            ▪ _text0reportstr       : (str) corresponding extract from text0
                                      to be initialized by Rhp***.set_text0reportstr()
                                      to be used by the Pyxis***.__str__() methods

            no RETURNED VALUE
        """
        Pyxis2XXXng.__init__(self,
                             language="fra",
                             pyxisname="Pyxis2FRAng",
                             details=details,
                             subpyxis=subpyxis,
                             _text0reportstr=_text0reportstr)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis2XXXng.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(details=self.details,
                          subpyxis=self.subpyxis,
                          _text0reportstr=self._text0reportstr)

################################################################################
class Pyxis2XXXvs(Pyxis2):
    """
        Pyxis2XXXvs class
        ________________________________________________________________________

        Pyxis2v[erbal]s[syntagm] : a Pyxis2 object for a verbal syntagm

        ✓ unittests : see the Pyxis2XXXvsTest class.

        about Pyxis classes:
        ˮ The Pyxis objects are boxes where informations are stored.
        ˮ
        ˮ Methods expected : read(), export(), clone(), set_hashvalue(), get_hashvalue(), __eq__()
        ˮ
        ˮ List of the (language independant) Pyxis classes:
        ˮ
        ˮ ▪ Pyxis         : mother all Pyxis*** classes
        ˮ ▪ Pyxis1        : mother all Pyxis1*** classes
        ˮ                   a box for one word, one punctuation symbol or one
        ˮ                   unknown list of characters.
        ˮ
        ˮ ▪ Pyxis1XXXword         : a Pyxis for roughly cut words
        ˮ ▪ Pyxis1XXXpunctuation  : a Pyxis for punctuation symbols
        ˮ ▪ Pyxis1XXXunknown      : a Pyxis for unknown list of characters
        ˮ
        ˮ ▪ Pyxis2        : mother of all Pyxis2*** classes
        ˮ                   abstract elements inside a proposition
        ˮ
        ˮ ▪ Pyxis2XXXng   : a Pyxis2 object for a nominal group
        ˮ ▪ Pyxis2XXXvs   : a Pyxis2 object for a verbal syntagm
        ________________________________________________________________________

        no class attribute

        instance attributes:
        ○ _hashvalue            : (None/bytes) the hash value of self computed by
                                  self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ○ _text0reportstr       : (str) report str of the extract from text0
                                  to be initialized by Rhp***.set_text0reportstr()
                                  to be used by the Pyxis***.__str__() methods
        ○ _type                 : (str) "word" | "punctuation" | "unknown"
                                  Don't read directly _type : instead, use the
                                  .is_a_word(), .is_unknown(),
                                  .is_a_punctuation_symbol()
        ○ details               : (DI object)
        ○ language              : (str) ISO 639-3
        ○ pyxisname             : (str)
        ○ subpyxis              : list of the Pyxis that compose self.

        methods :
        ◐ __init__(self,
                   language, pyxisname,
                   subpyxis=None,
                   details, _text0reportstr="")
        ○ __repr__(self)
        ○ __str__(self)
        ○ add_a_subpyxis(self, pyxis)
        ◐ clone(self)
        ○ get_hashvalue(self)
        ○ get_text0pos(self)
        ○ is_a_punctuation_symbol(self)
        ○ is_a_space(self)
        ○ is_a_word(self)
        ○ is_unknown(self)
        ◐ report(self)
        ○ set_hashvalue(self)
        ○ set_text0pos(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 pyxisname,
                 details,
                 subpyxis=None,
                 _text0reportstr=""):
        """
            Pyxis2XXXvs.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ language              : (str) ISO 639-3 name of the language of self,
                                      "" if irrelevant.
            ▪ pyxisname             : (str) string describing the type of self
            ▪ details               : dict(str:str) or a DI object
            ▪ subpyxis              : None(empty list) or a list of Pyxis***
                                      objects
            ▪ _text0reportstr       : (str) corresponding extract from text0
                                      to be initialized by Rhp***.set_text0reportstr()
                                      to be used by the Pyxis***.__str__() methods

            no RETURNED VALUE
        """
        Pyxis2.__init__(self,
                        language=language,
                        pyxisname=pyxisname,
                        details=details,
                        _text0reportstr=_text0reportstr,
                        subpyxis=subpyxis,
                        _type="word")

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis2XXXvs.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(language=self.language,
                          pyxisname=self.pyxisname,
                          details=self.details,
                          subpyxis=self.subpyxis,
                          _text0reportstr=self._text0reportstr)

    #///////////////////////////////////////////////////////////////////////////
    def report(self, margin=""):
        """
            Pyxis2XXXvs.report()
            ____________________________________________________________________

            Return a string describing self in a more friendly way than
            __str__() does, including colored segments of text.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a human-readable string
        """
        res = []

        res.append("{0} \"{1}\" (verbal syntagm) {2}:".format(PYXIS2_SYMB,
                                                              self._text0reportstr,
                                                              self.get_text0pos()))

        res.append("    {0}".format(self.details))

        for pyxis in self.subpyxis:
            res.append("    {0}".format(pyxis))

        return add_prefix_before_line(margin, "\n".join(res))

################################################################################
class Pyxis2XXXpunctuation(Pyxis2):
    """
        Pyxis2XXXpunctuation class
        ________________________________________________________________________

        Pyxis2XXXpunctuation : a Pyxis2 object for punctuation symbol(s).

        ✓ unittests : see the Pyxis2XXXpunctuationTest class.

        about Pyxis classes:
        ˮ The Pyxis objects are boxes where informations are stored.
        ˮ
        ˮ Methods expected : read(), export(), clone(), set_hashvalue(), get_hashvalue(), __eq__()
        ˮ
        ˮ List of the (language independant) Pyxis classes:
        ˮ
        ˮ ▪ Pyxis         : mother all Pyxis*** classes
        ˮ ▪ Pyxis1        : mother all Pyxis1*** classes
        ˮ                   a box for one word, one punctuation symbol or one
        ˮ                   unknown list of characters.
        ˮ
        ˮ ▪ Pyxis1XXXword         : a Pyxis for roughly cut words
        ˮ ▪ Pyxis1XXXpunctuation  : a Pyxis for punctuation symbols
        ˮ ▪ Pyxis1XXXunknown      : a Pyxis for unknown list of characters
        ˮ
        ˮ ▪ Pyxis2        : mother of all Pyxis2*** classes
        ˮ                   abstract elements inside a proposition
        ˮ
        ˮ ▪ Pyxis2XXXng   : a Pyxis2 object for a nominal group
        ˮ ▪ Pyxis2XXXvs   : a Pyxis2 object for a verbal syntagm
        ________________________________________________________________________

        no class attribute

        instance attributes:
        ○ _hashvalue            : (None/bytes) the hash value of self computed by
                                  self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ○ _text0reportstr       : (str) report str of the extract from text0
                                  to be initialized by Rhp***.set_text0reportstr()
                                  to be used by the Pyxis***.__str__() methods
        ○ _type                 : (str) "word" | "punctuation" | "unknown"
                                  Don't read directly _type : instead, use the
                                  .is_a_word(), .is_unknown(),
                                  .is_a_punctuation_symbol()
        ○ details               : (DI object)
        ○ language              : (str) ISO 639-3
        ○ pyxisname             : (str)
        ○ subpyxis              : list of the Pyxis that compose self.

        methods :
        ◐ __init__(self,
                   language, pyxisname,
                   subpyxis=None,
                   details, _text0reportstr="")
        ○ __repr__(self)
        ○ __str__(self)
        ○ add_a_subpyxis(self, pyxis)
        ◐ clone(self)
        ○ get_hashvalue(self)
        ○ get_text0pos(self)
        ○ is_a_punctuation_symbol(self)
        ○ is_a_space(self)
        ○ is_a_word(self)
        ○ is_unknown(self)
        ◐ report(self)
        ○ set_hashvalue(self)
        ○ set_text0pos(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 pyxisname,
                 details,
                 subpyxis=None,
                 _text0reportstr=""):
        """
            Pyxis2XXXpunctuation.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ language              : (str) ISO 639-3 name of the language of self,
                                      "" if irrelevant.
            ▪ pyxisname             : (str) string describing the type of self
            ▪ details               : dict(str:str) or a DI object
            ▪ subpyxis              : None(empty list) or a list of Pyxis***
                                      objects
            ▪ _text0reportstr       : (str) corresponding extract from text0
                                      to be initialized by Rhp***.set_text0reportstr()
                                      to be used by the Pyxis***.__str__() methods

            no RETURNED VALUE
        """
        Pyxis2.__init__(self,
                        language=language,
                        pyxisname=pyxisname,
                        details=details,
                        _text0reportstr=_text0reportstr,
                        subpyxis=subpyxis,
                        _type="punctuation")

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis2XXXpunctuation.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(language=self.language,
                          pyxisname=self.pyxisname,
                          details=self.details,
                          subpyxis=self.subpyxis,
                          _text0reportstr=self._text0reportstr)

    #///////////////////////////////////////////////////////////////////////////
    def report(self, margin=""):
        """
            Pyxis2XXXpunctuation.report()
            ____________________________________________________________________

            Return a string describing self in a more friendly way than
            __str__() does, including colored segments of text.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a human-readable string
        """
        res = []

        res.append("{0} \"{1}\" (punctuation) {2}:".format(PYXIS2_SYMB,
                                                           self._text0reportstr,
                                                           self.get_text0pos()))

        res.append("    {0}".format(self.details))

        for pyxis in self.subpyxis:
            res.append("    {0}".format(pyxis))

        return add_prefix_before_line(margin, "\n".join(res))

################################################################################
class Pyxis2FRApunctuation(Pyxis2XXXpunctuation):
    """
        Pyxis2FRApunctuation class
        ________________________________________________________________________

        (French) Pyxis2 for the punctuation symbol(s).

        ✓ unittests : see the Pyxis2FRApunctuationTest class.

        about Pyxis classes for French:
        ˮ ▪ Pyxis1FRAword       : (Ancient Greek) (roughly cut) "word" Pyxis1
        ˮ ▪ Pyxis1FRApunctuation: (Ancient Greek) "punctuation" Pyxis1
        ˮ ▪ Pyxis1FRAunknown    : (Ancient Greek) "unknown" Pyxis1
        ˮ
        ˮ ▪ Pyxis2FRAng   : (Ancient Greek) Pyxis2 for a nominal group.
        ˮ ▪ Pyxis2FRAvs   : (Ancient Greek) Pyxis2 for a verbal syntagm
        ˮ
        ________________________________________________________________________

        no class attribute

        instance attributes:
        ○ _hashvalue            : (None/bytes) the hash value of self computed by
                                  self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ○ _text0reportstr       : (str) report str of the extract from text0
                                  to be initialized by Rhp***.set_text0reportstr()
                                  to be used by the Pyxis***.__str__() methods
        ○ _type                 : (str) "word" | "punctuation" | "unknown"
                                  Don't read directly _type : instead, use the
                                  .is_a_word(), .is_unknown(),
                                  .is_a_punctuation_symbol()
        ○ details               : (DI object)
        ○ language              : (str) ISO 639-3
        ○ pyxisname             : (str)
        ○ subpyxis              : list of the Pyxis that compose self.

        methods :
        ◐ __init__(self,
                   subpyxis=None,
                   details, _text0reportstr="")
        ○ __repr__(self)
        ○ __str__(self)
        ○ add_a_subpyxis(self, pyxis)
        ◐ clone(self)
        ○ get_hashvalue(self)
        ○ get_text0pos(self)
        ○ is_a_punctuation_symbol(self)
        ○ is_a_space(self)
        ○ is_a_word(self)
        ○ is_unknown(self)
        ○ set_hashvalue(self)
        ○ set_text0pos(self)
        ○ report(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 details,
                 subpyxis=None,
                 _text0reportstr=""):
        """
            Pyxis2FRApunctuation.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ details               : dict(str:str) or a DI object
            ▪ subpyxis              : None(empty list) or a list of Pyxis***
                                      objects
            ▪ _text0reportstr       : (str) corresponding extract from text0
                                      to be initialized by Rhp***.set_text0reportstr()
                                      to be used by the Pyxis***.__str__() methods

            no RETURNED VALUE
        """
        Pyxis2XXXpunctuation.__init__(self,
                                      language="fra",
                                      pyxisname="Pyxis2FRApunctuation",
                                      details=details,
                                      subpyxis=subpyxis,
                                      _text0reportstr=_text0reportstr)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis2FRApunctuation.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(details=self.details,
                          subpyxis=self.subpyxis,
                          _text0reportstr=self._text0reportstr)

################################################################################
class Pyxis2GRCpunctuation(Pyxis2XXXpunctuation):
    """
        Pyxis2GRCpunctuation class
        ________________________________________________________________________

        (Ancient Greek) Pyxis2 for the punctuation symbol(s).

        ✓ unittests : see the Pyxis2GRCpunctuationTest class.

        about Pyxis classes for Ancient Greek:
        ˮ ▪ Pyxis1GRCword       : (Ancient Greek) (roughly cut) "word" Pyxis1
        ˮ ▪ Pyxis1GRCpunctuation: (Ancient Greek) "punctuation" Pyxis1
        ˮ ▪ Pyxis1GRCunknown    : (Ancient Greek) "unknown" Pyxis1
        ˮ
        ˮ ▪ Pyxis2GRCng   : (Ancient Greek) Pyxis2 for a nominal group.
        ˮ ▪ Pyxis2GRCvs   : (Ancient Greek) Pyxis2 for a verbal syntagm
        ________________________________________________________________________

        no class attribute

        instance attributes:
        ○ _hashvalue            : (None/bytes) the hash value of self computed by
                                  self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ○ _text0reportstr       : (str) report str of the extract from text0
                                  to be initialized by Rhp***.set_text0reportstr()
                                  to be used by the Pyxis***.__str__() methods
        ○ _type                 : (str) "word" | "punctuation" | "unknown"
                                  Don't read directly _type : instead, use the
                                  .is_a_word(), .is_unknown(),
                                  .is_a_punctuation_symbol()
        ○ details               : (DI object)
        ○ language              : (str) ISO 639-3
        ○ pyxisname             : (str)
        ○ subpyxis              : list of the Pyxis that compose self.

        methods :
        ◐ __init__(self,
                   subpyxis=None,
                   details, _text0reportstr="")
        ○ __repr__(self)
        ○ __str__(self)
        ○ add_a_subpyxis(self, pyxis)
        ◐ clone(self)
        ○ get_hashvalue(self)
        ○ get_text0pos(self)
        ○ is_a_punctuation_symbol(self)
        ○ is_a_space(self)
        ○ is_a_word(self)
        ○ is_unknown(self)
        ○ report(self)
        ○ set_hashvalue(self)
        ○ set_text0pos(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 details,
                 subpyxis=None,
                 _text0reportstr=""):
        """
            Pyxis2GRCpunctuation.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ details               : dict(str:str) or a DI object
            ▪ subpyxis              : None(empty list) or a list of Pyxis***
                                      objects
            ▪ _text0reportstr       : (str) corresponding extract from text0
                                      to be initialized by Rhp***.set_text0reportstr()
                                      to be used by the Pyxis***.__str__() methods

            no RETURNED VALUE
        """
        Pyxis2XXXpunctuation.__init__(self,
                                      language="fra",
                                      pyxisname="Pyxis2GRCpunctuation",
                                      details=details,
                                      subpyxis=subpyxis,
                                      _text0reportstr=_text0reportstr)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis2GRCpunctuation.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(details=self.details,
                          subpyxis=self.subpyxis,
                          _text0reportstr=self._text0reportstr)

################################################################################
class Pyxis2XXXunknown(Pyxis2):
    """
        Pyxis2XXXunknown class
        ________________________________________________________________________

        Pyxis2XXXunknown : a Pyxis2 object for punctuation symbol(s).

        ✓ unittests : see the Pyxis2XXXunknownTest class.

        about Pyxis classes:
        ˮ The Pyxis objects are boxes where informations are stored.
        ˮ
        ˮ Methods expected : read(), export(), clone(), set_hashvalue(), get_hashvalue(), __eq__()
        ˮ
        ˮ List of the (language independant) Pyxis classes:
        ˮ
        ˮ ▪ Pyxis         : mother all Pyxis*** classes
        ˮ ▪ Pyxis1        : mother all Pyxis1*** classes
        ˮ                   a box for one word, one punctuation symbol or one
        ˮ                   unknown list of characters.
        ˮ
        ˮ ▪ Pyxis1XXXword         : a Pyxis for roughly cut words
        ˮ ▪ Pyxis1XXXpunctuation  : a Pyxis for punctuation symbols
        ˮ ▪ Pyxis1XXXunknown      : a Pyxis for unknown list of characters
        ˮ
        ˮ ▪ Pyxis2        : mother of all Pyxis2*** classes
        ˮ                   abstract elements inside a proposition
        ˮ
        ˮ ▪ Pyxis2XXXng   : a Pyxis2 object for a nominal group
        ˮ ▪ Pyxis2XXXvs   : a Pyxis2 object for a verbal syntagm
        ________________________________________________________________________

        no class attribute

        instance attributes:
        ○ _hashvalue            : (None/bytes) the hash value of self computed by
                                  self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ○ _text0reportstr       : (str) report str of the extract from text0
                                  to be initialized by Rhp***.set_text0reportstr()
                                  to be used by the Pyxis***.__str__() methods
        ○ _type                 : (str) "word" | "punctuation" | "unknown"
                                  Don't read directly _type : instead, use the
                                  .is_a_word(), .is_unknown(),
                                  .is_a_punctuation_symbol()
        ○ details               : (DI object)
        ○ language              : (str) ISO 639-3
        ○ pyxisname             : (str)
        ○ subpyxis              : list of the Pyxis that compose self.

        methods :
        ◐ __init__(self,
                   language, pyxisname,
                   subpyxis=None,
                   details, _text0reportstr="")
        ○ __repr__(self)
        ○ __str__(self)
        ○ add_a_subpyxis(self, pyxis)
        ◐ clone(self)
        ○ get_hashvalue(self)
        ○ get_text0pos(self)
        ○ is_a_punctuation_symbol(self)
        ○ is_a_space(self)
        ○ is_a_word(self)
        ○ is_unknown(self)
        ◐ report(self)
        ○ set_hashvalue(self)
        ○ set_text0pos(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 pyxisname,
                 details,
                 subpyxis=None,
                 _text0reportstr=""):
        """
            Pyxis2XXXunknown.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ language              : (str) ISO 639-3 name of the language of self,
                                      "" if irrelevant.
            ▪ pyxisname             : (str) string describing the type of self
            ▪ details               : dict(str:str) or a DI object
            ▪ subpyxis              : None(empty list) or a list of Pyxis***
                                      objects
            ▪ _text0reportstr       : (str) corresponding extract from text0
                                      to be initialized by Rhp***.set_text0reportstr()
                                      to be used by the Pyxis***.__str__() methods

            no RETURNED VALUE
        """
        Pyxis2.__init__(self,
                        language=language,
                        pyxisname=pyxisname,
                        details=details,
                        _text0reportstr=_text0reportstr,
                        subpyxis=subpyxis,
                        _type="unknown")

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis2XXXunknown.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(language=self.language,
                          pyxisname=self.pyxisname,
                          details=self.details,
                          subpyxis=self.subpyxis,
                          _text0reportstr=self._text0reportstr)

    #///////////////////////////////////////////////////////////////////////////
    def report(self, margin=""):
        """
            Pyxis2XXXunknown.report()
            ____________________________________________________________________

            Return a string describing self in a more friendly way than
            __str__() does, including colored segments of text.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a human-readable string
        """
        res = []

        res.append("{0} \"{1}\" (unknown) {2}:".format(PYXIS2_SYMB,
                                                       self._text0reportstr,
                                                       self.get_text0pos()))

        res.append("    {0}".format(self.details))

        for pyxis in self.subpyxis:
            res.append("    {0}".format(pyxis))

        return add_prefix_before_line(margin, "\n".join(res))

################################################################################
class Pyxis2FRAunknown(Pyxis2XXXunknown):
    """
        Pyxis2FRAunknown class
        ________________________________________________________________________

        (French) Pyxis2 for the punctuation symbol(s).

        ✓ unittests : see the Pyxis2FRAunknownTest class.

        about Pyxis classes for French:
        ˮ ▪ Pyxis1FRAword       : (Ancient Greek) (roughly cut) "word" Pyxis1
        ˮ ▪ Pyxis1FRApunctuation: (Ancient Greek) "punctuation" Pyxis1
        ˮ ▪ Pyxis1FRAunknown    : (Ancient Greek) "unknown" Pyxis1
        ˮ
        ˮ ▪ Pyxis2FRAng   : (Ancient Greek) Pyxis2 for a nominal group.
        ˮ ▪ Pyxis2FRAvs   : (Ancient Greek) Pyxis2 for a verbal syntagm
        ˮ
        ________________________________________________________________________

        no class attribute

        instance attributes:
        ○ _hashvalue            : (None/bytes) the hash value of self computed by
                                  self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ○ _text0reportstr       : (str) report str of the extract from text0
                                  to be initialized by Rhp***.set_text0reportstr()
                                  to be used by the Pyxis***.__str__() methods
        ○ _type                 : (str) "word" | "punctuation" | "unknown"
                                  Don't read directly _type : instead, use the
                                  .is_a_word(), .is_unknown(),
                                  .is_a_punctuation_symbol()
        ○ details               : (DI object)
        ○ language              : (str) ISO 639-3
        ○ pyxisname             : (str)
        ○ subpyxis              : list of the Pyxis that compose self.

        methods :
        ◐ __init__(self,
                   subpyxis=None,
                   details, _text0reportstr="")
        ○ __repr__(self)
        ○ __str__(self)
        ○ add_a_subpyxis(self, pyxis)
        ◐ clone(self)
        ○ get_hashvalue(self)
        ○ get_text0pos(self)
        ○ is_a_punctuation_symbol(self)
        ○ is_a_space(self)
        ○ is_a_word(self)
        ○ is_unknown(self)
        ○ report(self)
        ○ set_hashvalue(self)
        ○ set_text0pos(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 details,
                 subpyxis=None,
                 _text0reportstr=""):
        """
            Pyxis2FRAunknown.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ details               : dict(str:str) or a DI object
            ▪ subpyxis              : None(empty list) or a list of Pyxis***
                                      objects
            ▪ _text0reportstr       : (str) corresponding extract from text0
                                      to be initialized by Rhp***.set_text0reportstr()
                                      to be used by the Pyxis***.__str__() methods

            no RETURNED VALUE
        """
        Pyxis2XXXunknown.__init__(self,
                                  language="fra",
                                  pyxisname="Pyxis2FRAunknown",
                                  details=details,
                                  subpyxis=subpyxis,
                                  _text0reportstr=_text0reportstr)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis2FRAunknown.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(details=self.details,
                          subpyxis=self.subpyxis,
                          _text0reportstr=self._text0reportstr)

################################################################################
class Pyxis2GRCunknown(Pyxis2XXXunknown):
    """
        Pyxis2GRCunknown class
        ________________________________________________________________________

        (Ancient Greek) Pyxis2 for the punctuation symbol(s).

        ✓ unittests : see the Pyxis2GRCunknownTest class.

        about Pyxis classes for Ancient Greek:
        ˮ ▪ Pyxis1GRCword       : (Ancient Greek) (roughly cut) "word" Pyxis1
        ˮ ▪ Pyxis1GRCpunctuation: (Ancient Greek) "punctuation" Pyxis1
        ˮ ▪ Pyxis1GRCunknown    : (Ancient Greek) "unknown" Pyxis1
        ˮ
        ˮ ▪ Pyxis2GRCng   : (Ancient Greek) Pyxis2 for a nominal group.
        ˮ ▪ Pyxis2GRCvs   : (Ancient Greek) Pyxis2 for a verbal syntagm
        ________________________________________________________________________

        no class attribute

        instance attributes:
        ○ _hashvalue            : (None/bytes) the hash value of self computed by
                                  self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ○ _text0reportstr       : (str) report str of the extract from text0
                                  to be initialized by Rhp***.set_text0reportstr()
                                  to be used by the Pyxis***.__str__() methods
        ○ _type                 : (str) "word" | "punctuation" | "unknown"
                                  Don't read directly _type : instead, use the
                                  .is_a_word(), .is_unknown(),
                                  .is_a_punctuation_symbol()
        ○ details               : (DI object)
        ○ language              : (str) ISO 639-3
        ○ pyxisname             : (str)
        ○ subpyxis              : list of the Pyxis that compose self.

        methods :
        ◐ __init__(self,
                   subpyxis=None,
                   details, _text0reportstr="")
        ○ __repr__(self)
        ○ __str__(self)
        ○ add_a_subpyxis(self, pyxis)
        ◐ clone(self)
        ○ get_hashvalue(self)
        ○ get_text0pos(self)
        ○ is_a_punctuation_symbol(self)
        ○ is_a_space(self)
        ○ is_a_word(self)
        ○ is_unknown(self)
        ○ report(self)
        ○ set_hashvalue(self)
        ○ set_text0pos(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 details,
                 subpyxis=None,
                 _text0reportstr=""):
        """
            Pyxis2GRCunknown.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ details               : dict(str:str) or a DI object
            ▪ subpyxis              : None(empty list) or a list of Pyxis***
                                      objects
            ▪ _text0reportstr       : (str) corresponding extract from text0
                                      to be initialized by Rhp***.set_text0reportstr()
                                      to be used by the Pyxis***.__str__() methods

            no RETURNED VALUE
        """
        Pyxis2XXXunknown.__init__(self,
                                  language="fra",
                                  pyxisname="Pyxis2GRCunknown",
                                  details=details,
                                  subpyxis=subpyxis,
                                  _text0reportstr=_text0reportstr)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis2GRCunknown.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(details=self.details,
                          subpyxis=self.subpyxis,
                          _text0reportstr=self._text0reportstr)

################################################################################
class Pyxis2FRAvs(Pyxis2XXXvs):
    """
        Pyxis2FRAvs class
        ________________________________________________________________________

        (French) Pyxis2 for a nominal group.

        ✓ unittests : see the Pyxis2FRAvsTest class.

        about Pyxis classes for French:
        ˮ ▪ Pyxis1FRAword       : (Ancient Greek) (roughly cut) "word" Pyxis1
        ˮ ▪ Pyxis1FRApunctuation: (Ancient Greek) "punctuation" Pyxis1
        ˮ ▪ Pyxis1FRAunknown    : (Ancient Greek) "unknown" Pyxis1
        ˮ
        ˮ ▪ Pyxis2FRAng   : (Ancient Greek) Pyxis2 for a nominal group.
        ˮ ▪ Pyxis2FRAvs   : (Ancient Greek) Pyxis2 for a verbal syntagm
        ˮ
        ________________________________________________________________________

        no class attribute

        instance attributes:
        ○ _hashvalue            : (None/bytes) the hash value of self computed by
                                  self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ○ _text0reportstr       : (str) report str of the extract from text0
                                  to be initialized by Rhp***.set_text0reportstr()
                                  to be used by the Pyxis***.__str__() methods
        ○ _type                 : (str) "word" | "punctuation" | "unknown"
                                  Don't read directly _type : instead, use the
                                  .is_a_word(), .is_unknown(),
                                  .is_a_punctuation_symbol()
        ○ details               : (DI object)
        ○ language              : (str) ISO 639-3
        ○ pyxisname             : (str)
        ○ subpyxis              : list of the Pyxis that compose self.

        methods :
        ◐ __init__(self,
                   subpyxis=None,
                   details, _text0reportstr="")
        ○ __repr__(self)
        ○ __str__(self)
        ○ add_a_subpyxis(self, pyxis)
        ◐ clone(self)
        ○ get_hashvalue(self)
        ○ get_text0pos(self)
        ○ is_a_punctuation_symbol(self)
        ○ is_a_space(self)
        ○ is_a_word(self)
        ○ is_unknown(self)
        ○ report(self)
        ○ set_hashvalue(self)
        ○ set_text0pos(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 details,
                 subpyxis=None,
                 _text0reportstr=""):
        """
            Pyxis2FRAvs.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ details               : dict(str:str) or a DI object
            ▪ subpyxis              : None(empty list) or a list of Pyxis***
                                      objects
            ▪ _text0reportstr       : (str) corresponding extract from text0
                                      to be initialized by Rhp***.set_text0reportstr()
                                      to be used by the Pyxis***.__str__() methods

            no RETURNED VALUE
        """
        Pyxis2XXXvs.__init__(self,
                             language="fra",
                             pyxisname="Pyxis2FRAvs",
                             details=details,
                             subpyxis=subpyxis,
                             _text0reportstr=_text0reportstr)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis2FRAvs.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(details=self.details,
                          subpyxis=self.subpyxis,
                          _text0reportstr=self._text0reportstr)

################################################################################
class LProcess(list):
    """
        LProcess class
        ________________________________________________________________________

        a list of Process** objects. See also the ProcessContainer class.
        ________________________________________________________________________

        no class attribute

        no instance attribute :

        methods :
        ◐ __init__(self)
        ● uniquenames(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
            LProcess.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE
        """
        list.__init__(self)

    #///////////////////////////////////////////////////////////////////////////
    def uniquenames(self):
        """
            LProcess.uniquenames()
            ____________________________________________________________________

            (debug oriented method)
            Return a short identification of self, i.e. a list of the uniquename
            of each element in self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : the expected string
        """
        res = []
        for process in self:
            res.append(process.uniquename())
        return "["+";".join(res)+"]"

################################################################################
class ProcessContainer(dict):
    """
        ProcessContainer class
        ________________________________________________________________________

        Use this object to store Processes*** objects. See also the LProcess
        class.

        dict : (str)process name → Process*** object
        ________________________________________________________________________

        no class attribute

        no instance attribute

        methods :
        ◐ __init__(self)
        ◐ __str__(self)
        ● add(self, new_process)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
            ProcessContainer.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE
        """
        dict.__init__(self)

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
            ProcessContainer.__str__()
            ____________________________________________________________________

            Return a human-readable representation of self.
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE
        """
        res = []
        for name in sorted(self):
            res.append("{0}".format(self[name]))
        return "\n".join(res)

    #///////////////////////////////////////////////////////////////////////////
    def add(self,
            new_process):
        """
            ProcessContainer.add()
            ____________________________________________________________________

            Return a human-readable representation of self.
            ____________________________________________________________________

            ARGUMENT: (Process*** object)

            no RETURNED VALUE
        """
        self[new_process.processname] = new_process

################################################################################
class Process(object):
    """
        Process class
        ________________________________________________________________________

        Mother-class for all the Process*** classes.

        about Process classes:
        ˮ Process objects are applied to Rhp*** objects and create other
        ˮ Rhp*** objects.
        ˮ
        ˮ ▪ Process : mother class of all Process*** classes
        ˮ ▪ ProcessXXXblurwords    : (language independant) cuts the text along the punctuation
        ˮ ▪ ProcessXXXmorpho      : (language independant) read a Rhp object and add
        ˮ                           informations about its morphological analysis
        ˮ ▪ ProcessXXXsentences   : (language independant) create a classe able to group
        ˮ                           together Pyxis objects into sentences
        ˮ ▪ ProcessXXXnormalize   : (language independant) normalize strings
        ˮ
        ˮ
        ˮ ▪ ProcessFRA : mother class of all ProcessFRA*** classes : Ancient Greek
        ˮ ▪ ProcessGRC : mother class of all ProcessGRC*** classes : French
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ● language              : (str) ISO 639-3 name of the language of self,
                                  "" if irrelevant.
        ● processname           : (str)
        ● output_rhpobject_name : (type) the name of the Rhp object to be added
        ● spec                  : (different types, None if undefined)
                                  specifications describing the way the process
                                  does its job.
        ● to_be_applied_to      : (type) name of the target Rhp object

        methods :
        ● __init__(self, processname, language, to_be_applied_to, output_rhpobject_name)
        ● __str__(self)
        ● uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 processname,
                 to_be_applied_to,
                 output_rhpobject_name,
                 spec=None):
        """
            Process.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ processname           : (str)
            ▪ language              : (str) ISO 639-3 name of the language of self,
                                      "" if irrelevant.
            ▪ to_be_applied_to      : (type) name of the target Rhp
                                      object
            ▪ output_rhpobject_name : (type) the name of the Rhp object to be added.
            ▪ spec                  : (different types, None if undefined)
                                      specifications describing the way the process
                                      does its job.

            no RETURNED VALUE.
        """
        self.language = language
        self.processname = processname
        self.to_be_applied_to = to_be_applied_to
        self.output_rhpobject_name = output_rhpobject_name
        self.spec = spec

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
            Process.__str__()
            ____________________________________________________________________

            Return a human-readable representation of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : the expected string
        """
        return "{0} {1} : language='{2}' " \
               "to_be_applied_to='{3}'".format(PROCESS_SYMB,
                                               self.processname,
                                               self.language,
                                               self.to_be_applied_to)

    #///////////////////////////////////////////////////////////////////////////
    def uniquename(self):
        """
            Process.uniquename()
            ____________________________________________________________________

            (debug oriented method)
            Return a short identification of self
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : the expected string
        """
        return self.processname

################################################################################
class ProcessXXXblurwords(Process):
    """
        ProcessXXXblurwords class
        ________________________________________________________________________

        about ProcessXXXblurwords:
        ˮ language independant class : Process to cut a string into words,
        ˮ punctuation and unknown characters.
        ˮ This is a very rough way to cut a string into words. A word may
        ˮ not end with a punctuation symbol, e.g. if an enclitic is added
        ˮ at the end of the word:
        ˮ     (Latin)             dominusque (in fact, dominus + que)
        ˮ     (Ancient Greek)     οἰωνοῖσίτε πᾶσι (in fact, οἰωνοῖσί + τε)
        ˮ     (Sanskrit)          गच्छतीश्वरः  (in fact, गच्छति + ईश्वरः)
        ˮ

        ▪ read a Rhp0 object, cuts it along the punctuation symbols, trying to
          find words.
        ▪ add a unique RhpFRA1 object.
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ○ language              : (str) ISO 639-3 name of the language of self,
        ○ output_rhpobject_name : (type) the name of the Rhp object to be added
        ○ processname           : (str)
        ○ spec                  : a list of str.
        ○ to_be_applied_to      : (type) name of the target Rhp object

        methods :
        ◐ __init__(self,
                   language, processname,
                   to_be_applied_to,
                   output_rhpobject_name,
                   spec)
        ○ __str__(self)
        ● read(self, target_rhp, text0)
        ○ uniquename(self)
   """
    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 processname,
                 to_be_applied_to,
                 output_rhpobject_name,
                 spec):
        """
            ProcessXXXblurwords.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ language                  : (str) ISO 639-3 name of the language of
                                          self, "" if irrelevant.
            ▪ processname               : (str)
            ▪ output_rhpobject_name     : (type) the name of the Rhp object to
                                          be added.
            ▪ spec                      : a list of str

            no RETURNED VALUE
        """
        Process.__init__(self,
                         language=language,
                         processname=processname,
                         to_be_applied_to=to_be_applied_to,
                         output_rhpobject_name=output_rhpobject_name,
                         spec=spec)

    #///////////////////////////////////////////////////////////////////////////
    def read(self,
             target_rhp,
             text0):
        """
            ProcessXXXblurwords.read()
            ____________________________________________________________________

            Apply a process to the Rhp object <target_rhp>, the initial source
            text being <text0>.
            ____________________________________________________________________

            ARGUMENTS:
            ▪ target_rhp    : the Rhp object whom self is applied.
            ▪ text0         : (str) the initial source text

            RETURNED VALUE : the list of the <new_object> objects to be added.
        """
        strings = LCharAndTextPos()
        text = target_rhp.text0  # text is a (str)ing.

        punctuation_symbols = self.spec

        for index, character in enumerate(text):
            if character in punctuation_symbols:
                strings.append(CharAndTextPos(character,
                                              TextPos().addx0x1(index, index+1)))
            else:
                if len(strings) == 0:
                    strings.append(CharAndTextPos(character,
                                                  TextPos().addx0x1(index, index+1)))

                elif strings[-1].characters not in punctuation_symbols:
                    strings[-1].characters += character
                    strings[-1].textpos[-1][1] = index+1
                else:
                    strings.append(CharAndTextPos(character,
                                                  TextPos().addx0x1(index, index+1)))

        new_rhp = self.output_rhpobject_name(text0=text0, text=strings)
        new_rhp.set_hashvalue()
        return tuple((new_rhp,))

################################################################################
#    ProcessXXXmorphoSPEC class
#    ________________________________________________________________________
#
#    ProcessXXXmorphoSPEC : class used by ProcessXXXmorpho to store the
#    three informations : {pyxis1_punctuation,
#                          pyxis1_word
#                          pyxis1_unknown
#                         }
#
#    about the format of ProcessXXXmorphoSPEC:
#    ˮ
#    ˮ     pyxis1_punctuation  : Pyxis1 object storing a punctuation symbol
#    ˮ     pyxis1_word         : Pyxis1 object storing a word
#    ˮ     pyxis1_unknown      : Pyxis1 object storing an unknown symbol
#    ˮ
#    ˮ example :
#    ˮ
#    ˮ     ProcessXXXmorphoSPEC(pyxis1_word=Pyxis1FRAword,
#    ˮ                          pyxis1_punctuation=Pyxis1FRApunctuation,
#    ˮ                          pyxis1_unknown=Pyxis1FRAunknown))
#    ____________________________________________________________________
#
#    instance attributes :
#    ● pyxis1_unknown           : Pyxis1 object storing an unknown symbol
#    ● pyxis1_punctuation       : Pyxis1 object storing a punctuation symbol
#    ● pyxis1_word              : Pyxis1 object storing a word

ProcessXXXmorphoSPEC = collections.namedtuple("ProcessXXXmorphoSPEC",
                                              ["pyxis1_punctuation",
                                               "pyxis1_unknown",
                                               "pyxis1_word"])

################################################################################
class ProcessXXXmorpho(Process):
    """
        ProcessXXXmorpho class
        ________________________________________________________________________

        Read a Rhp object and add informations about its morphological
        analysis.
        Add one or more <output_rhpobject_name> objects.
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ○ language                  : (str) ISO 639-3 name of the language of self,
        ○ output_rhpobject_name     : (type) name of the Rhp object to be added.
                                      dedicated to "unknown strings".
        ○ processname               : (str)
        ○ spec                      : (ProcessXXXmorphoSPEC)
        ○ to_be_applied_to          : (type) name of the target Rhp object

        methods :
        ◐ __init__(self,
                   language, processname,
                   to_be_applied_to,
                   output_rhpobject_name,
                   spec)
        ○ __str__(self)
        ● read(target_rhp, text0)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 processname,
                 to_be_applied_to,
                 output_rhpobject_name,
                 spec):
        """
            ProcessXXXmorpho.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:

            ▪ processname               : (str) name of the current
                                          process.
            ▪ language                  : (str) ISO 639-3, set to "fra" by
                                          the mother-class
            ▪ to_be_applied_to          : (type) objects read by this
                                          process.
            ▪ output_rhpobject_name     : (type) the name of the Rhp object to
                                          be added.
            ▪ spec                      : (ProcessXXXmorphoSPEC)

            no RETURNED VALUE.
        """
        Process.__init__(self,
                         language=language,
                         processname=processname,
                         to_be_applied_to=to_be_applied_to,
                         output_rhpobject_name=output_rhpobject_name,
                         spec=spec)

    #///////////////////////////////////////////////////////////////////////////
    def read(self,
             target_rhp,
             text0):
        """
            ProcessXXXmorpho.read()
            ____________________________________________________________________

            Apply a process to the Rhp object <target_rhp>, the initial source text
            being <text0>.
            ____________________________________________________________________

            ARGUMENTS:
            ▪ target_rhp    : the Rhp object whom the self is applied.
            ▪ text0         : (str) the initial source text

            RETURNED VALUE : the list of the <self.output_rhpobject_name> objects
                             to be added.
        """
        res = [self.output_rhpobject_name(text0=text0),] # a list of <output_rhpobject_name> objects
        text = target_rhp.text # text is a list of (string, index)

        for charandtextpos in text:
            res2 = []

            # morphos : a list of dict.
            morphos = GMORPHO.search(language=self.language,
                                     searched_form=charandtextpos.characters,
                                     minimal_accuracy=0.3)

            for morpho in morphos:

                # Yes, <pyxis_to_be_added> can be of three different kinds. It's ok.
                # pylint: disable=redefined-variable-type
                if morpho["@type"] == "word":
                    pyxis_to_be_added = \
                      self.spec.pyxis1_word(text=charandtextpos.characters,
                                            _text0pos=TextPos(charandtextpos.textpos),
                                            details=morpho)
                elif morpho["@type"] == "punctuation":
                    pyxis_to_be_added = \
                      self.spec.pyxis1_punctuation(text=charandtextpos.characters,
                                                   _text0pos=TextPos(charandtextpos.textpos),
                                                   details=morpho)
                else:
                    pyxis_to_be_added = \
                      self.spec.pyxis1_unknown(text=charandtextpos.characters,
                                               _text0pos=TextPos(charandtextpos.textpos),
                                               details=morpho)

                for outputobject in res:
                    new_outputobject = outputobject.clone()
                    new_outputobject.text.append(pyxis_to_be_added)
                    res2.append(new_outputobject)

            res = res2

        return res

################################################################################
class ProcessXXXsentences(Process):
    """
        ProcessXXXsentences class
        ________________________________________________________________________

        Use this class to create classes able to group together Pyxis
        objects into sentences.
        ________________________________________________________________________

        no class attribute

        instance attribute :
        ○ language              : (str) ISO 639-3 name of the language of self,
        ○ output_rhpobject_name : (type) the name of the Rhp object to
                                  be added.
        ○ processname           : (str)
        ○ spec                  : (None, undefined)
        ○ to_be_applied_to      : (type) name of the target Rhp object

        methods :
        ◐ __init__(self,
                   language, processname,
                   to_be_applied_to,
                   output_rhpobject_name)
        ○ __str__(self)
        ● read(self, target_rhp, text0)
        ○ uniquename(self)
   """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 processname,
                 to_be_applied_to,
                 output_rhpobject_name):
        """
            ProcessXXXsentences.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ processname           : (str)
            ▪ language              : (str) ISO 639-3 name of the language of self,
            ▪ to_be_applied_to      : (type) name of the target Rhp
                                      object
            ▪ output_rhpobject_name : (type) the name of the Rhp object to
                                      be added.

            no RETURNED VALUE
        """
        Process.__init__(self,
                         language=language,
                         processname=processname,
                         to_be_applied_to=to_be_applied_to,
                         output_rhpobject_name=output_rhpobject_name)

    #///////////////////////////////////////////////////////////////////////////
    def read(self,
             target_rhp,
             text0):
        """
            ProcessXXXsentences.read()
            ____________________________________________________________________

            Apply a process to the Rhp object <target_rhp>, the initial source
            text being <text0>.
            ____________________________________________________________________

            ARGUMENTS:
            ▪ target_rhp    : the Rhp object whom the self is applied.
            ▪ text0         : (str) the initial source text

            RETURNED VALUE  : the list of the <output_rhpobject_name> objects to
                              be added.
        """
        LOGGER.debug("ProcessXXXsentences.read() : target_rhp=%s",
                     target_rhp.uniquename())

        res = LRhp() # a list of Rhp*** objects
        text = target_rhp.text  # text is a LPyxis object

        for index, pyxis in enumerate(text):
            last_pyxis_in_text = index == len(text)-1

            if pyxis.details["@type"] == "unknown":
                # unknown content :
                if len(res) == 0:
                    res.append(self.output_rhpobject_name(text0=text0))
                res[-1].text.append(pyxis)

            elif pyxis.punctuation_symb is False:
                # everything but a punctuation symbol :
                if len(res) == 0:
                    res.append(self.output_rhpobject_name(text0=text0))
                res[-1].text.append(pyxis)

            elif pyxis.details["@punctuation type"] == "strong":
                # strong punctuation symbol
                if len(res) == 0:
                    res.append(self.output_rhpobject_name(text0=text0))

                res[-1].ending_punc = pyxis.clone()
                if not last_pyxis_in_text:
                    res.append(self.output_rhpobject_name(text0=text0))

            else:
                # other weak punctuation symbols :
                if len(res) == 0:
                    res.append(self.output_rhpobject_name(text0=text0))
                res[-1].text.append(pyxis)

        return res

################################################################################
class ProcessFRA0(ProcessXXXblurwords):
    """
        ProcessFRA0 class
        ________________________________________________________________________

        (French) use ProcessFRA0 to roughly cut a string into words and
        punctuation symbols.

        ▪ read a Rhp0 object, cuts it along the punctuation symbols, trying to find words.
        ▪ add a unique RhpFRA1 object.

        about ProcessXXXblurwords:
        ˮ language independant class : Process to cut a string into words,
        ˮ punctuation and unknown characters.
        ˮ This is a very rough way to cut a string into words. A word may
        ˮ not end with a punctuation symbol, e.g. if an enclitic is added
        ˮ at the end of the word:
        ˮ     (Latin)             dominusque (in fact, dominus + que)
        ˮ     (Ancient Greek)     οἰωνοῖσίτε πᾶσι (in fact, οἰωνοῖσί + τε)
        ˮ     (Sanskrit)          गच्छतीश्वरः  (in fact, गच्छति + ईश्वरः)
        ˮ

        about Process classes for French:
        ˮ ▪ ProcessFRA : mother class of all ProcessFRA*** classes : Ancient Greek
        ˮ ▪ ProcessFRA0 - reads Rhp0
        ˮ               -- cuts the text along the punctuation
        ˮ               --- creates RhpFRA1
        ˮ ▪ ProcessFRA1 - reads RhpFRA1
        ˮ               -- normalizes the text
        ˮ               --- creates RhpFRA2
        ˮ ▪ ProcessFRA2 - reads RhpFRA2
        ˮ               -- gets the morphological analysis
        ˮ               --- creates RhpFRA3
        ˮ ▪ ProcessFRA3 - reads RhpFRA3
        ˮ               -- groups together Pyxis into sentences
        ˮ               --- creates RhpFRA4
        ˮ ▪ ProcessFRA4 - reads RhpFRA4
        ˮ               -- Pyxis1FRAword > Pyxis2FRA***
        ˮ               --- creates RhpFRA5
        ____________________________________________________________________

        no class attribute

        instance attributes :
        ○ language              : (str) ISO 639-3, set to "fra" by
                                  the mother-class
        ○ output_rhpobject_name : the type added by the .read()
                                  method. Should be an Rhp*** object.
        ○ processname           : (str) name of the current
                                  process.
        ○ punctuation_symbols   : a list of str
        ○ spec                  : (different types, None if undefined)
                                  specifications describing the way the process
                                  does its job.
        ○ to_be_applied_to      : (type) objects read by this
                                  process.

        methods :
        ◐ __init__(self)
        ○ __str__(self)
        ○ read(self, target_rhp, text0)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
            ProcessFRA0.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        ProcessXXXblurwords.__init__(self,
                                     language="fra",
                                     processname="ProcessFRA0",
                                     to_be_applied_to=Rhp0,
                                     output_rhpobject_name=RhpFRA1,
                                     spec=(' ', '.', ';', "'", ","))

################################################################################
class ProcessXXXnormalize(Process):
    """
        ProcessXXXnormalize class
        ________________________________________________________________________

        use ProcessXXXnormalize to normalize strings.

        ▪ Read a Rhp object and normalize its content.
        ▪ Add a unique output_rhpobject_name object.

        about Process classes:
        ˮ Process objects are applied to Rhp*** objects and create other
        ˮ Rhp*** objects.
        ˮ
        ˮ ▪ Process : mother class of all Process*** classes
        ˮ ▪ ProcessXXXblurwords    : (language independant) cuts the text along the punctuation
        ˮ ▪ ProcessXXXmorpho      : (language independant) read a Rhp object and add
        ˮ                           informations about its morphological analysis
        ˮ ▪ ProcessXXXsentences   : (language independant) create a classe able to group
        ˮ                           together Pyxis objects into sentences
        ˮ ▪ ProcessXXXnormalize   : (language independant) normalize strings
        ˮ
        ˮ
        ˮ ▪ ProcessFRA : mother class of all ProcessFRA*** classes : Ancient Greek
        ˮ ▪ ProcessGRC : mother class of all ProcessGRC*** classes : French
        ____________________________________________________________________

        no class attribute

        instance attributes :
        ○ language              : (str) ISO 639-3 name of the
                                  language of self,
        ○ output_rhpobject_name : (type) the name of the Rhp object to be added
        ○ processname           : (str)
        ○ spec                  : (None, undefined)
        ○ to_be_applied_to      : (type) object read by the process.

        methods :
        ◐ __init__(self,
                   language, processname,
                   to_be_applied_to, output_rhpobject_name)
        ○ __str__(self)
        ● read(self, all_rhp, rhphashvalue, text0)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 processname,
                 to_be_applied_to,
                 output_rhpobject_name):
        """
            ProcessXXXnormalize.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ language                  : (str) ISO 639-3 name of the language of
                                          self, "" if irrelevant.
            ▪ processname               : (str)
            ▪ to_be_applied_to          : (type) name of the target Rhp object
            ▪ output_rhpobject_name     : (type) the name of the Rhp object to
                                          be added.

            no RETURNED VALUE.
        """
        Process.__init__(self,
                         language=language,
                         processname=processname,
                         to_be_applied_to=to_be_applied_to,
                         output_rhpobject_name=output_rhpobject_name)

    #///////////////////////////////////////////////////////////////////////////
    def read(self,
             target_rhp,
             text0):
        """
            ProcessXXXnormalize.read()
            ____________________________________________________________________

            Apply a process to the Rhp object <target_rhp>, the initial source
            text being <text0>.
            ____________________________________________________________________

            ARGUMENTS:
            ▪ target_rhp    : the Rhp object whom the self is applied.
            ▪ text0         : (str) the initial source text

            RETURNED VALUE : a list of Rhp*** objects.
        """
        strings = LCharAndTextPos() # [(str, pos), ...]
        text = target_rhp.text  # text is a list of (string, index)

        for cpos in text:
            strings.append(CharAndTextPos(characters=cpos.characters,
                                          textpos=cpos.textpos))

        return tuple((self.output_rhpobject_name(text=strings, text0=text0),))


################################################################################
#    Pyxis1TOPyxis2SPECSVK class
#    ________________________________________________________________________
#
#    Pyxis1TOPyxis2SPECSVK : class used by Pyxis1TOPyxis2SPEC to store the
#    three informations : {src_pyxisname,        Svk
#                          value_in_details,     sVk
#                          keys_in_details       svK
#                         }
#
#    about the format of Pyxis1TOPyxis2SPEC(+SVK):
#    ˮ
#    ˮ     dest_type        : (type)
#    ˮ     src_pyxisname    : (str)
#    ˮ     value_in_details : (str, None if irrelevant)
#    ˮ     keys_in_details  : (list of str, None if value_in_details is None)
#    ˮ
#    ˮ example :
#    ˮ to transform a Pyxis1GRCword into a Pyxis2GRCng if
#    ˮ details["grammatical nature"] in ("common noun", "something") :
#    ˮ
#    ˮ     Pyxis1TOPyxis2SPEC({
#    ˮ       Pyxis2GRCng : ("Pyxis1GRCword",          = dest_type : {src_pyxisname,
#    ˮ                      "grammatical nature",                 value_in_details,
#    ˮ                      ("common noun", "something")),        keys_in_details}
#    ˮ     })
#    ˮ
#    ____________________________________________________________________
#
#    instance attributes :
#    ● src_pyxisname         : Pyxis1 object to be transformed into a Pyxis2
#                              object
#    ● value_in_details      : (str) value expected in .details
#    ● keys_in_details       : .details[value_in_details] have to be equal
#                              to one of the <keys_in_details>.
Pyxis1TOPyxis2SPECSVK = collections.namedtuple("Pyxis1TOPyxis2SPECSVK",
                                               ['src_pyxisname',
                                                'value_in_details',
                                                'keys_in_details'])

################################################################################
class Pyxis1TOPyxis2SPEC(dict):
    """
        Pyxis1TOPyxis2SPEC class
        ________________________________________________________________________

        Class used by ProcessXXXPyxis1ToPyxis2 to store the specifications
        describing how to replace a Pyxis1 object by a Pyxis2 one.

        dict: (type)dest_type → Pyxis1TOPyxis2SPECSVK

        about the format of Pyxis1TOPyxis2SPEC(+SVK):
        ˮ
        ˮ     dest_type        : (type)
        ˮ     src_pyxisname    : (str)
        ˮ     value_in_details : (str, None if irrelevant)
        ˮ     keys_in_details  : (list of str, None if value_in_details is None)
        ˮ
        ˮ example :
        ˮ to transform a Pyxis1GRCword into a Pyxis2GRCng if
        ˮ details["grammatical nature"] in ("common noun", "something") :
        ˮ
        ˮ     Pyxis1TOPyxis2SPEC({
        ˮ       Pyxis2GRCng : ("Pyxis1GRCword",          = dest_type : {src_pyxisname,
        ˮ                      "grammatical nature",                 value_in_details,
        ˮ                      ("common noun", "something")),        keys_in_details}
        ˮ     })
        ˮ
        ____________________________________________________________________

        no class attribute

        no instance attribute

        methods :
        ◐ __init__(self, src)
        ○ add(self, dest_type, src_pyxisname, value_in_details, keys_in_details)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self, src):
        """
            Pyxis1TOPyxis2SPEC.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENT:
            ▪ src : a dict, see below :

              about the dict given to Pyxis1TOPyxis2SPEC.__init__():
              ˮ { (type)dest_type : ((str)src_pyxisname,
              ˮ                      (str)value_in_details,
              ˮ                      (list of str)keys_in_details) }
              ˮ
              ˮ by example :
              ˮ             { Pyxis2GRCng : ("Pyxis1GRCword",
              ˮ                              "grammatical nature",
              ˮ                              ("common noun",))
              ˮ             }
              ˮ

            no RETURNED VALUE.
        """
        dict.__init__(self)

        for dest_type, (src_pyxisname, value_in_details, keys_in_details) in src.items():
            self.add(dest_type=dest_type,
                     src_pyxisname=src_pyxisname,
                     value_in_details=value_in_details,
                     keys_in_details=keys_in_details)

    #///////////////////////////////////////////////////////////////////////////
    def add(self, dest_type, src_pyxisname, value_in_details, keys_in_details):
        """
            Pyxis1TOPyxis2SPEC.add()
            ____________________________________________________________________

            A convenient way to fill self.
            ____________________________________________________________________

            ARGUMENTS:
            ▪ dest_type         : (type) the Pyxis2 to be created
            ▪ src_pyxisname     : (str) the Pyxis1 to be transformed
            ▪ value_in_details  : (str) .details[value_in_details] has to be
                                        equal to one of the keys_in_details.
            ▪ keys_in_details   : (list of str) see value_in_details

            no RETURNED VALUE.
        """
        self[dest_type] = Pyxis1TOPyxis2SPECSVK(src_pyxisname=src_pyxisname,
                                                value_in_details=value_in_details,
                                                keys_in_details=keys_in_details)

################################################################################
class ProcessXXXPyxis1ToPyxis2(Process):
    """
        ProcessXXXPyxis1ToPyxis2 class
        ________________________________________________________________________

        about ProcessXXXPyxis1ToPyxis2:
        ˮ a language independant class : transform each Pyxis1 objects into
        ˮ Pyxis2 objects.
        ˮ The transformation is described by the .specifications attribute, a
        ˮ Pyxis1TOPyxis2SPEC object.
        ˮ
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ○ language              : (str) ISO 639-3 name of the language of self,
        ○ output_rhpobject_name : (type) the name of the Rhp object to be added
        ○ processname           : (str)
        ○ spec                  : (Pyxis1TOPyxis2SPEC) the object describing how
                                  the Pyxis1 objects will be transform into
                                  Pyxis2 objects.
        ○ to_be_applied_to      : (type) name of the target Rhp object

        methods :
        ◐ __init__(self,
                   language, processname,
                   to_be_applied_to,
                   output_rhpobject_name,
                   spec)
        ○ __str__(self)
        ● read(self, target_rhp, text0)
        ○ uniquename(self)
   """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 processname,
                 to_be_applied_to,
                 output_rhpobject_name,
                 spec):
        """
            ProcessXXXPyxis1ToPyxis2.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ language                  : (str) ISO 639-3 name of the language of
                                          self, "" if irrelevant.
            ▪ processname               : (str)
            ▪ to_be_applied_to          : (type) name of the target Rhp object
            ▪ output_rhpobject_name     : (type) the name of the Rhp object to
                                          be added.
            ▪ spec                      : a Pyxis1TOPyxis2SPEC object
        """
        Process.__init__(self,
                         language=language,
                         processname=processname,
                         to_be_applied_to=to_be_applied_to,
                         output_rhpobject_name=output_rhpobject_name,
                         spec=spec)

    #///////////////////////////////////////////////////////////////////////////
    def read(self,
             target_rhp,
             text0):
        """
            ProcessXXXPyxis1ToPyxis2.read()
            ____________________________________________________________________

            Apply a process to the Rhp object <target_rhp>, the initial source
            text being <text0>.
            ____________________________________________________________________

            ARGUMENTS:
            ▪ target_rhp    : the Rhp object whom self is applied.
            ▪ text0         : (str) the initial source text

            RETURNED VALUE : the list of the <new_object> objects to be added.
        """
        res = LRhp() # a list of <.output_rhpobject_name>
        text = target_rhp.text  # text is a LPyxis object

        for pyxis in text:
            if len(res) == 0:
                res.append(self.output_rhpobject_name(text0=text0,
                                                      ending_punc=target_rhp.ending_punc))

            conversion_done = False

            # (type)dest_type, Pyxis1TOPyxis2SPECSVK object :
            for dest_type, svk in self.spec.items():
                if pyxis.pyxisname == svk.src_pyxisname:

                    if svk.value_in_details is None or \
                       pyxis.details[svk.value_in_details] in svk.keys_in_details:

                        new_pyxis2 = dest_type(details=pyxis.details)
                        new_pyxis2.add_a_subpyxis(pyxis)

                        for rhp5 in res:
                            rhp5.text[new_pyxis2.get_hashvalue()] = new_pyxis2.clone()

                            # we have to update the _text0reportstr attribute :
                            rhp5.set_text0reportstr()

                        conversion_done = True

            if not conversion_done:
                LOGGER.error("[%s] Don't know what to do with : " \
                             "{%s};\nself.spec={%s}",
                             self.processname,
                             pyxis,
                             self.spec)

        return res

################################################################################
#    ProcessXXXgluespSPEC class
#    ________________________________________________________________________
#
#    ProcessXXXgluespSPEC  : class used by ProcessXXXgluesp to store the
#    two informations : {pyxisobject_to_be_sticked,
#                        matching_keys,
#                       }
#
#    about the format of the ProcessXXXgluespSPEC:
#    ˮ
#    ˮ     pyxisobject_to_be_sticked   : (type)
#    ˮ     matching_keys               : (a list of str)
#    ˮ
#    ˮ example : to stick on together two Pyxis2FRAng having the same
#    ˮ "number" and the same "case" :
#    ˮ ProcessXXXgluespSPEC{(
#    ˮ              pyxisobject_to_be_sticked=Pyxis2FRAng,
#    ˮ              matching_keys=("number", "case")
#    ˮ           )}
#    ˮ
#    ____________________________________________________________________
#
#    instance attributes :
#    ● pyxisobject_to_be_sticked     : Pyxis2 object to be searched at
#                                      the beginning and the end of a
#                                      string.
#    ● matching_keys                 : (a list of str) keys in details
#                                      that have to be equal to the
#                                      first and last Pyxis2 object.
ProcessXXXgluespSPEC = collections.namedtuple("ProcessXXXgluespSPEC",
                                              ['pyxisobject_to_be_sticked',
                                               'matching_keys'])

################################################################################
class ProcessXXXgluesp(Process):
    """
        ProcessXXXgluesp class : glue [requiring] spaces [between the Pyxis2
                                 objects to be sticked on together]
        ________________________________________________________________________

        about ProcessXXXgluesp:
        ˮ a language independant class : group together two Pyxis2
        ˮ objects separated by one or several spaces.
        ˮ The transformation is described by the .specifications attribute, a
        ˮ ProcessXXXgluespSPEC object.
        ˮ
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ○ language              : (str) ISO 639-3 name of the language of self,
        ○ output_rhpobject_name : (type) the name of the Rhp object to be added
        ○ processname           : (str)
        ○ spec                  : (ProcessXXXgluespSPEC) the object describing what
                                  Pyxis2 have to be sticked on together.
        ○ to_be_applied_to      : (type) name of the target Rhp object

        methods :
        ◐ __init__(self,
                   language, processname,
                   to_be_applied_to,
                   output_rhpobject_name, spec)
        ○ __str__(self)
        ● read(self, target_rhp, text0)
        ● read__add(self, res, text0, target_rhp, lpyxis_to_be_sticked)
        ○ uniquename(self)
   """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 processname,
                 to_be_applied_to,
                 output_rhpobject_name,
                 spec):
        """
            ProcessXXXgluesp.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ language                  : (str) ISO 639-3 name of the language of
                                          self, "" if irrelevant.
            ▪ processname               : (str)
            ▪ to_be_applied_to          : (type) name of the target Rhp object
            ▪ output_rhpobject_name     : (type) the name of the Rhp object to
                                          be added.
            ▪ spec                      : a ProcessXXXgluespSPEC object
        """
        Process.__init__(self,
                         language=language,
                         processname=processname,
                         to_be_applied_to=to_be_applied_to,
                         output_rhpobject_name=output_rhpobject_name,
                         spec=spec)

    #///////////////////////////////////////////////////////////////////////////
    def read(self,
             target_rhp,
             text0):
        """
            ProcessXXXgluesp.read()
            ____________________________________________________________________

            Apply a process to the Rhp object <target_rhp>, the initial source
            text being <text0>.
            ____________________________________________________________________

            ARGUMENTS:
            ▪ target_rhp    : the Rhp object whom the self is applied.
            ▪ text0         : (str) the initial source text

            RETURNED VALUE : a list of Rhp*** objects.
        """
        text = target_rhp.text  # <text> is a LPyxis object

        # (1/2) reading of <target_rhp.text> : if two Pyxis matching what's
        # required in .spec are detected, <found> will be set to True
        # and <lpyxis_to_be_sticked> will store the Pyxis2 to be sticked on together.
        found = False   # True if the Pyxis to be sticked on together have been found
        lpyxis_to_be_sticked = LPyHashvalues()

        # main loop : let's search two Pyxis matching what's required by .spec :
        for pyxis_hashvalue in text:
            pyxis = text[pyxis_hashvalue]

            # (a Pyxis2 object, not a hash value) the very first Pyxis of lpyxis_to_be_sticked
            first_pyxis = None

            # let's initialize first_pyxis if there's something in <lpyxis_to_be_sticked> :
            if len(lpyxis_to_be_sticked) > 0:
                first_pyxis = text[lpyxis_to_be_sticked[0]]

            # e.g. if <pyxis> is a Pyxis2FRAng object as required :
            if pyxis.pyxisname == self.spec.pyxisobject_to_be_sticked.__name__:

                # Are all the .details[matching key] equal on first_pyxis and in pyxis ?
                matching_keys = True
                if first_pyxis is None:
                    # we can't match the required content of .details[key]
                    # for key in <matching_keys> :
                    matching_keys = False
                else:
                    # let's try if the .details[key] for key in matching_keys
                    # are equal in <first_pyxis> and in <pyxis> :
                    for key in self.spec.matching_keys:
                        if first_pyxis.details[key] != pyxis.details[key]:
                            matching_keys = False
                            break

                if len(lpyxis_to_be_sticked) == 0:
                    # let's add this <pyxis>, whatever its details : indeed, its
                    # pyxisname is what's required by .spec.pyxisobject_to_be_sticked
                    # and it's the first pyxis to be found and to be added
                    # in <lpyxis_to_be_sticked> :
                    lpyxis_to_be_sticked.append(pyxis.get_hashvalue())
                elif first_pyxis.pyxisname == self.spec.pyxisobject_to_be_sticked.__name__ and \
                     matching_keys is True:
                    # let'add the <pyxis> : it's pyxisname is allright as its .details :
                    found = True
                    lpyxis_to_be_sticked.append(pyxis_hashvalue)
                    break
                else:
                    # other cases : let's drop this pyxis :
                    lpyxis_to_be_sticked = LPyHashvalues()
            else:
                if len(lpyxis_to_be_sticked) > 0 and pyxis.is_a_space():
                    # the current <pyxis> is a space and it's not the first Pyxis2
                    # to be added to <lpyxis_to_be_sticked> : so it's ok, we can
                    # keep it.
                    lpyxis_to_be_sticked.append(pyxis.get_hashvalue())
                else:
                    # other cases : let's drop this pyxis :
                    lpyxis_to_be_sticked = LPyHashvalues()

        # (2/2) if two Pyxis have been found, let's create a new Rhp object to
        #       be added in <res> :
        res = LRhp() # a list of <.output_rhpobject_name>

        if found:
            res.extend(self.read__add(res,
                                      text0,
                                      target_rhp,
                                      lpyxis_to_be_sticked))

        return res

    #///////////////////////////////////////////////////////////////////////////
    def read__add(self, res, text0, target_rhp, lpyxis_to_be_sticked):
        """
            ProcessXXXgluesp.read__add()
            ____________________________________________________________________

            a subfunction of ProcessXXXgluesp.read(); this method is called
            when something has been found by .read() and needs to be added.

            Create a list of Rhp*** objects; add <lpyxis_to_be_sticked> in
            <res> and return <res>.
            ____________________________________________________________________

            ARGUMENTS:
            ▪ target_rhp           : a LRhp() object
            ▪ text0                : (str) the initial source text
            ▪ target_rhp           : the Rhp object whom the self is applied.
            ▪ lpyxis_to_be_sticked : (LPyHashvalues) the Pyxis objects to
                                     be added.

            RETURNED VALUE : a list of Rhp*** objects.
        """
        text = target_rhp.text
        first_pyxis = text[lpyxis_to_be_sticked[0]]

        res = LRhp() # a list of <.output_rhpobject_name>

        # the Rhp object to be added in <res> :
        new_rhp = self.output_rhpobject_name(text0=text0,
                                             ending_punc=target_rhp.ending_punc)

        # let's copy in new_pyxis2 the expected keys :
        new_pyxis2__details = DI()
        for key in self.spec.matching_keys:
            new_pyxis2__details[key] = first_pyxis.details[key]

        new_pyxis2 = self.spec.pyxisobject_to_be_sticked(details=new_pyxis2__details)

        # making of the <new_pyxis2> object :
        # we have to fill it from <lpyxis_to_be_sticked> before we may
        # insert it :
        for pyxis_hashvalue in lpyxis_to_be_sticked:
            for subpyxis in text[pyxis_hashvalue].subpyxis:
                new_pyxis2.subpyxis.append(subpyxis)

        # insertion in new_rhp :

        # flag : the new pyxis2 has not been yet added.
        new_pyxis2_has_been_added = False

        for pyxis_hashvalue in text:
            if pyxis_hashvalue not in lpyxis_to_be_sticked:
                new_rhp.text[pyxis_hashvalue] = text[pyxis_hashvalue]
            else:
                if not new_pyxis2_has_been_added:
                    new_rhp.text[new_pyxis2.get_hashvalue()] = new_pyxis2
                    new_pyxis2_has_been_added = True

        # todo we have to update ._text0reportstr :
        new_rhp.set_text0reportstr()

        # let's add to <res> our new rhp :
        res.append(new_rhp)

        return res

################################################################################
class ProcessFRA1(ProcessXXXnormalize):
    """
        ProcessFRA1 class
        ________________________________________________________________________

        (French) use ProcessFRA1 to normalize strings.

        ▪ Read a RhpFRA1 object and normalize its content.
        ▪ Add a unique RhpFRA2 object.

        about Process classes for French:
        ˮ ▪ ProcessFRA : mother class of all ProcessFRA*** classes : Ancient Greek
        ˮ ▪ ProcessFRA0 - reads Rhp0
        ˮ               -- cuts the text along the punctuation
        ˮ               --- creates RhpFRA1
        ˮ ▪ ProcessFRA1 - reads RhpFRA1
        ˮ               -- normalizes the text
        ˮ               --- creates RhpFRA2
        ˮ ▪ ProcessFRA2 - reads RhpFRA2
        ˮ               -- gets the morphological analysis
        ˮ               --- creates RhpFRA3
        ˮ ▪ ProcessFRA3 - reads RhpFRA3
        ˮ               -- groups together Pyxis into sentences
        ˮ               --- creates RhpFRA4
        ˮ ▪ ProcessFRA4 - reads RhpFRA4
        ˮ               -- Pyxis1FRAword > Pyxis2FRA***
        ˮ               --- creates RhpFRA5
        ____________________________________________________________________

        no class attribute

        instance attributes :
        ○ language              : (str) ISO 639-3 name of the
                                  language of self,
        ○ output_rhpobject_name : the type added by the .read()
                                  method. Should be an Rhp*** object.
        ○ processname           : (str)
        ○ spec                  : (None, undefined)
        ○ to_be_applied_to      : (type) object read by the process.

        methods :
        ◐ __init__(self)
        ○ __str__(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
            ProcessFRA1.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        ProcessXXXnormalize.__init__(self,
                                     language="fra",
                                     processname="ProcessFRA1",
                                     to_be_applied_to=RhpFRA1,
                                     output_rhpobject_name=RhpFRA2)

################################################################################
class ProcessFRA2(ProcessXXXmorpho):
    """
        ProcessFRA2 class
        ________________________________________________________________________

        (French) use ProcessFRA2 to get the morphological analysis of
        strings.

        ▪ Read a RhpFRA2 object and add informations about its morphological
          analysis.
        ▪ Add one or more RhpFRA3 objects.

        about Process classes for French:
        ˮ ▪ ProcessFRA : mother class of all ProcessFRA*** classes : Ancient Greek
        ˮ ▪ ProcessFRA0 - reads Rhp0
        ˮ               -- cuts the text along the punctuation
        ˮ               --- creates RhpFRA1
        ˮ ▪ ProcessFRA1 - reads RhpFRA1
        ˮ               -- normalizes the text
        ˮ               --- creates RhpFRA2
        ˮ ▪ ProcessFRA2 - reads RhpFRA2
        ˮ               -- gets the morphological analysis
        ˮ               --- creates RhpFRA3
        ˮ ▪ ProcessFRA3 - reads RhpFRA3
        ˮ               -- groups together Pyxis into sentences
        ˮ               --- creates RhpFRA4
        ˮ ▪ ProcessFRA4 - reads RhpFRA4
        ˮ               -- Pyxis1FRAword > Pyxis2FRA***
        ˮ               --- creates RhpFRA5
        ____________________________________________________________________

        no class attribute

        instance attributes :
        ○ language              : (str) ISO 639-3, set to "fra"
                                  by the mother-class
        ○ output_rhpobject_name : the type added by the .read()
                                  method. Should be an Rhp*** object.
        ○ processname           : (str) name of the current
                                  process.
        ○ punctuation_symbols   : a list of str
        ○ spec                  : (ProcessXXXmorphoSPEC)
        ○ to_be_applied_to      : (type) object read by the process.

        methods :
        ◐ __init__(self)
        ○ __str__(self)
        ○ read(self, target_rhp, text0)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
            ProcessFRA2.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        ProcessXXXmorpho.__init__(self,
                                  language="fra",
                                  processname="ProcessFRA2",
                                  to_be_applied_to=RhpFRA2,
                                  output_rhpobject_name=RhpFRA3,
                                  spec=ProcessXXXmorphoSPEC(pyxis1_word=Pyxis1FRAword,
                                                            pyxis1_punctuation=Pyxis1FRApunctuation,
                                                            pyxis1_unknown=Pyxis1FRAunknown))

################################################################################
class ProcessFRA3(ProcessXXXsentences):
    """
        ProcessFRA3 class
        ________________________________________________________________________

        (French) use ProcessFRA3 to group together Pyxis objects into
        sentences.

        ▪ Read a RhpFRA3 object and cut it into sentences.
        ▪ Add one or more RhpFRA4 objects.

        about Process classes for French:
        ˮ ▪ ProcessFRA : mother class of all ProcessFRA*** classes : Ancient Greek
        ˮ ▪ ProcessFRA0 - reads Rhp0
        ˮ               -- cuts the text along the punctuation
        ˮ               --- creates RhpFRA1
        ˮ ▪ ProcessFRA1 - reads RhpFRA1
        ˮ               -- normalizes the text
        ˮ               --- creates RhpFRA2
        ˮ ▪ ProcessFRA2 - reads RhpFRA2
        ˮ               -- gets the morphological analysis
        ˮ               --- creates RhpFRA3
        ˮ ▪ ProcessFRA3 - reads RhpFRA3
        ˮ               -- groups together Pyxis into sentences
        ˮ               --- creates RhpFRA4
        ˮ ▪ ProcessFRA4 - reads RhpFRA4
        ˮ               -- Pyxis1FRAword > Pyxis2FRA***
        ˮ               --- creates RhpFRA5
        ___________________________________________________________________

        no class attribute

        instance attributes :
        ○ language              : (str) ISO 639-3, set to "fra"
                                  by the mother-class
        ○ output_rhpobject_name : the type added by the .read()
                                  method. Should be an Rhp*** object.
        ○ processname           : (str) name of the current
                                  process.
        ○ spec                  : (None, undefined)
        ○ to_be_applied_to      : (type) object read by the process.

        methods :
        ○ __init__(self)
        ○ __str__(self)
        ○ read(self, target_rhp, text0)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
            ProcessFRA3.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        ProcessXXXsentences.__init__(self,
                                     language="fra",
                                     processname="ProcessFRA3",
                                     to_be_applied_to=RhpFRA3,
                                     output_rhpobject_name=RhpFRA4)

################################################################################
class ProcessFRA4(ProcessXXXPyxis1ToPyxis2):
    """
        ProcessFRA4 class
        ________________________________________________________________________

        Read a RhpFRA4 object and convert the Pyxis1FRAword into Pyxis2*** objects
        Add one or more RhpFRA5 objects.

        about Process classes for French:
        ˮ ▪ ProcessFRA : mother class of all ProcessFRA*** classes : Ancient Greek
        ˮ ▪ ProcessFRA0 - reads Rhp0
        ˮ               -- cuts the text along the punctuation
        ˮ               --- creates RhpFRA1
        ˮ ▪ ProcessFRA1 - reads RhpFRA1
        ˮ               -- normalizes the text
        ˮ               --- creates RhpFRA2
        ˮ ▪ ProcessFRA2 - reads RhpFRA2
        ˮ               -- gets the morphological analysis
        ˮ               --- creates RhpFRA3
        ˮ ▪ ProcessFRA3 - reads RhpFRA3
        ˮ               -- groups together Pyxis into sentences
        ˮ               --- creates RhpFRA4
        ˮ ▪ ProcessFRA4 - reads RhpFRA4
        ˮ               -- Pyxis1FRAword > Pyxis2FRA***
        ˮ               --- creates RhpFRA5
        ____________________________________________________________________

        class attribute :
        ○ pyxis1topyxis2spec    : (dict) see the documentation below

        instance attributes :
        ○ language              : (str) ISO 639-3 name of the language of self,
        ○ output_rhpobject_name : the type added by the .read()
                                  method. Should be an Rhp*** object.
        ○ processname           : (str)
        ○ spec                  : (different types, None if undefined)
                                  specifications describing the way the process
                                  does its job.
        ○ to_be_applied_to      : (type) name of the target Rhp object

        methods :
        ◐ __init__(self)
        ○ __str__(self)
        ● read(self, target_rhp, text0)
        ○ uniquename(self)
    """

    # about the dict given to Pyxis1TOPyxis2SPEC.__init__():
    # ˮ { (type)dest_type : ((str)src_pyxisname,
    # ˮ                      (str)value_in_details,
    # ˮ                      (list of str)keys_in_details) }
    # ˮ
    # ˮ by example :
    # ˮ             { Pyxis2GRCng : ("Pyxis1GRCword",
    # ˮ                              "grammatical nature",
    # ˮ                              ("common noun",))
    # ˮ             }
    # ˮ
    pyxis1topyxis2spec = Pyxis1TOPyxis2SPEC({
        Pyxis2FRAng : ("Pyxis1FRAword",
                       "nature grammaticale",
                       ("nom commun", "déterminant.article défini")),

        Pyxis2FRAvs : ("Pyxis1FRAword",
                       "nature grammaticale",
                       ("verbe",)),

        Pyxis2FRApunctuation    : ("Pyxis1FRApunctuation", None, ()),
        Pyxis2FRAunknown        : ("Pyxis1FRAunknown", None, ()),
    })

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
            ProcessFRA4.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        ProcessXXXPyxis1ToPyxis2.__init__(self,
                                          language="fra",
                                          processname="ProcessFRA4",
                                          to_be_applied_to=RhpFRA4,
                                          output_rhpobject_name=RhpFRA5,
                                          spec=ProcessFRA4.pyxis1topyxis2spec)

################################################################################
class ProcessFRA5ng(ProcessXXXgluesp):
    """
        ProcessFRA5ng class
        ________________________________________________________________________

        Read a RhpFRA5 object and stick on together Pyxis2FRAng objects if
        they are grammatically equivalent and if one or more spaces lie
        between them.

        about Process classes for French:
        ˮ ▪ ProcessFRA : mother class of all ProcessFRA*** classes : Ancient Greek
        ˮ ▪ ProcessFRA0 - reads Rhp0
        ˮ               -- cuts the text along the punctuation
        ˮ               --- creates RhpFRA1
        ˮ ▪ ProcessFRA1 - reads RhpFRA1
        ˮ               -- normalizes the text
        ˮ               --- creates RhpFRA2
        ˮ ▪ ProcessFRA2 - reads RhpFRA2
        ˮ               -- gets the morphological analysis
        ˮ               --- creates RhpFRA3
        ˮ ▪ ProcessFRA3 - reads RhpFRA3
        ˮ               -- groups together Pyxis into sentences
        ˮ               --- creates RhpFRA4
        ˮ ▪ ProcessFRA4 - reads RhpFRA4
        ˮ               -- Pyxis1FRAword > Pyxis2FRA***
        ˮ               --- creates RhpFRA5
        ____________________________________________________________________

        no class attribute

        instance attributes :
        ○ language              : (str) ISO 639-3 name of the language of self,
        ○ output_rhpobject_name : the type added by the .read()
                                  method. Should be an Rhp*** object.
        ○ processname           : (str)
        ○ spec                  : (different types, None if undefined)
                                  specifications describing the way the process
                                  does its job.
        ○ to_be_applied_to      : (type) name of the target Rhp object

        methods :
        ◐ __init__(self)
        ○ __str__(self)
        ○ read(self, target_rhp, text0)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
            ProcessFRA5ng.__init__()
            ____________________________________________________________________

            about the format of the ProcessXXXgluespSPEC:
            ˮ
            ˮ     pyxisobject_to_be_sticked   : (type)
            ˮ     matching_keys               : (a list of str)
            ˮ
            ˮ example : to stick on together two Pyxis2FRAng having the same
            ˮ "number" and the same "case" :
            ˮ ProcessXXXgluespSPEC{(
            ˮ              pyxisobject_to_be_sticked=Pyxis2FRAng,
            ˮ              matching_keys=("number", "case")
            ˮ           )}
            ˮ
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        ProcessXXXgluesp.__init__(self,
                                  language="fra",
                                  processname="ProcessFRA5ng",
                                  to_be_applied_to=RhpFRA5,
                                  output_rhpobject_name=RhpFRA5,
                                  spec=ProcessXXXgluespSPEC(pyxisobject_to_be_sticked=Pyxis2FRAng,
                                                            matching_keys=("genre", "nombre")),)

################################################################################
class ProcessGRC5ng(ProcessXXXgluesp):
    """
        ProcessGRC5ng class
        ________________________________________________________________________

        Read a RhpGRC5 object and stick on together Pyxis2GRCng objects if
        they are grammatically equivalent and if one or more spaces lie
        between them.

        about Process classes for Ancient Greek:
        ˮ ▪ ProcessGRC : mother class of all ProcessGRC*** classes : Ancient Greek
        ˮ ▪ ProcessGRC0 - reads Rhp0
        ˮ               -- cuts the text along the punctuation
        ˮ               --- creates RhpGRC1
        ˮ ▪ ProcessGRC1 - reads RhpGRC1
        ˮ               -- normalizes the text
        ˮ               --- creates RhpGRC2
        ˮ ▪ ProcessGRC2 - reads RhpGRC2
        ˮ               -- gets the morphological analysis
        ˮ               --- creates RhpGRC3
        ˮ ▪ ProcessGRC3 - reads RhpGRC3
        ˮ               -- groups together Pyxis into sentences
        ˮ               --- creates RhpGRC4
        ˮ ▪ ProcessGRC4 - reads RhpGRC4
        ˮ               -- Pyxis1GRCword > Pyxis2GRC***
        ˮ               --- creates RhpGRC5
        ____________________________________________________________________

        no class attribute

        instance attributes :
        ○ language              : (str) ISO 639-3 name of the language of self,
        ○ output_rhpobject_name : the type added by the .read()
                                  method. Should be an Rhp*** object.
        ○ processname           : (str)
        ○ spec                  : (different types, None if undefined)
                                  specifications describing the way the process
                                  does its job.
        ○ to_be_applied_to      : (type) name of the target Rhp object

        methods :
        ◐ __init__(self)
        ○ __str__(self)
        ○ read(self, target_rhp, text0)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
            ProcessGRC5ng.__init__()
            ____________________________________________________________________

            about the format of the ProcessXXXgluespSPEC:
            ˮ
            ˮ     pyxisobject_to_be_sticked   : (type)
            ˮ     matching_keys               : (a list of str)
            ˮ
            ˮ example : to stick on together two Pyxis2FRAng having the same
            ˮ "number" and the same "case" :
            ˮ ProcessXXXgluespSPEC{(
            ˮ              pyxisobject_to_be_sticked=Pyxis2FRAng,
            ˮ              matching_keys=("number", "case")
            ˮ           )}
            ˮ
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        ProcessXXXgluesp.__init__(self,
                                  language="grc",
                                  processname="ProcessGRC5ng",
                                  to_be_applied_to=RhpGRC5,
                                  output_rhpobject_name=RhpGRC5,
                                  spec=ProcessXXXgluespSPEC(pyxisobject_to_be_sticked=Pyxis2GRCng,
                                                            matching_keys=("genre", "nombre")),)

################################################################################
class LRhp(list):
    """
        LRhp class
        ________________________________________________________________________

        a list of Rhp** objects
        ________________________________________________________________________

        no class attribute

        no instance attribute :

        methods :
        ◐ __init__(self)
        ● uniquenames(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
            LRhp.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE
        """
        list.__init__(self)

    #///////////////////////////////////////////////////////////////////////////
    def uniquenames(self):
        """
            LRhp.uniquenames()
            ____________________________________________________________________

            (debug oriented method)
            Return a short identification of self, i.e. a list of the uniquename
            of each element in self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : the expected string
        """
        res = []
        for rhp in self:
            res.append(rhp.uniquename())
        return "["+";".join(res)+"]"

################################################################################
class RhpContainer(dict):
    """
        RhpContainer class
        ________________________________________________________________________

        use this object to store Rhp objects. Please use the add() method,
        do not directly access the members !

        dict : (byte)rhphashvalue → Rhp*** object
        ________________________________________________________________________

        no class attribute

        no instance attribute

        methods :
        ○ __init__(self)
        ○ __str__(self)
        ● add(self, rhp_object)
        ● report(self, just=None)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
            RhpContainer.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        dict.__init__(self)

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
            RhpContainer.__str__()
            ___________________________________________________________________

            Return a human-readable representation of self.
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        res = []
        for rhphashvalue in sorted(self,
                                   key=lambda rhphashvalue: self[rhphashvalue].uniquename()):

            res.append("{0}".format(self[rhphashvalue]))

        return "\n".join(res)

    #///////////////////////////////////////////////////////////////////////////
    def add(self,
            rhp_object):
        """
            RhpContainer.add()
            ____________________________________________________________________

            Add rhp_object to self : if rhp_object is not already present in
            self, it is added; otherwise rhp_object is skipped.
            ____________________________________________________________________

            ARGUMENT:
            ▪ rhp_object : a Rhp*** objet

            no RETURNED VALUE.
        """
        rhp_object__hashvalue = rhp_object.get_hashvalue()
        if rhp_object__hashvalue in self:
            LOGGER.info("Skipped an Rhp object, already in self : %s - %s",
                        rhp_object.rhpname,
                        hashvalue2hex(rhp_object__hashvalue))
        else:
            LOGGER.info("Let's add a new rhp : "+str(rhp_object))
            self[rhp_object.get_hashvalue()] = rhp_object

    #///////////////////////////////////////////////////////////////////////////
    def report(self,
               just=None,
               margin=""):
        """
            RhpContainer.report()
            ____________________________________________________________________

            Return a string describing self in a more friendly way than
            __str__() does, including colored segments of text.
            ____________________________________________________________________

            ARGUMENT:
            ▪ just      : (None/str) list of the Rhp types to be displayed or
                          None if all the Rhp types have to be displayed.

            RETURNED VALUE : the expected string.
        """
        res = []

        # number of reading hypothese(s) :
        if len(self) == 0:
            res.append("no reading hypothese :")
        elif len(self) == 1:
            res.append("One reading hypothese :")
        else:
            res.append("{0} reading hypotheses :".format(len(self)))

        # list of all reading hypothese(s) :
        for rhp_hashvalue in sorted(self,
                                    key=lambda rhphashvalue: self[rhphashvalue].uniquename()):

            if just is None or self[rhp_hashvalue].rhpname in just:
                res.append(add_prefix_before_line("  ", self[rhp_hashvalue].report()))

        # what's the best reading hypothese ?
        best_interest = [0, None]   # (float)interest, (byte)rhp_hashvalue
        for rhp_hashvalue in self:
            if self[rhp_hashvalue].get_interest() > best_interest[0]:
                best_interest[0] = self[rhp_hashvalue].get_interest()
                best_interest[1] = rhp_hashvalue
        res.append("! best reading hypothese : {0} .".format(self[best_interest[1]].uniquename()))
        res.append(add_prefix_before_line("! ", self[best_interest[1]].report()))

        return add_prefix_before_line(margin, "\n".join(res))

################################################################################
class Rhp(object):
    """
        Rhp class
        ________________________________________________________________________

        Mother-class for all the Rhp*** classes.

        about Rhp classes:
        ˮ Use an Rhp (Reading Hypothesis) class to store an analyse of a
        ˮ textual segment.
        ˮ
        ˮ Method expected : .set_hashvalue(), .clone(), .report() ....
        ˮ
        ˮ ▪ (Rhp : mother class of all Rhp*** classes)
        ˮ
        ˮ ▪ Rhp0 : raw text, to be read by ProcessFRA0 (raw text in .text0)
        ˮ ▪ RhpXXXblurwords : store words roughly cut
        ˮ ▪ RhpXXXnormalization : store a normalized text in a LCharAndTextPos object
        ˮ ▪ RhpXXXmorpho : store Pyxis objects with morphological analysis
        ˮ ▪ RhpXXXsentences : store Pyxis objects grouped together into sentences
        ˮ
        ˮ Ancient Greek :
        ˮ ▪ (RhpGRC : mother class of all RhpGRC*** classes)
        ˮ
        ˮ French :
        ˮ ▪ (RhpFRA : mother class of all RhpFRA*** classes)
        ________________________________________________________________________

        class attribute
        ● default_interest      : (float) default value for ._interest

        instance attributes :
        ● _hashvalue            : (bytes or None)
                                  Use .get_hashvalue() to read its value.
        ● _interest             : (float) numerical interest of self
                                  Use .get_interest() to read its value.
        ● language              : (str) ISO 639-3 name of the language of self,
                                  "" if irrelevant
        ● text0                 : (str) the initial source text
        ● rhpname               : (str)

        methods :
        ● __eq__(self, other)
        ● __init__(self, rhpname, text0)
        ● get_hashvalue(self)
        ● get_interest(self)
        ● set_hashvalue(self) (faked method, see above)
        ● uniquename(self)
    """
    default_interest = 1.0

    #///////////////////////////////////////////////////////////////////////////
    def __eq__(self,
               other):
        """
            Rhp.__eq__()
            ____________________________________________________________________

            Return true if self==other, False otherwise.
            ____________________________________________________________________

            ARGUMENT:
            ▪ other : an Rhp object.

            RETURNED VALUE : the expected boolean
        """
        return self.get_hashvalue() == other.get_hashvalue()

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 rhpname,
                 text0):
        """
            Rhp.__init__()
            ___________________________________________________________________

            nota bene : as expected for a class with a _hashvalue attribute,
            _hashvalue is set to None in the __init__() method.
            ___________________________________________________________________

            ARGUMENTS:
            ▪ language              : (str)language name (ISO 639-3) or None if
                                      irrelevant
            ▪ rhpname               : (str)
            ▪ text0                 : (str) the initial source text

            no RETURNED VALUE
        """
        self.language = language
        self.rhpname = rhpname
        self.text0 = text0
        # about .interest : temporary initialization, see .get_interest()
        self._interest = Rhp.default_interest
        self._hashvalue = None

    #///////////////////////////////////////////////////////////////////////////
    def get_hashvalue(self):
        """
            Rhp.get_hashvalue()
            ___________________________________________________________________

            Compute the value of ._hashvalue if necessary and return it.
            ___________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : self._hashvalue
        """
        if self._hashvalue is None:
            self.set_hashvalue()
        return self._hashvalue

    #///////////////////////////////////////////////////////////////////////////
    def get_interest(self):
        """
            Rhp.get_interest()
            ___________________________________________________________________

            Compute the value of ._interest and return it.
            ___________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : (float) self._interest
        """
        self._interest = Rhp.default_interest
        return self._interest

    #///////////////////////////////////////////////////////////////////////////
    def set_hashvalue(self):
        """
            Rhp.set_hashvalue()
            ____________________________________________________________________

            Compute the value of ._hashvalue if necessary and return it.

            Fake code, just here to avoid the following error from Pylint in the
            self.get_hashvalue() method :

              "Instance of 'Rhp' has no 'set_hashvalue' member (no-member)"

            how to write a set_hashvalue() for an Rhp class ? A set_hashvalue()
            method initializes the ._hashvalue instance attribute, hence :

                        hasher = HASHER()
                        hasher.update(self.language.encode())
                        hasher.update(self.rhpname.encode())
                        hasher.update(self.text0.encode())
                        ... several calls to hasher.update() ...
                        self._hashvalue = hasher.digest()
            ____________________________________________________________________
        """
        raise NotImplementedError

    #///////////////////////////////////////////////////////////////////////////
    def uniquename(self):
        """
            Rhp.uniquename()
            ____________________________________________________________________

            (debug oriented method)
            Return a short identification of self
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : the expected string
        """
        return "{0}({1})".format(self.rhpname,
                                 hashvalue2hex(self.get_hashvalue()))

################################################################################
class Rhp0(Rhp):
    """
        Rhp0 class
        ________________________________________________________________________

        "Raw text" class. Use this class to store the input text to be read.

        ✓ unittests : see the Rhp0Test class.

        about Rhp classes:
        ˮ Use an Rhp (Reading Hypothesis) class to store an analyse of a
        ˮ textual segment.
        ˮ
        ˮ Method expected : .set_hashvalue(), .clone(), .report() ....
        ˮ
        ˮ ▪ (Rhp : mother class of all Rhp*** classes)
        ˮ
        ˮ ▪ Rhp0 : raw text, to be read by ProcessFRA0 (raw text in .text0)
        ˮ ▪ RhpXXXblurwords : store words roughly cut
        ˮ ▪ RhpXXXnormalization : store a normalized text in a LCharAndTextPos object
        ˮ ▪ RhpXXXmorpho : store Pyxis objects with morphological analysis
        ˮ ▪ RhpXXXsentences : store Pyxis objects grouped together into sentences
        ˮ
        ˮ Ancient Greek :
        ˮ ▪ (RhpGRC : mother class of all RhpGRC*** classes)
        ˮ
        ˮ French :
        ˮ ▪ (RhpFRA : mother class of all RhpFRA*** classes)
        ________________________________________________________________________

        class attribute :
        ◐ default_interest      : (float) default value for ._interest

        instance attributes :
        ○ _hashvalue            : (bytes or None)
                                  Use .get_hashvalue() to read its value.
        ○ _interest             : (float) numerical interest of self
                                  Use .get_interest() to read its value.
        ○ language              : (str) ISO 639-3 name of the
                                  language of self set to "" since this attribute
                                  is irrelevant to self
        ○ rhpname               : (str)
        ○ text0                 : (str) the initial source text

        methods :
        ○ __eq__(self, other)
        ◐ __init__(self, text0)
        ● __str__(self)
        ● clone(self)
        ○ get_hashvalue(self)
        ◐ get_interest(self)
        ● report(self)
        ● set_hashvalue(self)
        ○ uniquename(self)
    """
    default_interest = 2.0

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 text0):
        """
            Rhp0.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENT:
            ▪ text0                  : (str) the initial source text

            no RETURNED VALUE
        """
        Rhp.__init__(self,
                     text0=text0,
                     language="",
                     rhpname="Rhp0")

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
            Rhp0.__str__()
            ____________________________________________________________________

            Return a human-readable representation of self.
            ____________________________________________________________________

            RETURNED VALUE : a human-readable string
        """
        return "{0} {1} - {2} : text='{3}'".format(RHP_SYMB,
                                                   self.rhpname,
                                                   hashvalue2hex(self.get_hashvalue()),
                                                   self.text0)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Rhp0.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(text0=self.text0)

    #///////////////////////////////////////////////////////////////////////////
    def get_interest(self):
        """
            Rhp0.get_interest()
            ___________________________________________________________________

            Compute the value of ._interest and return it.
            ___________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : (float) self._interest
        """
        self._interest = Rhp0.default_interest
        return self._interest

    #///////////////////////////////////////////////////////////////////////////
    def report(self, margin=""):
        """
            Rhp0.report()
            ____________________________________________________________________

            Return a string describing self in a more friendly way than
            __str__() does, including colored segments of text.
            ____________________________________________________________________

            no ARGUMENT.

            RETURNED VALUE : the expected (str)string.
        """
        reportstr = "{0} ({1}) : " \
                    "[color1]\"{2}\"[default]".format(RHP_SYMB,
                                                      self.rhpname,
                                                      improve_reportstr_readibilty(self.text0))

        return add_prefix_before_line(margin, reportstr)

    #///////////////////////////////////////////////////////////////////////////
    def set_hashvalue(self):
        """
            Rhp0.set_hashvalue()
            ____________________________________________________________________

            Initialize the value of _hashvalue.
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        hasher = HASHER()
        hasher.update(self.language.encode())
        hasher.update(self.rhpname.encode())
        hasher.update(self.text0.encode())
        self._hashvalue = hasher.digest()

################################################################################
class RhpXXXblurwords(Rhp):
    """
        RhpXXXblurwords class
        ________________________________________________________________________

        Use RhpXXXblurwords to store words roughly cut from the input string.

        ✓ unittests : see the RhpXXXblurwordsTest class.

        about Rhp classes:
        ˮ Use an Rhp (Reading Hypothesis) class to store an analyse of a
        ˮ textual segment.
        ˮ
        ˮ Method expected : .set_hashvalue(), .clone(), .report() ....
        ˮ
        ˮ ▪ (Rhp : mother class of all Rhp*** classes)
        ˮ
        ˮ ▪ Rhp0 : raw text, to be read by ProcessFRA0 (raw text in .text0)
        ˮ ▪ RhpXXXblurwords : store words roughly cut
        ˮ ▪ RhpXXXnormalization : store a normalized text in a LCharAndTextPos object
        ˮ ▪ RhpXXXmorpho : store Pyxis objects with morphological analysis
        ˮ ▪ RhpXXXsentences : store Pyxis objects grouped together into sentences
        ˮ
        ˮ Ancient Greek :
        ˮ ▪ (RhpGRC : mother class of all RhpGRC*** classes)
        ˮ
        ˮ French :
        ˮ ▪ (RhpFRA : mother class of all RhpFRA*** classes)
        ________________________________________________________________________

        class attribute :
        ◐ default_interest      : (float) default value for ._interest

        instance attributes :
        ○ _hashvalue            : (bytes or None)
                                  Use .get_hashvalue() to read its value.
        ○ _interest             : (float) numerical interest of self
                                  Use .get_interest() to read its value.
        ○ language              : (str) ISO 639-3 name of the language
                                  of self.
        ○ rhpname               : (str)
        ● text                  : (LCharAndTextPos) main attribute : Rhp text
        ○ text0                 : (str) the initial source text

        methods :
        ○ __eq__(self, other)
        ◐ __init__(self, language, rhpname, text0, text)
        ● __str__(self)
        ● clone(self)
        ○ get_hashvalue(self)
        ◐ get_interest(self)
        ● report(self)
        ● set_hashvalue(self)
        ○ uniquename(self)
    """
    default_interest = 3.0

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 rhpname,
                 text0,
                 text):
        """
            RhpXXXblurwords.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ language              : (str) ISO 639-3 name of the language of
                                      self
            ▪ rhpname               : (str)
            ▪ text0                 : (str) the initial source text
            ▪ text                  : (LCharAndTextPos) main attribute : Rhp text

            no RETURNED VALUE
        """
        Rhp.__init__(self,
                     language=language,
                     rhpname=rhpname,
                     text0=text0)
        self.text = text

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
            RhpXXXblurwords.__str__()
            ____________________________________________________________________

            Return a human-readable representation of self.
            ____________________________________________________________________

            RETURNED VALUE : a human-readable string
        """
        return "{0} {1} - {2} :\n  text='{3}' <{4:.3f}>".format(RHP_SYMB,
                                                                self.rhpname,
                                                                hashvalue2hex(self.get_hashvalue()),
                                                                self.text,
                                                                self.get_interest())

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            RhpXXXblurwords.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(language=self.language,
                          rhpname=self.rhpname,
                          text0=self.text0,
                          text=self.text)

    #///////////////////////////////////////////////////////////////////////////
    def get_interest(self):
        """
            RhpXXXblurwords.get_interest()
            ___________________________________________________________________

            Compute the value of ._interest and return it.
            ___________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : (float) self._interest
        """
        self._interest = RhpXXXblurwords.default_interest
        return self._interest

    #///////////////////////////////////////////////////////////////////////////
    def report(self, margin=""):
        """
            RhpXXXblurwords.report()
            ____________________________________________________________________

            Return a string describing self in a more friendly way than
            __str__() does, including colored segments of text.
            ____________________________________________________________________

            no ARGUMENT.

            RETURNED VALUE : the expected (str)string.
        """
        colors = dict()
        index = 0 # to be used to alternate the colors
        for charandpos in self.text:
            for x0x1 in charandpos.textpos:
                if index == 0:
                    colors[(tuple(x0x1),)] = "[color1]"
                else:
                    colors[(tuple(x0x1),)] = "[color2]"
                index ^= 1

        colorstr = ColorStr(srcstring=improve_reportstr_readibilty(self.text0),
                            colors=colors)

        reportstr = "{0} ({1}) : \"{2}\" <{3:.3f}>".format(RHP_SYMB,
                                                           self.rhpname,
                                                           colorstr,
                                                           self.get_interest())
        return add_prefix_before_line(margin, reportstr)

    #///////////////////////////////////////////////////////////////////////////
    def set_hashvalue(self):
        """
            RhpXXXblurwords.set_hashvalue()
            ____________________________________________________________________

            Initialize the value of _hashvalue.
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        hasher = HASHER()
        hasher.update(self.language.encode())
        hasher.update(self.rhpname.encode())
        hasher.update(self.text0.encode())
        for string in self.text:
            hasher.update(string.get_hashvalue())
        self._hashvalue = hasher.digest()

################################################################################
class RhpFRA1(RhpXXXblurwords):
    """
        RhpFRA1 class
        ________________________________________________________________________

        (French) Use RhpFRA1 to store words roughly cut from the
        input string.

        ✓ unittests : see the RhpFRA1Test class.

        about Rhp classes for French:
        ˮ ▪ (RhpFRA : mother class of all RhpFRA*** classes)
        ˮ ▪ RhpFRA1 : to be read by ProcessFRA1 (text in .text, a LCharAndTextPos object)
        ˮ ▪ RhpFRA2 : to be read by ProcessFRA2 (text in .text, a LCharAndTextPos object)
        ˮ ▪ RhpFRA3 : to be read by ProcessFRA3 (text in .text, a LPyxis object)
        ˮ ▪ RhpFRA4 : to be read by ProcessFRA4 (text in .text, a LPyxis object,
        ˮ                                        + in .ending_punctuation)
        ˮ
        ________________________________________________________________________

        class attribute :
        ○ default_interest      : (float) default value for ._interest

        instance attributes :
        ○ _hashvalue            : (bytes or None)
                                  Use .get_hashvalue() to read its value.
        ○ _interest             : (float) numerical interest of self
                                  Use .get_interest() to read its value.
        ○ language              : (str) ISO 639-3 name of the language
                                  of self.
        ○ rhpname               : (str)
        ○ text                  : (LCharAndTextPos objet) main attribute :
                                  Rhp text
        ○ text0                 : (str) the initial source text

        methods :
        ○ __eq__(self, other)
        ◐ __init__(self, language="fra", rhpname="RhpFRA1", text0, text)
        ○ __str__(self)
        ○ clone(self)
        ○ get_hashvalue(self)
        ○ get_interest(self)
        ○ report(self)
        ○ set_hashvalue(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 text0,
                 text,
                 language="fra",
                 rhpname="RhpFRA1"):
        """
            RhpFRA1.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ text0                 : (str) the initial source text
            ▪ text                  : (LCharAndTextPos) main attribute : Rhp text
            ▪ language              : (str) ISO 639-3
            ▪ rhpname               : (str)

            no RETURNED VALUE
        """
        RhpXXXblurwords.__init__(self,
                                 language=language,
                                 rhpname=rhpname,
                                 text0=text0,
                                 text=text)

################################################################################
class RhpXXXnormalization(Rhp):
    """
        RhpXXXnormalization class
        ________________________________________________________________________

        Use RhpXXXnormalization to store a normalized text in a
        LCharAndTextPos object.

        ✓ unittests : see the RhpXXXnormalizationTest class.

        about Rhp classes:
        ˮ Use an Rhp (Reading Hypothesis) class to store an analyse of a
        ˮ textual segment.
        ˮ
        ˮ Method expected : .set_hashvalue(), .clone(), .report() ....
        ˮ
        ˮ ▪ (Rhp : mother class of all Rhp*** classes)
        ˮ
        ˮ ▪ Rhp0 : raw text, to be read by ProcessFRA0 (raw text in .text0)
        ˮ ▪ RhpXXXblurwords : store words roughly cut
        ˮ ▪ RhpXXXnormalization : store a normalized text in a LCharAndTextPos object
        ˮ ▪ RhpXXXmorpho : store Pyxis objects with morphological analysis
        ˮ ▪ RhpXXXsentences : store Pyxis objects grouped together into sentences
        ˮ
        ˮ Ancient Greek :
        ˮ ▪ (RhpGRC : mother class of all RhpGRC*** classes)
        ˮ
        ˮ French :
        ˮ ▪ (RhpFRA : mother class of all RhpFRA*** classes)
        ________________________________________________________________________

        class attribute :
        ◐ default_interest      : (float) default value for ._interest

        instance attributes :
        ○ _hashvalue            : (bytes or None)
                                  Use .get_hashvalue() to read its value.
        ○ _interest             : (float) numerical interest of self
                                  Use .get_interest() to read its value.
        ○ language              : (str) ISO 639-3 name of the language of self.
        ○ rhpname               : (str)
                                  Modified __init__().
        ● text                  : (LCharAndTextPos) main attribute : Rhp text
        ○ text0                 : (str) the initial source text
                                  Modified __init__().

        methods :
        ○ __eq__(self, other)
        ○ __init__(self, language, rhpname, text0, text)
        ● __str__(self)
        ● clone(self)
        ○ get_hashvalue(self)
        ◐ get_interest(self)
        ● report(self)
        ● set_hashvalue(self)
        ○ uniquename(self)
    """
    default_interest = 4.0

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 rhpname,
                 text0,
                 text):
        """
            RhpXXXnormalization.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ language              : (str) ISO 639-3 name of the language of
                                      self
            ▪ rhpname               : (str)
            ▪ text0                 : (str) the initial source text
            ▪ text                  : (LCharAndTextPos) main attribute : Rhp text

            no RETURNED VALUE
        """
        Rhp.__init__(self,
                     language=language,
                     rhpname=rhpname,
                     text0=text0)
        self.text = text

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
            RhpXXXnormalization.__str__()
            ____________________________________________________________________

            Return a human-readable representation of self.
            ____________________________________________________________________

            RETURNED VALUE : a human-readable string
        """
        return "{0} {1} - {2} :\n  text='{3}' <{4:.3f}>".format(RHP_SYMB,
                                                                self.rhpname,
                                                                hashvalue2hex(self.get_hashvalue()),
                                                                self.text,
                                                                self.get_interest())

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            RhpXXXnormalization.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(language=self.language,
                          rhpname=self.rhpname,
                          text0=self.text0,
                          text=self.text)

    #///////////////////////////////////////////////////////////////////////////
    def get_interest(self):
        """
            RhpXXXnormalization.get_interest()
            ___________________________________________________________________

            Compute the value of ._interest and return it.
            ___________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : (float) self._interest
        """
        self._interest = RhpXXXnormalization.default_interest
        return self._interest

    #///////////////////////////////////////////////////////////////////////////
    def report(self, margin=""):
        """
            RhpXXXnormalization.report()
            ____________________________________________________________________

            Return a string describing self in a more friendly way than
            __str__() does, including colored segments of text.
            ____________________________________________________________________

            no ARGUMENT.

            RETURNED VALUE : the expected (str)string.
        """
        colors = dict()
        index = 0 # to be used to alternate the colors
        for charandtextpos in self.text:
            for x0x1 in charandtextpos.textpos:
                if index == 0:
                    colors[(tuple(x0x1),)] = "[color1]"
                else:
                    colors[(tuple(x0x1),)] = "[color2]"
                index ^= 1

        colorstr = ColorStr(srcstring=improve_reportstr_readibilty(self.text0),
                            colors=colors)

        reportstr = "{0} ({1}) : \"{2}\" <{3:.3f}>".format(RHP_SYMB,
                                                           self.rhpname,
                                                           colorstr,
                                                           self.get_interest())
        return add_prefix_before_line(margin, reportstr)

    #///////////////////////////////////////////////////////////////////////////
    def set_hashvalue(self):
        """
            RhpXXXnormalization.set_hashvalue()
            ____________________________________________________________________

            Initialize the value of _hashvalue.
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        hasher = HASHER()
        hasher.update(self.language.encode())
        hasher.update(self.rhpname.encode())
        hasher.update(self.text0.encode())
        hasher.update(self.text.get_hashvalue())
        for charandtextpos in self.text:
            hasher.update(charandtextpos.characters.encode())
            hasher.update(charandtextpos.textpos.get_hashvalue())
        self._hashvalue = hasher.digest()

################################################################################
class RhpFRA2(RhpXXXnormalization):
    """
        RhpFRA2 class
        ________________________________________________________________________

        (French) Use RhpFRA2 to store a normalized text in a
        LCharAndTextPos object.

        ✓ unittests : see the RhpFRA2Test class.

        about Rhp classes for French:
        ˮ ▪ (RhpFRA : mother class of all RhpFRA*** classes)
        ˮ ▪ RhpFRA1 : to be read by ProcessFRA1 (text in .text, a LCharAndTextPos object)
        ˮ ▪ RhpFRA2 : to be read by ProcessFRA2 (text in .text, a LCharAndTextPos object)
        ˮ ▪ RhpFRA3 : to be read by ProcessFRA3 (text in .text, a LPyxis object)
        ˮ ▪ RhpFRA4 : to be read by ProcessFRA4 (text in .text, a LPyxis object,
        ˮ                                        + in .ending_punctuation)
        ˮ
        ________________________________________________________________________

        class attribute :
        ○ default_interest      : (float) default value for ._interest

        instance attributes :
        ○ _hashvalue            : (bytes or None)
                                  Use .get_hashvalue() to read its value.
        ○ _interest             : (float) numerical interest of self
                                  Use .get_interest() to read its value.
        ○ language              : (str) ISO 639-3 name of the language of self.
        ○ rhpname               : (str)
        ○ text                  : (LCharAndTextPos) main attribute : Rhp text
        ○ text0                 : (str) the initial source text
                                  Modified __init__().

        methods :
        ○ __eq__(self, other)
        ◐ __init__(self, language="fra", rhpname="RhpFRA2", text0, text)
        ○ __str__(self)
        ○ clone(self)
        ○ get_hashvalue(self)
        ○ get_interest(self)
        ○ report(self)
        ○ set_hashvalue(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 text0,
                 text,
                 language="fra",
                 rhpname="RhpFRA2"):
        """
            RhpFRA2.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ text0                 : (str) the initial source text
            ▪ text                  : (LCharAndTextPos) main attribute : Rhp text
            ▪ language              : (str) ISO 639-3
            ▪ rhpname               : (str)

            no RETURNED VALUE
        """
        RhpXXXnormalization.__init__(self,
                                     language=language,
                                     rhpname=rhpname,
                                     text0=text0,
                                     text=text)

################################################################################
class RhpXXXmorpho(Rhp):
    """
        RhpXXXmorpho class
        ________________________________________________________________________

        Use RhpXXXmorpho to store Pyxis objects with morphological analysis.

        ✓ unittests : see the RhpXXXmorphoTest class.

        about Rhp classes:
        ˮ Use an Rhp (Reading Hypothesis) class to store an analyse of a
        ˮ textual segment.
        ˮ
        ˮ Method expected : .set_hashvalue(), .clone(), .report() ....
        ˮ
        ˮ ▪ (Rhp : mother class of all Rhp*** classes)
        ˮ
        ˮ ▪ Rhp0 : raw text, to be read by ProcessFRA0 (raw text in .text0)
        ˮ ▪ RhpXXXblurwords : store words roughly cut
        ˮ ▪ RhpXXXnormalization : store a normalized text in a LCharAndTextPos object
        ˮ ▪ RhpXXXmorpho : store Pyxis objects with morphological analysis
        ˮ ▪ RhpXXXsentences : store Pyxis objects grouped together into sentences
        ˮ
        ˮ Ancient Greek :
        ˮ ▪ (RhpGRC : mother class of all RhpGRC*** classes)
        ˮ
        ˮ French :
        ˮ ▪ (RhpFRA : mother class of all RhpFRA*** classes)
        ________________________________________________________________________

        class attribute :
        ◐ default_interest      : (float) default value for ._interest

        instance attributes :
        ○ _hashvalue            : (bytes or None)
                                  Use .get_hashvalue() to read its value.
        ○ _interest             : (float) numerical interest of self
                                  Use .get_interest() to read its value.
        ○ language              : (str) ISO 639-3 name of the language of self.
        ○ rhpname               : (str)
        ● text                  : (LPyxis) main attribute : Rhp text
        ○ text0                 : (str) the initial source text

        methods :
        ○ __eq__(self, other)
        ◐ __init__(self, language, rhpname, text0, text=None)
        ● __str__(self)
        ● clone(self)
        ○ get_hashvalue(self)
        ◐ get_interest(self)
        ● report(self)
        ● set_hashvalue(self)
        ○ uniquename(self)
    """
    default_interest = 5.0

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 rhpname,
                 text0,
                 text=None):
        """
            RhpXXXmorpho.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ language              : (str) ISO 639-3 name of the language of self.
            ▪ rhpname               : (str)
            ▪ text                  : (None=LPyxis() or LPyxis) main attribute :
                                      Rhp text
            ▪ text0                 : (str) the initial source text
        """
        if text is None:
            text = LPyxis()

        Rhp.__init__(self,
                     language=language,
                     rhpname=rhpname,
                     text0=text0)
        self.text = text

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
            RhpXXXmorpho.__str__()
            ____________________________________________________________________

            Return a human-readable representation of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a human-readable string
        """
        res = []
        res.append("{0} {1} - {2} <{3:.3f}>:".format(RHP_SYMB,
                                                     self.rhpname,
                                                     hashvalue2hex(self.get_hashvalue()),
                                                     self.get_interest()))
        res.append(add_prefix_before_line("     ", str(self.text)))
        return "\n".join(res)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            RhpXXXmorpho.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        res = type(self)(language=self.language,
                         rhpname=self.rhpname,
                         text=self.text,
                         text0=self.text0)
        res.text = self.text.clone()
        return res

    #///////////////////////////////////////////////////////////////////////////
    def get_interest(self):
        """
            RhpXXXmorpho.get_interest()
            ___________________________________________________________________

            Compute the value of ._interest and return it.
            ___________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : (float) self._interest
        """
        self._interest = RhpXXXmorpho.default_interest

        for pyxis in self.text:
            if "Pyxis1" in pyxis.pyxisname:
                if not pyxis.recognized:
                    self._interest *= 0.9

        return self._interest

    #///////////////////////////////////////////////////////////////////////////
    def report(self, margin=""):
        """
            RhpXXXmorpho.report()
            ____________________________________________________________________

            Return a string describing self in a more friendly way than
            __str__() does, including colored segments of text.
            ____________________________________________________________________

            no ARGUMENT.

            RETURNED VALUE : the expected (str)string.
        """
        colors = dict()
        index = 0 # to be used to alternate the colors
        for pyxis in self.text:
            for x0x1 in pyxis.get_text0pos():
                if index == 0:
                    colors[(tuple(x0x1),)] = "[color1]"
                else:
                    colors[(tuple(x0x1),)] = "[color2]"
                index ^= 1

        colorstr = ColorStr(srcstring=improve_reportstr_readibilty(self.text0),
                            colors=colors)

        reportstr = "{0} ({1}) : \"{2}\" <{3:.3f}>".format(RHP_SYMB,
                                                           self.rhpname,
                                                           colorstr,
                                                           self.get_interest())

        return add_prefix_before_line(margin, reportstr)

    #///////////////////////////////////////////////////////////////////////////
    def set_hashvalue(self):
        """
            RhpXXXmorpho.set_hashvalue()
            ____________________________________________________________________

            Initialize the value of _hashvalue.
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        hasher = HASHER()
        hasher.update(self.language.encode())
        hasher.update(self.rhpname.encode())
        hasher.update(self.text0.encode())
        hasher.update(self.text.get_hashvalue())
        self._hashvalue = hasher.digest()

################################################################################
class RhpFRA3(RhpXXXmorpho):
    """
        RhpFRA3 class
        ________________________________________________________________________

        (French) Use RhpFRA3  to store Pyxis objects with morphological
        analysis.

        ✓ unittests : see the RhpFRA3Test class.

        about Rhp classes for French:
        ˮ ▪ (RhpFRA : mother class of all RhpFRA*** classes)
        ˮ ▪ RhpFRA1 : to be read by ProcessFRA1 (text in .text, a LCharAndTextPos object)
        ˮ ▪ RhpFRA2 : to be read by ProcessFRA2 (text in .text, a LCharAndTextPos object)
        ˮ ▪ RhpFRA3 : to be read by ProcessFRA3 (text in .text, a LPyxis object)
        ˮ ▪ RhpFRA4 : to be read by ProcessFRA4 (text in .text, a LPyxis object,
        ˮ                                        + in .ending_punctuation)
        ˮ
        ________________________________________________________________________

        class attribute :
        ○ default_interest      : (float) default value for ._interest

        instance attributes :
        ○ _hashvalue            : (bytes or None)
                                  Use .get_hashvalue() to read its value.
        ○ _interest             : (float) numerical interest of self
                                  Use .get_interest() to read its value.
        ○ language              : (str) ISO 639-3 name of the language of self.
        ○ rhpname               : (str)
        ● text                  : (LPyxis) main attribute : Rhp text
        ○ text0                 : (str) the initial source text

        methods :
        ○ __eq__(self, other)
        ◐ __init__(self, language="fra", rhpname="RhpFRA3", text=None, text0)
        ○ __str__(self)
        ○ clone(self)
        ○ get_hashvalue(self)
        ○ get_interest(self)
        ○ report(self)
        ○ set_hashvalue(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 text0,
                 text=None,
                 language="fra",
                 rhpname="RhpFRA3"):
        """
            RhpFRA3.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENT:
            ▪ text                  : (None=LPyxis() or LPyxis) main attribute :
                                      Rhp text
            ▪ text0                 : (str) the initial source text
            ▪ language              : (str) ISO 639-3
            ▪ rhpname               : (str)
        """
        if text is None:
            text = LPyxis()

        RhpXXXmorpho.__init__(self,
                              language=language,
                              rhpname=rhpname,
                              text=text,
                              text0=text0)

################################################################################
class RhpXXXsentences(Rhp):
    """
        RhpXXXsentences class
        ________________________________________________________________________

        Use RhpXXXsentences to store Pyxis objects grouped together into
        sentences, each sentence ending with special Pyxis object named
        .ending_punc.

        ✓ unittests : see the RhpXXXsentencesTest class.

        about Rhp classes:
        ˮ Use an Rhp (Reading Hypothesis) class to store an analyse of a
        ˮ textual segment.
        ˮ
        ˮ Method expected : .set_hashvalue(), .clone(), .report() ....
        ˮ
        ˮ ▪ (Rhp : mother class of all Rhp*** classes)
        ˮ
        ˮ ▪ Rhp0 : raw text, to be read by ProcessFRA0 (raw text in .text0)
        ˮ ▪ RhpXXXblurwords : store words roughly cut
        ˮ ▪ RhpXXXnormalization : store a normalized text in a LCharAndTextPos object
        ˮ ▪ RhpXXXmorpho : store Pyxis objects with morphological analysis
        ˮ ▪ RhpXXXsentences : store Pyxis objects grouped together into sentences
        ˮ
        ˮ Ancient Greek :
        ˮ ▪ (RhpGRC : mother class of all RhpGRC*** classes)
        ˮ
        ˮ French :
        ˮ ▪ (RhpFRA : mother class of all RhpFRA*** classes)
        ________________________________________________________________________

        class attribute :
        ◐ default_interest      : (float) default value for ._interest

        instance attributes :
        ○ _hashvalue            : (bytes or None)
                                  Use .get_hashvalue() to read its value.
        ○ _interest             : (float) numerical interest of self
                                  Use .get_interest() to read its value.
        ● ending_punc           : None or a Pyxis1 object
        ○ language              : (str) ISO 639-3 name of the
                                  language of self.
        ○ rhpname               : (str)
        ● text                  : (LPyxis) main attribute : Rhp text
        ○ text0                 : (str) the initial source text

        methods :
        ● __eq__(self, other)
        ◐ __init__(self, language, rhpname, text=None, text0, ending_punc)
        ● __str__(self)
        ● clone(self)
        ○ get_hashvalue(self)
        ◐ get_interest(self)
        ● report(self)
        ● set_hashvalue(self)
        ○ uniquename(self)
    """
    default_interest = 10.0

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 rhpname,
                 text0,
                 ending_punc,
                 text=None):
        """
            RhpXXXsentences.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ language              : (str)language name (ISO 639-3) or None if
                                      irrelevant
            ▪ rhpname               : (str)
            ▪ text                  : (LPyxis) main attribute : Rhp text
            ▪ text0                 : (str) the initial source text
            ▪ ending_punc    : None or a Pyxis1 object
        """
        if text is None:
            text = LPyxis()
        Rhp.__init__(self,
                     language,
                     rhpname,
                     text0)

        self.text = text
        self.ending_punc = ending_punc

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
            RhpXXXsentences.__str__()
            ____________________________________________________________________

            Return a human-readable representation of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a human-readable string
        """
        res = []
        res.append("{0} {1} - {2} <{3:.3f}>:".format(RHP_SYMB,
                                                     self.rhpname,
                                                     hashvalue2hex(self.get_hashvalue()),
                                                     self.get_interest()))
        res.append("  ➤ ending punctuation : '{0}'".format(self.ending_punc))
        res.append("  ➤ Pyxis :")
        res.append(add_prefix_before_line("    ", str(self.text)))
        return "\n".join(res)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            RhpXXXsentences.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        res = type(self)(language=self.language,
                         rhpname=self.rhpname,
                         text0=self.text0,
                         text=self.text,
                         ending_punc=self.ending_punc)
        res.text = self.text.clone()
        return res

    #///////////////////////////////////////////////////////////////////////////
    def get_interest(self):
        """
            RhpXXXsentences.get_interest()
            ___________________________________________________________________

            Compute the value of ._interest and return it.
            ___________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : (float) self._interest
        """
        self._interest = RhpXXXsentences.default_interest

        for pyxis in self.text:
            if "Pyxis1" in pyxis.pyxisname:
                if not pyxis.recognized:
                    self._interest *= 0.9

        return self._interest

    #///////////////////////////////////////////////////////////////////////////
    def report(self, margin=""):
        """
            RhpXXXsentences.report()
            ____________________________________________________________________

            Return a string describing self in a more friendly way than
            __str__() does, including colored segments of text.
            ____________________________________________________________________

            no ARGUMENT.

            RETURNED VALUE : the expected (str)string.
        """
        res = []

        colors = dict()
        index = 0 # to be used to alternate the colors
        for pyxis in self.text:
            for x0x1 in pyxis.get_text0pos():
                if index == 0:
                    colors[(tuple(x0x1),)] = "[color1]"
                else:
                    colors[(tuple(x0x1),)] = "[color2]"
                index ^= 1

        # ... let's not forget the punctuation symbol :
        if self.ending_punc is not None:
            for x0x1 in self.ending_punc.get_text0pos():
                if index == 0:
                    colors[(tuple(x0x1),)] = "[color1]"
                else:
                    colors[(tuple(x0x1),)] = "[color2]"
                index ^= 1

        colorstr = ColorStr(srcstring=improve_reportstr_readibilty(self.text0),
                            colors=colors)
        res.append("{0} ({1}) : \"{2}\" <{3:.3f}>".format(RHP_SYMB,
                                                          self.rhpname,
                                                          colorstr,
                                                          self.get_interest()))

        for pyxis in self.text:
            res.append(add_prefix_before_line("  ", pyxis.report()))

        if self.ending_punc is None:
            res.append("  [[no ending punctuation]]")
        else:
            res.append(add_prefix_before_line("  ", "[[ending punctuation :]]"))
            res.append(add_prefix_before_line("  ", self.ending_punc.report()))

        return add_prefix_before_line(margin, "\n".join(res))

    #///////////////////////////////////////////////////////////////////////////
    def set_hashvalue(self):
        """
            RhpXXXsentences.set_hashvalue()
            ____________________________________________________________________

            Initialize the value of _hashvalue.
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        hasher = HASHER()
        hasher.update(self.language.encode())
        hasher.update(self.rhpname.encode())
        hasher.update(self.text0.encode())
        hasher.update(self.text.get_hashvalue())

        if self.ending_punc is None:
            hasher.update("None".encode())
        else:
            hasher.update(self.ending_punc.get_hashvalue())

        self._hashvalue = hasher.digest()

################################################################################
class RhpFRA4(RhpXXXsentences):
    """
        RhpFRA4 class
        ________________________________________________________________________

        (French)
        Use RhpXXXsentences to store Pyxis objects grouped together into
        sentences, each sentence ending with special Pyxis object named
        .ending_punc.

        ✓ unittests : see the RhpFRA4Test class.

        about Rhp classes for French:
        ˮ ▪ (RhpFRA : mother class of all RhpFRA*** classes)
        ˮ ▪ RhpFRA1 : to be read by ProcessFRA1 (text in .text, a LCharAndTextPos object)
        ˮ ▪ RhpFRA2 : to be read by ProcessFRA2 (text in .text, a LCharAndTextPos object)
        ˮ ▪ RhpFRA3 : to be read by ProcessFRA3 (text in .text, a LPyxis object)
        ˮ ▪ RhpFRA4 : to be read by ProcessFRA4 (text in .text, a LPyxis object,
        ˮ                                        + in .ending_punctuation)
        ˮ
        ________________________________________________________________________

        class attribute :
        ○ default_interest      : (float) default value for ._interest

        instance attributes :
        ○ _hashvalue            : (bytes or None)
                                  Use .get_hashvalue() to read its value.
        ○ _interest             : (float) numerical interest of self
                                  Use .get_interest() to read its value.
        ○ ending_punc           : None or a Pyxis1 object
        ○ language              : (str) ISO 639-3 name of the language of self.
        ○ rhpname               : (str)
        ○ text                  : (LPyxis) main attribute : Rhp text
        ○ text0                 : (str) the initial source text

        methods :
        ○ __eq__(self, other)
        ◐ __init__(self,
                   text=None, text0, ending_punc,
                   language="fra", rhpname="RhpFRA4")
        ○ __str__(self)
        ○ clone(self)
        ○ get_hashvalue(self)
        ○ get_interest(self)
        ○ report(self)
        ○ set_hashvalue(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////SZ
    def __init__(self,
                 text0,
                 ending_punc=None,
                 language="fra",
                 rhpname="RhpFRA4",
                 text=None):
        """
            RhpFRA4.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ text                  : (LPyxis) main attribute : Rhp text
            ▪ text0                 : (str) the initial source text
            ▪ ending_punc    : None or a Pyxis1 object
            ▪ language              : (str) ISO 639-3
            ▪ rhpname               : (str)
        """
        if text is None:
            text = LPyxis()

        RhpXXXsentences.__init__(self,
                                 language=language,
                                 rhpname=rhpname,
                                 text0=text0,
                                 text=text,
                                 ending_punc=ending_punc)

################################################################################
class RhpXXXinsidesentence(Rhp):
    """
        RhpXXXinsidesentence class
        ________________________________________________________________________

        Use RhpXXXinsidesentence to store Pyxis2 objects. The text is stored in
        self.text, a DictHashvalueToPyxis object.

        ✓ unittests : see the RhpXXXinsidesentenceTest class.

        about Rhp classes:
        ˮ Use an Rhp (Reading Hypothesis) class to store an analyse of a
        ˮ textual segment.
        ˮ
        ˮ Method expected : .set_hashvalue(), .clone(), .report() ....
        ˮ
        ˮ ▪ (Rhp : mother class of all Rhp*** classes)
        ˮ
        ˮ ▪ Rhp0 : raw text, to be read by ProcessFRA0 (raw text in .text0)
        ˮ ▪ RhpXXXblurwords : store words roughly cut
        ˮ ▪ RhpXXXnormalization : store a normalized text in a LCharAndTextPos object
        ˮ ▪ RhpXXXmorpho : store Pyxis objects with morphological analysis
        ˮ ▪ RhpXXXsentences : store Pyxis objects grouped together into sentences
        ˮ
        ˮ Ancient Greek :
        ˮ ▪ (RhpGRC : mother class of all RhpGRC*** classes)
        ˮ
        ˮ French :
        ˮ ▪ (RhpFRA : mother class of all RhpFRA*** classes)
        ________________________________________________________________________

        class attribute :
        ◐ default_interest      : (float) default value for ._interest

        instance attributes :
        ○ _hashvalue            : (bytes or None)
                                  Use .get_hashvalue() to read its value.
        ○ _interest             : (float) numerical interest of self
                                  Use .get_interest() to read its value.
        ○ ending_punc           : None or a Pyxis1 object
        ○ language              : (str) ISO 639-3 name of the language of self.
        ○ rhpname               : (str)
        ○ text                  : (DictHashvalueToPyxis) main attribute : Rhp
                                  text
        ○ text0                 : (str) the initial source text

        methods :
        ○ __eq__(self, other)
        ◐ __init__(self,
                   language, rhpname,
                   text=None, text0, ending_punc=None)
        ● __str__(self)
        ● clone(self)
        ○ get_hashvalue(self)
        ◐ get_interest(self)
        ● report(self)
        ● report__pyxis(self)
        ● report__mainline_colors(self)
        ● set_hashvalue(self)
        ● set_text0reportstr(self)
        ○ uniquename(self)
    """
    default_interest = 100.0

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 language,
                 rhpname,
                 text0,
                 text=None,
                 ending_punc=None):
        """
            RhpXXXinsidesentence.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENT:
            ▪ language              : (str) ISO 639-3
            ▪ rhpname               : (str)
            ▪ text                  : (DictHashvalueToPyxis) main attribute :
                                      Rhp text
            ▪ text0                 : (str) the initial source text
            ▪ ending_punc    : None or a Pyxis1 object
        """
        if text is None:
            text = DictHashvalueToPyxis()

        Rhp.__init__(self,
                     language=language,
                     rhpname=rhpname,
                     text0=text0)

        self.text = text
        self.ending_punc = ending_punc

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
            RhpXXXinsidesentence.__str__()
            ____________________________________________________________________

            Return a human-readable representation of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a human-readable string
        """
        res = []
        res.append("{0} {1} - {2} <{3:.3f}>:".format(RHP_SYMB,
                                                     self.rhpname,
                                                     hashvalue2hex(self.get_hashvalue()),
                                                     self.get_interest()))
        res.append("  ➤ ending punctuation : '{0}'".format(self.ending_punc))
        res.append("  ➤ Pyxis :")
        res.append(add_prefix_before_line("    ", str(self.text)))
        return "\n".join(res)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            RhpXXXinsidesentence.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        res = type(self)(language=self.language,
                         rhpname=self.rhpname,
                         text0=self.text0,
                         text=self.text,
                         ending_punc=self.ending_punc)
        res.text = self.text.clone()
        return res

    #///////////////////////////////////////////////////////////////////////////
    def get_interest(self):
        """
            RhpXXXinsidesentence.get_interest()
            ___________________________________________________________________

            Compute the value of ._interest and return it.
            ___________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : (float) self._interest
        """
        self._interest = RhpXXXinsidesentence.default_interest

        for pyxis_hashvalue in self.text:
            pyxis = self.text[pyxis_hashvalue]

            if pyxis.is_unknown():
                self._interest *= 0.9
            else:
                self._interest *= 1+(0.1*(len(pyxis.subpyxis)-1))

        return self._interest

    #///////////////////////////////////////////////////////////////////////////
    def report(self, margin=""):
        """
            RhpXXXinsidesentence.report()
            ____________________________________________________________________

            Return a string describing self in a more friendly way than
            __str__() does, including colored segments of text.
            ____________________________________________________________________

            no ARGUMENT.

            RETURNED VALUE : the expected (str)string.
        """
        res = []

        # (1/3) Main line :
        colors = self.report__mainline_colors()
        colorstr = ColorStr(srcstring=improve_reportstr_readibilty(self.text0),
                            colors=colors)
        res.append("{0} ({1}) : \"{2}\" <{3:.3f}>".format(RHP_SYMB,
                                                          self.rhpname,
                                                          colorstr,
                                                          self.get_interest()))

        # (2/3) Pyxis*** objects :
        res1 = self.report__pyxis()

        # (3/3) ending punctuation :
        res2 = []
        if self.ending_punc is None:
            res2.append("  (no ending punctuation)")
        else:
            res2.append(add_prefix_before_line("  ", "[[ending punctuation :]]"))
            res2.append(add_prefix_before_line("  ", self.ending_punc.report()))

        return add_prefix_before_line(margin, "\n".join(res+res1+res2))

    #///////////////////////////////////////////////////////////////////////////
    def report__pyxis(self):
        """
            RhpXXXinsidesentence.report__pyxis()
            ____________________________________________________________________

            This method is a sub-function of .report() .

            (lines about Pyxis objects in the report)

            Return a list of (str) strings describing the Pyxis objects.
            ____________________________________________________________________

            no ARGUMENT.

            RETURNED VALUE : [], []
        """
        res = []       # for Pyxis1 objects

        for pyxis_hashvalue in self.text:
            pyxis = self.text[pyxis_hashvalue]
            res.append(add_prefix_before_line("  ", pyxis.report()))
        return res

    #///////////////////////////////////////////////////////////////////////////
    def report__mainline_colors(self):
        """
            RhpXXXinsidesentence.report__mainline_colors()
            ____________________________________________________________________

            This method is a sub-function of .report() .

            (main line of the report)

            Return a dict to be used by ColorStr.
            ____________________________________________________________________

            no ARGUMENT.

            RETURNED VALUE : a dict to be used by ColorStr.
        """
        colors = dict()
        index = 0 # to be used to alternate the colors

        for hashvalue in self.text:
            pyxis = self.text[hashvalue]
            for x0x1 in pyxis.get_text0pos():
                if index == 0:
                    colors[(tuple(x0x1),)] = "[color3]"
                else:
                    colors[(tuple(x0x1),)] = "[color4]"
                index ^= 1

        # ... let's not forget the punctuation symbol :
        if self.ending_punc is not None:
            for x0x1 in self.ending_punc.get_text0pos():
                if index == 0:
                    colors[(tuple(x0x1),)] = "[color3]"
                else:
                    colors[(tuple(x0x1),)] = "[color4]"
                index ^= 1

        return colors

    #///////////////////////////////////////////////////////////////////////////
    def set_hashvalue(self):
        """
            RhpXXXinsidesentence.set_hashvalue()
            ____________________________________________________________________

            Initialize the value of _hashvalue.
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        hasher = HASHER()
        hasher.update(self.language.encode())
        hasher.update(self.rhpname.encode())
        hasher.update(self.text0.encode())
        hasher.update(self.text.get_hashvalue())

        if self.ending_punc is None:
            hasher.update("None".encode())
        else:
            hasher.update(self.ending_punc.get_hashvalue())

        self._hashvalue = hasher.digest()

    #///////////////////////////////////////////////////////////////////////////
    def set_text0reportstr(self):
        """
            RhpXXXinsidesentence.set_text0reportstr()
            ____________________________________________________________________

            Initialize the Pyxis2._text0reportstr instance attribute of
            every Pyxis2 object in self.text .
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        for pyxis in self.text.values():
            text0extract = []
            for x0x1 in pyxis.get_text0pos():
                text0extract.append(self.text0[x0x1[0]:x0x1[1]])
            # Yes, this method needs an access to ._text0reportstr :
            # pylint: disable=protected-access
            pyxis._text0reportstr = "/" + "/".join(text0extract) + "/"

################################################################################
class RhpFRA5(RhpXXXinsidesentence):
    """
        RhpFRA5 class
        ________________________________________________________________________

        ✓ unittests : see the RhpFRA5Test class.
        ________________________________________________________________________

        class attribute :
        ○ default_interest      : (float) default value for ._interest

        instance attributes :
        ○ _hashvalue            : (bytes or None)
                                  Use .get_hashvalue() to read its value.
        ○ _interest             : (float) numerical interest of self
                                  Use .get_interest() to read its value.
        ○ ending_punc           : None or a Pyxis1 object
        ○ rhpname               : (str)
        ○ text                  : (DictHashvalueToPyxis) main attribute : Rhp
                                  text
        ○ text0                 : (str) the initial source text

        methods :
        ○ __eq__(self)
        ◐ __init__(self,
                   language="fra", rhpname="RhpFRA5",
                   text=None, text0, ending_punc=None)
        ○ __str__(self)
        ○ clone(self)
        ○ get_hashvalue(self)
        ○ get_interest(self)
        ○ report(self)
        ○ report__pyxis()
        ○ report__mainline_colors()
        ○ set_hashvalue(self)
        ○ set_text0reportstr(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 text0,
                 text=None,
                 ending_punc=None,
                 language="fra",
                 rhpname="RhpFRA5"):
        """
            RhpFRA5.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ language              : (str) ISO 639-3
            ▪ rhpname               : (str)
            ▪ text                  : (DictHashvalueToPyxis) main attribute :
                                      Rhp text
            ▪ text0                 : (str) the initial source text
            ▪ ending_punc    : None or a Pyxis1 object
        """
        if text is None:
            text = DictHashvalueToPyxis()

        RhpXXXinsidesentence.__init__(self,
                                      language=language,
                                      rhpname=rhpname,
                                      text=text,
                                      text0=text0,
                                      ending_punc=ending_punc)

################################################################################
class Pyxis1GRCword(Pyxis1XXXword):
    """
        Pyxis1GRCword class
        ________________________________________________________________________

        (Ancient Greek) Pyxis1 for a word.

        ✓ unittests : see the Pyxis1GRCwordTest class

        about Pyxis classes for Ancient Greek:
        ˮ ▪ Pyxis1GRCword       : (Ancient Greek) (roughly cut) "word" Pyxis1
        ˮ ▪ Pyxis1GRCpunctuation: (Ancient Greek) "punctuation" Pyxis1
        ˮ ▪ Pyxis1GRCunknown    : (Ancient Greek) "unknown" Pyxis1
        ˮ
        ˮ ▪ Pyxis2GRCng   : (Ancient Greek) Pyxis2 for a nominal group.
        ˮ ▪ Pyxis2GRCvs   : (Ancient Greek) Pyxis2 for a verbal syntagm
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ○ _hashvalue            : (None/bytes) the hash value of self computed
                                  by self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _interest             : (float) numerical interest of self
                                  Use .get_interest() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ○ details               : (DI object)
        ○ language              : (str) ISO 639-3 name of the language of self,
                                  "" if irrelevant.
        ○ punctuation_symb      : bool or None if self.recognized is
                                  set to False
        ○ pyxisname             : (str) string describing the type of self; may
                                  be equal to the classe name.
        ○ recognized            : bool
        ○ text                  : (str)source string

        methods :
        ○ __eq__(self, other)
        ◐ __init__(self,
                   text, _text0pos, details)
        ○ __str__(self)
        ○ __repr__(self)
        ◐ clone(self)
        ○ report(self)
        ○ get_hashvalue(self)
        ○ get_text0pos(self)
        ○ set_hashvalue(self)
        ○ set_text0pos(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 text,
                 _text0pos,
                 details):
        """
            Pyxis1GRCword.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ text                  : (str)source string
            ▪ _text0pos               : TextPos
            ▪ details               : dict(str:str) or a DI object

            no RETURNED VALUE
        """
        Pyxis1XXXword.__init__(self,
                               text=text,
                               _text0pos=_text0pos,
                               details=details,
                               language="grc",
                               pyxisname="Pyxis1GRCword")

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis1GRCword.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(text=self.text,
                          _text0pos=self.get_text0pos(),
                          details=self.details)

################################################################################
class Pyxis1GRCpunctuation(Pyxis1XXXpunctuation):
    """
        Pyxis1GRCpunctuation class
        ________________________________________________________________________

        (Ancient Greek) Pyxis1 for a punctuation symbol.

        ✓ unittests : see the Pyxis1GRCpunctuationTest class.

        about Pyxis classes for Ancient Greek:
        ˮ ▪ Pyxis1GRCword       : (Ancient Greek) (roughly cut) "word" Pyxis1
        ˮ ▪ Pyxis1GRCpunctuation: (Ancient Greek) "punctuation" Pyxis1
        ˮ ▪ Pyxis1GRCunknown    : (Ancient Greek) "unknown" Pyxis1
        ˮ
        ˮ ▪ Pyxis2GRCng   : (Ancient Greek) Pyxis2 for a nominal group.
        ˮ ▪ Pyxis2GRCvs   : (Ancient Greek) Pyxis2 for a verbal syntagm
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ○ _hashvalue            : (None/bytes) the hash value of self computed
                                  by self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _interest             : (float) numerical interest of self
                                  Use .get_interest() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ○ details               : (DI object)
        ○ language              : (str) ISO 639-3 name of the
                                  language of self, "" if irrelevant.
        ○ punctuation_symb      : bool or None if self.recognized is set to
                                  False
        ○ pyxisname             : (str) string describing the type of self; may
                                  be equal to the classe name.
        ○ recognized            : bool
        ○ text                  : (str) source string

        methods :
        ○ __eq__(self, other)
        ◐ __init__(self, text, _text0pos, details)
        ○ __str__(self)
        ○ __repr__(self)
        ◐ clone(self)
        ○ report(self)
        ○ get_hashvalue(self)
        ○ get_text0pos(self)
        ○ set_hashvalue(self)
        ○ set_text0pos(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 text,
                 _text0pos,
                 details):
        """
            Pyxis1GRCpunctuation.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ text                  : (str)source string
            ▪ _text0pos               : (TextPos)
            ▪ details               : dict(str:str) or a DI object

            no RETURNED VALUE
        """
        Pyxis1XXXpunctuation.__init__(self,
                                      language="grc",
                                      pyxisname="Pyxis1GRCpunctuation",
                                      text=text,
                                      _text0pos=_text0pos,
                                      details=details)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis1XXXpunctuation.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(text=self.text,
                          _text0pos=self.get_text0pos(),
                          details=self.details)

################################################################################
class Pyxis1GRCunknown(Pyxis1XXXunknown):
    """
        Pyxis1GRCunknown class
        ________________________________________________________________________

        (Ancient Greek) Pyxis1 for a list of unrecognized characters.

        ✓ unittests : see the Pyxis1GRCunknownTest class.

        about Pyxis classes for Ancient Greek:
        ˮ ▪ Pyxis1GRCword       : (Ancient Greek) (roughly cut) "word" Pyxis1
        ˮ ▪ Pyxis1GRCpunctuation: (Ancient Greek) "punctuation" Pyxis1
        ˮ ▪ Pyxis1GRCunknown    : (Ancient Greek) "unknown" Pyxis1
        ˮ
        ˮ ▪ Pyxis2GRCng   : (Ancient Greek) Pyxis2 for a nominal group.
        ˮ ▪ Pyxis2GRCvs   : (Ancient Greek) Pyxis2 for a verbal syntagm
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ○ _hashvalue            : (None/bytes) the hash value of self computed
                                  by self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _interest             : (float) numerical interest of self
                                  Use .get_interest() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ○ details               : (DI object)
        ○ language              : (str) ISO 639-3 name of the language of self,
                                  "" if irrelevant.
        ○ punctuation_symb      : bool or None if self.recognized is set to
                                  False
        ○ pyxisname             : (str) string describing the type of self; may
                                  be equal to the classe name.
        ○ recognized            : bool
        ○ text                  : (str)source string

        methods :
        ○ __eq__(self, other)
        ◐ __init__(self,
                   text, _text0pos, details=DI())
        ○ __str__(self)
        ○ __repr__(self)
        ◐ clone(self)
        ○ report(self)
        ○ get_hashvalue(self)
        ○ get_text0pos(self)
        ○ set_hashvalue(self)
        ○ set_text0pos(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 text,
                 _text0pos,
                 details=None):
        """
            Pyxis1GRCunknown.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ text                   : (str)source string
            ▪ _text0pos                : (TextPos)
            ▪ details                : None(=DI()) or dict(str:str) or a DI object

            no RETURNED VALUE
        """
        if details is None:
            details = DI()

        Pyxis1XXXunknown.__init__(self,
                                  text=text,
                                  _text0pos=_text0pos,
                                  details=details,
                                  language="grc",
                                  pyxisname="Pyxis1GRCunknown")

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis1GRCunknown.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(text=self.text,
                          _text0pos=self.get_text0pos(),
                          details=self.details)
################################################################################
class Pyxis2GRCng(Pyxis2XXXng):
    """
        Pyxis2GRCng class
        ________________________________________________________________________

        (Ancient Greek) Pyxis2 for a nominal group.

        ✓ unittests : see the Pyxis2GRCngTest class.

        about Pyxis classes for Ancient Greek:
        ˮ ▪ Pyxis1GRCword       : (Ancient Greek) (roughly cut) "word" Pyxis1
        ˮ ▪ Pyxis1GRCpunctuation: (Ancient Greek) "punctuation" Pyxis1
        ˮ ▪ Pyxis1GRCunknown    : (Ancient Greek) "unknown" Pyxis1
        ˮ
        ˮ ▪ Pyxis2GRCng   : (Ancient Greek) Pyxis2 for a nominal group.
        ˮ ▪ Pyxis2GRCvs   : (Ancient Greek) Pyxis2 for a verbal syntagm
        ________________________________________________________________________

        no class attribute

        instance attributes:
        ○ _hashvalue            : (None/bytes) the hash value of self computed by
                                  self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _interest             : (float) numerical interest of self
                                  Use .get_interest() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ○ _text0reportstr       : (str) report str of the extract from text0
                                  to be initialized by Rhp***.set_text0reportstr()
                                  to be used by the Pyxis***.__str__() methods
        ○ details               : (DI object)
        ○ language              : (str) ISO 639-3
        ○ pyxisname             : (str)

        methods :
        ◐ __init__(self,
                   subpyxis=None,
                   details, _text0reportstr="")
        ○ __repr__(self)
        ○ __str__(self)
        ○ add_a_subpyxis(self, pyxis)
        ◐ clone(self)
        ○ get_hashvalue(self)
        ○ get_text0pos(self)
        ○ is_a_punctuation_symbol(self)
        ○ is_a_space(self)
        ○ is_a_word(self)
        ○ is_unknown(self)
        ○ set_hashvalue(self)
        ○ set_text0pos(self)
        ○ report(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 details,
                 subpyxis=None,
                 _text0reportstr=""):
        """
            Pyxis2GRCng.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ details               : dict(str:str) or a DI object
            ▪ _text0reportstr       : (str) corresponding extract from text0
                                      to be initialized by Rhp***.set_text0reportstr()
                                      to be used by the Pyxis***.__str__() methods

            no RETURNED VALUE
        """
        Pyxis2XXXng.__init__(self,
                             language="grc",
                             pyxisname="Pyxis2GRCng",
                             details=details,
                             subpyxis=subpyxis,
                             _text0reportstr=_text0reportstr)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis2XXXng.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(details=self.details,
                          _text0reportstr=self._text0reportstr,
                          subpyxis=self.subpyxis)

################################################################################
class Pyxis2GRCvs(Pyxis2XXXvs):
    """
        Pyxis2GRCvs class
        ________________________________________________________________________

        (Ancient Greek) Pyxis2 for a nominal group.

        ✓ unittests : see the Pyxis2GRCvsTest class.

        about Pyxis classes for Ancient Greek:
        ˮ ▪ Pyxis1GRCword       : (Ancient Greek) (roughly cut) "word" Pyxis1
        ˮ ▪ Pyxis1GRCpunctuation: (Ancient Greek) "punctuation" Pyxis1
        ˮ ▪ Pyxis1GRCunknown    : (Ancient Greek) "unknown" Pyxis1
        ˮ
        ˮ ▪ Pyxis2GRCng   : (Ancient Greek) Pyxis2 for a nominal group.
        ˮ ▪ Pyxis2GRCvs   : (Ancient Greek) Pyxis2 for a verbal syntagm
        ________________________________________________________________________

        no class attribute

        instance attributes:
        ○ _hashvalue            : (None/bytes) the hash value of self computed by
                                  self.set_hashvalue()
                                  Use .get_hashvalue() to read its value.
        ○ _interest             : (float) numerical interest of self
                                  Use .get_interest() to read its value.
        ○ _text0pos             : (Textpos or None if uninitialized)
                                  positions of the text0 extracts stored in self.
                                  Use .get_text0pos() to read its value.
        ○ _text0reportstr       : (str) report str of the extract from text0
                                  to be initialized by Rhp***.set_text0reportstr()
                                  to be used by the Pyxis***.__str__() methods
        ○ details               : (DI object)
        ○ language              : (str) ISO 639-3
        ○ pyxisname             : (str)

        methods :
        ◐ __init__(self,
                   subpyxis=None,
                   details, _text0reportstr="")
        ○ __repr__(self)
        ○ __str__(self)
        ○ add_a_subpyxis(self, pyxis)
        ◐ clone(self)
        ○ get_hashvalue(self)
        ○ get_text0pos(self)
        ○ is_a_punctuation_symbol(self)
        ○ is_a_space(self)
        ○ is_a_word(self)
        ○ is_unknown(self)
        ○ set_hashvalue(self)
        ○ set_text0pos(self)
        ○ report(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 details,
                 subpyxis=None,
                 _text0reportstr=""):
        """
            Pyxis2GRCvs.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ details               : dict(str:str) or a DI object
            ▪ _text0reportstr       : (str) corresponding extract from text0
                                      to be initialized by Rhp***.set_text0reportstr()
                                      to be used by the Pyxis***.__str__() methods

            no RETURNED VALUE
        """
        Pyxis2XXXvs.__init__(self,
                             language="grc",
                             pyxisname="Pyxis2GRCvs",
                             details=details,
                             _text0reportstr=_text0reportstr)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
            Pyxis2GRCvs.clone()
            ____________________________________________________________________

            Return an independent copy of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : a copy of self.
        """
        return type(self)(details=self.details,
                          _text0reportstr=self._text0reportstr,
                          subpyxis=self.subpyxis)

################################################################################
class ProcessGRC0(ProcessXXXblurwords):
    """
        ProcessGRC0 class
        ________________________________________________________________________

        (Ancient Greek) use ProcessGRC0 to roughly cut a string into words and
        punctuation symbols.

        ▪ read a Rhp0 object, cuts it along the punctuation symbols, trying to find words.
        ▪ add a unique RhpGRC1 object.

        about ProcessXXXblurwords:
        ˮ language independant class : Process to cut a string into words,
        ˮ punctuation and unknown characters.
        ˮ This is a very rough way to cut a string into words. A word may
        ˮ not end with a punctuation symbol, e.g. if an enclitic is added
        ˮ at the end of the word:
        ˮ     (Latin)             dominusque (in fact, dominus + que)
        ˮ     (Ancient Greek)     οἰωνοῖσίτε πᾶσι (in fact, οἰωνοῖσί + τε)
        ˮ     (Sanskrit)          गच्छतीश्वरः  (in fact, गच्छति + ईश्वरः)
        ˮ

        about Process classes for Ancient Greek:
        ˮ ▪ ProcessGRC : mother class of all ProcessGRC*** classes : Ancient Greek
        ˮ ▪ ProcessGRC0 - reads Rhp0
        ˮ               -- cuts the text along the punctuation
        ˮ               --- creates RhpGRC1
        ˮ ▪ ProcessGRC1 - reads RhpGRC1
        ˮ               -- normalizes the text
        ˮ               --- creates RhpGRC2
        ˮ ▪ ProcessGRC2 - reads RhpGRC2
        ˮ               -- gets the morphological analysis
        ˮ               --- creates RhpGRC3
        ˮ ▪ ProcessGRC3 - reads RhpGRC3
        ˮ               -- groups together Pyxis into sentences
        ˮ               --- creates RhpGRC4
        ˮ ▪ ProcessGRC4 - reads RhpGRC4
        ˮ               -- Pyxis1GRCword > Pyxis2GRC***
        ˮ               --- creates RhpGRC5
        ____________________________________________________________________

        no class attribute

        instance attributes :
        ○ language              : (str) ISO 639-3, set to "grc" by
                                  the mother-class
        ○ output_rhpobject_name : the type added by the .read()
                                  method. Should be an Rhp*** object.
        ○ processname           : (str) name of the current
                                  process.
        ○ punctuation_symbols   : a list of str
        ○ spec                  : (different types, None if undefined)
                                  specifications describing the way the process
                                  does its job.
        ○ to_be_applied_to      : (type) objects read by this
                                  process.

        methods :
        ◐ __init__(self)
        ○ __str__(self)
        ○ read(self, target_rhp, text0)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
            ProcessGRC0.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        ProcessXXXblurwords.__init__(self,
                                     language="grc",
                                     processname="ProcessGRC0",
                                     to_be_applied_to=Rhp0,
                                     output_rhpobject_name=RhpGRC1,
                                     spec=(' ', '.', ';', "'", ","))

################################################################################
class ProcessGRC1(ProcessXXXnormalize):
    """
        ProcessGRC1 class
        ________________________________________________________________________

        (Ancient Greek) use ProcessGRC1 to normalize strings.

        ▪ Read a RhpGRC1 object and normalize its content.
        ▪ Add a unique RhpGRC2 object.

        about Process classes for Ancient Greek:
        ˮ ▪ ProcessGRC : mother class of all ProcessGRC*** classes : Ancient Greek
        ˮ ▪ ProcessGRC0 - reads Rhp0
        ˮ               -- cuts the text along the punctuation
        ˮ               --- creates RhpGRC1
        ˮ ▪ ProcessGRC1 - reads RhpGRC1
        ˮ               -- normalizes the text
        ˮ               --- creates RhpGRC2
        ˮ ▪ ProcessGRC2 - reads RhpGRC2
        ˮ               -- gets the morphological analysis
        ˮ               --- creates RhpGRC3
        ˮ ▪ ProcessGRC3 - reads RhpGRC3
        ˮ               -- groups together Pyxis into sentences
        ˮ               --- creates RhpGRC4
        ˮ ▪ ProcessGRC4 - reads RhpGRC4
        ˮ               -- Pyxis1GRCword > Pyxis2GRC***
        ˮ               --- creates RhpGRC5
        ____________________________________________________________________

        no class attribute

        instance attributes :
        ○ language              : (str) ISO 639-3 name of the
                                  language of self,
        ○ processname           : (str)
        ○ spec                  : (None, undefined)
        ○ to_be_applied_to      : (type) object read by the process.

        methods :
        ◐ __init__(self)
        ○ __str__(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
            ProcessGRC1.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        ProcessXXXnormalize.__init__(self,
                                     language="grc",
                                     processname="ProcessGRC1",
                                     to_be_applied_to=RhpGRC1,
                                     output_rhpobject_name=RhpGRC2)

################################################################################
class ProcessGRC2(ProcessXXXmorpho):
    """
        ProcessGRC2 class
        ________________________________________________________________________

        (Ancient Greek) use ProcessGRC2 to get the morphological analysis of
        strings.

        ▪ Read a RhpGRC2 object and add informations about its morphological
          analysis.
        ▪ Add one or more RhpGRC3 objects.

        about Process classes for Ancient Greek:
        ˮ ▪ ProcessGRC : mother class of all ProcessGRC*** classes : Ancient Greek
        ˮ ▪ ProcessGRC0 - reads Rhp0
        ˮ               -- cuts the text along the punctuation
        ˮ               --- creates RhpGRC1
        ˮ ▪ ProcessGRC1 - reads RhpGRC1
        ˮ               -- normalizes the text
        ˮ               --- creates RhpGRC2
        ˮ ▪ ProcessGRC2 - reads RhpGRC2
        ˮ               -- gets the morphological analysis
        ˮ               --- creates RhpGRC3
        ˮ ▪ ProcessGRC3 - reads RhpGRC3
        ˮ               -- groups together Pyxis into sentences
        ˮ               --- creates RhpGRC4
        ˮ ▪ ProcessGRC4 - reads RhpGRC4
        ˮ               -- Pyxis1GRCword > Pyxis2GRC***
        ˮ               --- creates RhpGRC5
        ____________________________________________________________________

        no class attribute

        instance attributes :
        ○ language              : (str) ISO 639-3, set to "grc"
                                  by the mother-class
        ○ output_rhpobject_name : the type added by the .read()
                                  method. Should be an Rhp*** object.
        ○ processname           : (str) name of the current
                                  process.
        ○ punctuation_symbols   : a list of str
        ○ spec                  : (ProcessXXXmorphoSPEC)
        ○ to_be_applied_to      : (type) object read by the process.

        methods :
        ○ __init__(self)
        ○ __str__(self)
        ○ read(self, target_rhp, text0)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
            ProcessGRC2.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        ProcessXXXmorpho.__init__(self,
                                  language="grc",
                                  processname="ProcessGRC2",
                                  to_be_applied_to=RhpGRC2,
                                  output_rhpobject_name=RhpGRC3,
                                  spec=ProcessXXXmorphoSPEC(pyxis1_word=Pyxis1GRCword,
                                                            pyxis1_punctuation=Pyxis1GRCpunctuation,
                                                            pyxis1_unknown=Pyxis1GRCunknown))

################################################################################
class ProcessGRC3(ProcessXXXsentences):
    """
        ProcessGRC3 class
        ________________________________________________________________________

        (Ancient Greek) use ProcessGRC3 to group together Pyxis objects into
        sentences.

        ▪ Read a RhpGRC3 object and cut it into sentences.
        ▪ Add one or more RhpGRC4 objects.

        about Process classes for Ancient Greek:
        ˮ ▪ ProcessGRC : mother class of all ProcessGRC*** classes : Ancient Greek
        ˮ ▪ ProcessGRC0 - reads Rhp0
        ˮ               -- cuts the text along the punctuation
        ˮ               --- creates RhpGRC1
        ˮ ▪ ProcessGRC1 - reads RhpGRC1
        ˮ               -- normalizes the text
        ˮ               --- creates RhpGRC2
        ˮ ▪ ProcessGRC2 - reads RhpGRC2
        ˮ               -- gets the morphological analysis
        ˮ               --- creates RhpGRC3
        ˮ ▪ ProcessGRC3 - reads RhpGRC3
        ˮ               -- groups together Pyxis into sentences
        ˮ               --- creates RhpGRC4
        ˮ ▪ ProcessGRC4 - reads RhpGRC4
        ˮ               -- Pyxis1GRCword > Pyxis2GRC***
        ˮ               --- creates RhpGRC5
        ___________________________________________________________________

        no class attribute

        instance attributes :
        ○ language              : (str) ISO 639-3, set to "grc"
                                  by the mother-class
        ○ output_rhpobject_name : the type added by the .read()
                                  method. Should be an Rhp*** object.
        ○ processname           : (str) name of the current
                                  process.
        ○ spec                  : (None, undefined)
        ○ to_be_applied_to      : (type) object read by the process.

        methods :
        ○ __init__(self)
        ○ __str__(self)
        ○ read(self, target_rhp, text0)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
            ProcessGRC3.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        ProcessXXXsentences.__init__(self,
                                     language="grc",
                                     processname="ProcessGRC3",
                                     to_be_applied_to=RhpGRC3,
                                     output_rhpobject_name=RhpGRC4)

################################################################################
class ProcessGRC4(ProcessXXXPyxis1ToPyxis2):
    """
        ProcessGRC4 class
        ________________________________________________________________________

        Read a RhpGRC4 object and convert the Pyxis1GRCword into Pyxis2*** objects
        Add one or more RhpGRC5 objects.

        about Process classes for Ancient Greek:
        ˮ ▪ ProcessGRC : mother class of all ProcessGRC*** classes : Ancient Greek
        ˮ ▪ ProcessGRC0 - reads Rhp0
        ˮ               -- cuts the text along the punctuation
        ˮ               --- creates RhpGRC1
        ˮ ▪ ProcessGRC1 - reads RhpGRC1
        ˮ               -- normalizes the text
        ˮ               --- creates RhpGRC2
        ˮ ▪ ProcessGRC2 - reads RhpGRC2
        ˮ               -- gets the morphological analysis
        ˮ               --- creates RhpGRC3
        ˮ ▪ ProcessGRC3 - reads RhpGRC3
        ˮ               -- groups together Pyxis into sentences
        ˮ               --- creates RhpGRC4
        ˮ ▪ ProcessGRC4 - reads RhpGRC4
        ˮ               -- Pyxis1GRCword > Pyxis2GRC***
        ˮ               --- creates RhpGRC5
        ____________________________________________________________________

        class attribute :
        ○ pyxis1topyxis2spec    : (dict) see the documentation below

        instance attributes :
        ○ language              : (str) ISO 639-3 name of the language of self,
        ○ processname           : (str)
        ○ spec                  : (different types, None if undefined)
                                  specifications describing the way the process
                                  does its job.
        ○ to_be_applied_to      : (type) name of the target Rhp object

        methods :
        ◐ __init__(self)
        ○ __str__(self)
        ● read(self, target_rhp, text0)
        ○ uniquename(self)
    """

    # about the dict given to Pyxis1TOPyxis2SPEC.__init__():
    # ˮ { (type)dest_type : ((str)src_pyxisname,
    # ˮ                      (str)value_in_details,
    # ˮ                      (list of str)keys_in_details) }
    # ˮ
    # ˮ by example :
    # ˮ             { Pyxis2GRCng : ("Pyxis1GRCword",
    # ˮ                              "grammatical nature",
    # ˮ                              ("common noun",))
    # ˮ             }
    # ˮ
    pyxis1topyxis2spec = Pyxis1TOPyxis2SPEC({
        Pyxis2GRCng : ("Pyxis1GRCword",
                       "grammatical nature",
                       ("common noun",)),

        Pyxis2GRCvs : ("Pyxis1GRCword",
                       "grammatical nature",
                       ("verb",)),

        Pyxis2GRCpunctuation    : ("Pyxis1GRCpunctuation", None, ()),
        Pyxis2GRCunknown        : ("Pyxis1GRCunknown", None, ()),
    })

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
            ProcessGRC4.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            no ARGUMENT, no RETURNED VALUE.
        """
        ProcessXXXPyxis1ToPyxis2.__init__(self,
                                          language="grc",
                                          processname="ProcessGRC4",
                                          to_be_applied_to=RhpGRC4,
                                          output_rhpobject_name=RhpGRC5,
                                          spec=ProcessGRC4.pyxis1topyxis2spec)

################################################################################
class RhpGRC1(RhpXXXblurwords):
    """
        RhpGRC1 class
        ________________________________________________________________________

        (Ancient Greek) Use RhpGRC1 to store words roughly cut from the
        input string.

        ✓ unittests : see the RhpGRC1Test class.

        about Rhp classes for Ancient Greek:
        ˮ ▪ (RhpGRC : mother class of all RhpGRC*** classes)
        ˮ ▪ RhpGRC1 : to be read by ProcessGRC1 (text in .text, a LCharAndTextPos object)
        ˮ ▪ RhpGRC2 : to be read by ProcessGRC2 (text in .text, a LCharAndTextPos object)
        ˮ ▪ RhpGRC3 : to be read by ProcessGRC3 (text in .text, a LPyxis object)
        ˮ ▪ RhpGRC4 : to be read by ProcessGRC4 (text in .text, a LPyxis object,
        ˮ                                        + in .ending_punctuation)
        ˮ
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ○ _hashvalue            : (bytes or None)
                                  Use .get_hashvalue() to read its value.
        ○ language              : (str) ISO 639-3 name of the language
                                  of self.
        ○ rhpname               : (str)
        ○ text                  : (LCharAndTextPos objet) main attribute :
                                  Rhp text
        ○ text0                 : (str) the initial source text

        methods :
        ○ __eq__(self, other)
        ◐ __init__(self, language="grc", rhpname="RhpGRC1", text0, text)
        ○ __str__(self)
        ○ clone(self)
        ○ get_hashvalue(self)
        ○ report(self)
        ○ set_hashvalue(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 text0,
                 text,
                 language="grc",
                 rhpname="RhpGRC1"):
        """
            RhpGRC1.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ text0                 : (str) the initial source text
            ▪ text                  : (LCharAndTextPos) main attribute : Rhp text
            ▪ language              : (str) ISO 639-3
            ▪ rhpname               : (str)

            no RETURNED VALUE
        """
        RhpXXXblurwords.__init__(self,
                                 language=language,
                                 rhpname=rhpname,
                                 text0=text0,
                                 text=text)

################################################################################
class RhpGRC2(RhpXXXnormalization):
    """
        RhpGRC2 class
        ________________________________________________________________________

        (Ancient Greek) Use RhpGRC2 to store a normalized text in a
        LCharAndTextPos object.

        ✓ unittests : see the RhpGRC2Test class.

        about Rhp classes for Ancient Greek:
        ˮ ▪ (RhpGRC : mother class of all RhpGRC*** classes)
        ˮ ▪ RhpGRC1 : to be read by ProcessGRC1 (text in .text, a LCharAndTextPos object)
        ˮ ▪ RhpGRC2 : to be read by ProcessGRC2 (text in .text, a LCharAndTextPos object)
        ˮ ▪ RhpGRC3 : to be read by ProcessGRC3 (text in .text, a LPyxis object)
        ˮ ▪ RhpGRC4 : to be read by ProcessGRC4 (text in .text, a LPyxis object,
        ˮ                                        + in .ending_punctuation)
        ˮ
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ○ _hashvalue            : (bytes or None)
                                  Use .get_hashvalue() to read its value.
        ○ language              : (str) ISO 639-3 name of the language of self.
        ○ rhpname               : (str)
        ○ text                  : (LCharAndTextPos) main attribute : Rhp text
        ○ text0                 : (str) the initial source text
                                  Modified __init__().

        methods :
        ○ __eq__(self, other)
        ◐ __init__(self, language="grc", rhpname="RhpGRC2", text0, text)
        ○ __str__(self)
        ○ clone(self)
        ○ get_hashvalue(self)
        ○ report(self)
        ○ set_hashvalue(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 text0,
                 text,
                 language="grc",
                 rhpname="RhpGRC2"):
        """
            RhpGRC2.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ text0                 : (str) the initial source text
            ▪ text                  : (LCharAndTextPos) main attribute : Rhp text
            ▪ language              : (str) ISO 639-3
            ▪ rhpname               : (str)

            no RETURNED VALUE
        """
        RhpXXXnormalization.__init__(self,
                                     language=language,
                                     rhpname=rhpname,
                                     text0=text0,
                                     text=text)

################################################################################
class RhpGRC3(RhpXXXmorpho):
    """
        RhpGRC3 class
        ________________________________________________________________________

        (Ancient Greek) Use RhpGRC3  to store Pyxis objects with morphological
        analysis.

        ✓ unittests : see the RhpGRC3Test class.

        about Rhp classes for Ancient Greek:
        ˮ ▪ (RhpGRC : mother class of all RhpGRC*** classes)
        ˮ ▪ RhpGRC1 : to be read by ProcessGRC1 (text in .text, a LCharAndTextPos object)
        ˮ ▪ RhpGRC2 : to be read by ProcessGRC2 (text in .text, a LCharAndTextPos object)
        ˮ ▪ RhpGRC3 : to be read by ProcessGRC3 (text in .text, a LPyxis object)
        ˮ ▪ RhpGRC4 : to be read by ProcessGRC4 (text in .text, a LPyxis object,
        ˮ                                        + in .ending_punctuation)
        ˮ
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ○ _hashvalue            : (bytes or None)
                                  Use .get_hashvalue() to read its value.
        ○ language              : (str) ISO 639-3 name of the language of self.
        ○ rhpname               : (str)
        ● text                  : (LPyxis) main attribute : Rhp text
        ○ text0                 : (str) the initial source text

        methods :
        ○ __eq__(self, other)
        ◐ __init__(self, language="grc", rhpname="RhpGRC3", text=None, text0)
        ○ __str__(self)
        ○ clone(self)
        ○ get_hashvalue(self)
        ○ report(self)
        ○ set_hashvalue(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 text0,
                 text=None,
                 language="grc",
                 rhpname="RhpGRC3"):
        """
            RhpGRC3.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENT:
            ▪ text                  : (None=LPyxis() or LPyxis) main attribute :
                                      Rhp text
            ▪ text0                 : (str) the initial source text
            ▪ language              : (str) ISO 639-3
            ▪ rhpname               : (str)
        """
        if text is None:
            text = LPyxis()

        RhpXXXmorpho.__init__(self,
                              language=language,
                              rhpname=rhpname,
                              text=text,
                              text0=text0)
################################################################################
class RhpGRC4(RhpXXXsentences):
    """
        RhpGRC4 class
        ________________________________________________________________________

        (Ancient Greek)
        Use RhpXXXsentences to store Pyxis objects grouped together into
        sentences, each sentence ending with special Pyxis object named
        .ending_punc.

        ✓ unittests : see the RhpGRC4Test class.

        about Rhp classes for Ancient Greek:
        ˮ ▪ (RhpGRC : mother class of all RhpGRC*** classes)
        ˮ ▪ RhpGRC1 : to be read by ProcessGRC1 (text in .text, a LCharAndTextPos object)
        ˮ ▪ RhpGRC2 : to be read by ProcessGRC2 (text in .text, a LCharAndTextPos object)
        ˮ ▪ RhpGRC3 : to be read by ProcessGRC3 (text in .text, a LPyxis object)
        ˮ ▪ RhpGRC4 : to be read by ProcessGRC4 (text in .text, a LPyxis object,
        ˮ                                        + in .ending_punctuation)
        ˮ
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ○ _hashvalue            : (bytes or None)
                                  Use .get_hashvalue() to read its value.
        ○ ending_punc    : None or a Pyxis1 object
        ○ language              : (str) ISO 639-3 name of the language of self.
        ○ rhpname               : (str)
        ○ text                  : (LPyxis) main attribute : Rhp text
        ○ text0                 : (str) the initial source text

        methods :
        ○ __eq__(self, other)
        ◐ __init__(self,
                   text=None, text0, ending_punc,
                   language="grc", rhpname="RhpGRC4")
        ○ __str__(self)
        ○ clone(self)
        ○ get_hashvalue(self)
        ○ report(self)
        ○ set_hashvalue(self)
        ○ uniquename(self)
    """

    #///////////////////////////////////////////////////////////////////////////SZ
    def __init__(self,
                 text0,
                 ending_punc=None,
                 language="grc",
                 rhpname="RhpGRC4",
                 text=None):
        """
            RhpGRC4.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ text                  : (LPyxis) main attribute : Rhp text
            ▪ text0                 : (str) the initial source text
            ▪ ending_punc    : None or a Pyxis1 object
            ▪ language              : (str) ISO 639-3
            ▪ rhpname               : (str)
        """
        if text is None:
            text = LPyxis()

        RhpXXXsentences.__init__(self,
                                 language=language,
                                 rhpname=rhpname,
                                 text0=text0,
                                 text=text,
                                 ending_punc=ending_punc)

################################################################################
class RhpGRC5(RhpXXXinsidesentence):
    """
        RhpGRC5 class
        ________________________________________________________________________

        ✓ unittests : see the RhpGRC5Test class.
        ________________________________________________________________________

        instance attributes :
        ○ _hashvalue            : (bytes or None)
                                  Use .get_hashvalue() to read its value.
        ○ ending_punc    : None or a Pyxis1 object
        ○ rhpname               : (str)
        ○ text                  : (DictHashvalueToPyxis) main attribute : Rhp
                                  text
        ○ text0                 : (str) the initial source text

        methods :
        ○ __eq__(self, other)
        ◐ __init__(self, text0)
        ○ __str__(self)
        ○ clone(self)
        ○ get_hashvalue(self)
        ○ report(self)
        ○ set_hashvalue(self)
        ○ uniquename(self)
    """
    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 text0,
                 text=None,
                 ending_punc=None,
                 language="grc",
                 rhpname="RhpGRC5"):
        """
            RhpGRC5.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ language              : (str) ISO 639-3
            ▪ rhpname               : (str)
            ▪ text                  : (DictHashvalueToPyxis) main attribute :
                                      Rhp text
            ▪ text0                 : (str) the initial source text
            ▪ ending_punc    : None or a Pyxis1 object
        """
        if text is None:
            text = DictHashvalueToPyxis()

        RhpXXXinsidesentence.__init__(self,
                                      language=language,
                                      rhpname=rhpname,
                                      text=text,
                                      text0=text0,
                                      ending_punc=ending_punc)

################################################################################
class Lector(object):
    """
        Lector class
        ________________________________________________________________________

        Main class of the project.

        Read a (str)self.text0 text with the help of the .processes .
        ________________________________________________________________________

        no class attribute

        instance attributes :
        ● all_rhp                       : a RhpContainer object
        ● done_with                     : DictStr2LBytes
        ● processes                     : a ProcessContainer object
        ● turn_number                   : (int)

        methods :
        ● __init__(self, text0, processes)
        ● __str__(self)
        ● add_rhp(self, new_rhp)
        ● read(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 text0,
                 processes):
        """
            Lector.__init__()
            ____________________________________________________________________

            ARGUMENTS:
            ▪ text0                         : (str) the initial source text
            ▪ processes                     : a ProcessContainer object
        """
        self.text0 = text0

        self.turn_number = 0
        self.done_with = DictStr2LBytes()

        self.all_rhp = RhpContainer()
        self.processes = processes

        # let's add the first Rhp object :
        self.add_rhp(Rhp0(text0=text0))

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
            Lector.__str__()
            ____________________________________________________________________

            Return a human-readable representation of self.
            ____________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : the expected string
        """
        res = ""
        res += "list of the reading hypotheses :\n"
        res += add_prefix_before_line("    ", str(self.all_rhp))

        res += "\nprocesses:\n"
        res += add_prefix_before_line("    ", str(self.processes))
        return res

    #///////////////////////////////////////////////////////////////////////////
    def add_rhp(self,
                new_rhp):
        """
            Lector.add_rhp()
            ____________________________________________________________________

            Add the Rhp object <new_rhp> into self.
            ____________________________________________________________________

            ARGUMENT:
            ▪ new_rhp           : an Rhp object

            no RETURNED VALUE
        """
        self.all_rhp.add(new_rhp)

    #///////////////////////////////////////////////////////////////////////////
    def read(self):
        """
            Lector.read()
            ____________________________________________________________________

            Renvoie True s'il faut continuer, False si on peut stopper la boucle.
        """
        self.turn_number += 1
        LOGGER.info("=== turn number : %s ===", self.turn_number)
        LOGGER.info("= done_with =\n" +\
                    add_prefix_before_line("      ", str(self.done_with)))

        # we try to launch all processes :

        # if no process has been launched and if the the number of rhp is constant,
        # we stop the loop :
        nbr_of_applied_processes = 0
        ancient_number_of_rhp = len(self.all_rhp)

        rhp_to_be_added = LRhp()
        for process_name in self.processes:
            process = self.processes[process_name]

            if process_name not in self.done_with:
                self.done_with[process_name] = LProcess()

            for rhphashvalue in self.all_rhp:
                rhp = self.all_rhp[rhphashvalue]
                if rhphashvalue not in self.done_with[process_name] and \
                   process.to_be_applied_to.__name__ == rhp.rhpname:
                    # ok, let's apply rhphashvalue to self.all_rhp[rhphashvalue]
                    # and let's store the future new rhp :
                    target_rhp = self.all_rhp[rhphashvalue]
                    LOGGER.debug("= let's apply %s " \
                                 "to %s.",
                                 process.uniquename(),
                                 target_rhp.uniquename())

                    newrhps = process.read(target_rhp=target_rhp,
                                           text0=self.text0)
                    LOGGER.debug("Process '%s' applied to %s returned %s object(s) : %s",
                                 process.processname,
                                 target_rhp.uniquename(),
                                 len(newrhps),
                                 [rhp.uniquename() for rhp in newrhps])

                    for new_rhp in newrhps:
                        rhp_to_be_added.append(new_rhp)

                    if process_name not in self.done_with:
                        self.done_with[process_name] = [rhphashvalue,]
                    else:
                        self.done_with[process_name].append(rhphashvalue)

        for rhp in rhp_to_be_added:
            self.all_rhp.add(rhp)

        res = True
        if nbr_of_applied_processes == 0 and ancient_number_of_rhp == len(self.all_rhp):
            LOGGER.info("Lector.read() : end of the main loop")
            res = False

        return res
