import reflectutils
import lxml.etree


cls = reflectutils.getclass(lxml.etree._Element)
print reflectutils.fullname(cls)