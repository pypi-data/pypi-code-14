from lxml import etree as ET

__version__ = '0.1'

# This model has been built to conform with the Rosetta DNX AIP data model as of 
# Version 5.0 (released March 2016, available at:
# http://knowledge.exlibrisgroup.com/@api/deki/files/39700/Rosetta_AIP_Data_Model.pdf)
# (last visited 4th August 2016)


METS_NS = "http://www.loc.gov/METS/"
XLIN_NS = "http://www.w3.org/1999/xlink"
DNX_NS = "http://www.exlibrisgroup.com/dps/dnx"

mets_nsmap = {
    'mets': METS_NS,
    }

xlin_nsmap = {
    'xlin': XLIN_NS
}

dnx_nsmap = {
    'dnx': DNX_NS
}

ET.register_namespace('mets', METS_NS)
ET.register_namespace('xlin', XLIN_NS)
ET.register_namespace('dnx', DNX_NS)

strict = True
class Dnx(ET.ElementBase):
    TAG = '{http://www.exlibrisgroup.com/dps/dnx}dnx'





# class Dnx(ET.ElementBase):
#   TAG = '{http://www.exlibrisgroup.com/dps/dnx}dnx'


# class Dnx(ET.ElementBase):
#   TAG = '{http://www.exlibrisgroup.com/dps/dnx}dnx'


# class Dnx(ET.ElementBase):
#   TAG = '{http://www.exlibrisgroup.com/dps/dnx}dnx'


# class Dnx(ET.ElementBase):
#   TAG = '{http://www.exlibrisgroup.com/dps/dnx}dnx'