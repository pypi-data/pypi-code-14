################################################################################
# ZMSFormatProviderAcquired.py
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
################################################################################


# Imports.
import copy
import zope.interface
# Product Imports.
import IZMSFormatProvider, ZMSFormatProvider


################################################################################
################################################################################
###
###   Class
###
################################################################################
################################################################################
class ZMSFormatProviderAcquired(
        ZMSFormatProvider.ZMSFormatProvider):
    zope.interface.implements(
        IZMSFormatProvider.IZMSFormatProvider)

    # Properties.
    # -----------
    meta_type = 'ZMSFormatProviderAcquired'

    """
    ############################################################################
    #
    #   Constructor
    #
    ############################################################################
    """

    ############################################################################
    #  ZMSFormatProvider.__init__: 
    #
    #  Initialise a new instance.
    ############################################################################
    def __init__(self, textformats=[], charformats=[]):
      self.id = 'format_manager'

    def getTextFormatDefault(self):
      return self.getPortalMaster().getTextFormatDefault()
  
    def getTextFormat(self, id, REQUEST):
      return self.getPortalMaster().getTextFormat(id, REQUEST)

    def getTextFormats(self, REQUEST):
      textformats = self.getPortalMaster().getTextFormats(REQUEST)
      return textformats

    def getCharFormats(self):
      charformats = copy.deepcopy(self.getPortalMaster().getCharFormats())
      for charformat in charformats:
        btn = charformat.get('btn')
        if type(btn) is str and btn.find('/') < 0:
          charformat['btn'] = '%s/%s'%(self.getPortalMaster().getFormatManager().absolute_url(),btn)
      return charformats

################################################################################
