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
    ❏DChars❏ : dchars/successivetransformations.py
"""
from dchars.errors.errors import DCharsError

################################################################################
class Transformation(object):
    """
        class Transformation : <Transformation> objects are stored in (and used
        by) <SuccessiveTransformations> objects
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self, dstring_type = None, direction = 0):
        """
                Transformation.__init__

                dstring_type    :       object created by dchars.py::new_dstring()
                                        function
                direction       :       (int) either +1 (=text->transliteration),
                                        either -1 (transliteration->text),
                                        either 0 (unset)
        """
        self.dstring_type = dstring_type
        self.direction = direction

        # <result> will store the result of the transformation after the
        # function self.apply() being called.
        self.result = ""

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
                Transformation.__str__
        """
        return "(Transformation) dstring_type={0}; direction={1}; result={2}".format(
                                                       self.dstring_type,
                                                       self.direction,
                                                       self.result)

    #///////////////////////////////////////////////////////////////////////////
    def apply(self, sourcetext):
        """
                Transformation.apply

                Apply the transformation defined in <self> to <sourcetext>.
                Initialize self.result and return self.result.
        """

        if self.direction == +1:
            self.result = self.dstring_type(sourcetext).get_transliteration()

        elif self.direction == -1:
            self.result = str(self.dstring_type().init_from_transliteration(sourcetext))

        else:
            raise DCharsError( context = "Transformation.apply",
                               message = "invalid direction : "+str(self.direction))

        return self.result

    #///////////////////////////////////////////////////////////////////////////
    def is_ready_to_be_applied(self):
        """
                Transformation.is_ready_to_be_applied

                Verify that <self> is ok.
        """

        if self.dstring_type is None:
            return False

        if self.direction == 0:
            return False

        return True

################################################################################
class SuccessiveTransformations(list):
    """
        class SuccessiveTransformations : a list of <Transformation> objects
    """

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
                SuccessiveTransformations.__str__
        """
        res = [ str(stransf) for stransf in self ]

        return "\n*".join(res)

    #///////////////////////////////////////////////////////////////////////////
    def add(self, dstring_type, direction):
        """
                SuccessiveTransformations.add

                Create a new <Transformation> object at the end of <self>

                dstring_type, direction : see Transformation.__init__
        """
        self.append( Transformation(dstring_type = dstring_type,
                                    direction = direction, ))

    #///////////////////////////////////////////////////////////////////////////
    def apply(self, sourcetext, limit_to_the_number_of_transf=999):
        """
                SuccessiveTransformations.apply

				sourcetext    : (str)
				limit_to_the_number_of_transf : (int)

                Apply the successive transformations to <sourcetext>, return
                the last result.
        """
        for index_transf, transf in enumerate(self):

            if index_transf+1 > limit_to_the_number_of_transf:
                break

            else:
                if index_transf == 0:
                    transf.apply(sourcetext)
                else:
                    transf.apply( self[index_transf-1].result )

        return self[-1].result
