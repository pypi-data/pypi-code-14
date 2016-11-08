from __future__ import unicode_literals

from collections import OrderedDict

from six import StringIO
from ._pretty_xml import WritePrettyXMLElement
from xml.etree import ElementTree
import six


class XmlFactory(object):
    """
    Fast and easy XML creation class.

    This class provides a simple a fast way of creating XML files in Python. It tries to deduce as
    much information as possible, creating intermediate elements as necessary.

    Example:
        xml = XmlFactory('root')

        xml['alpha/bravo/charlie'] # Create intermediate nodes
        xml['alpha/bravo.one'] # Create attribute on "alpha/bravo" tag
        xml['alpha/delta'] = 'XXX' # Create delta tag with text

        xml.Write('filename.xml') # Always write with a pretty XML format
    """

    def __init__(self, root_element):
        """
        :param str|Element root_element:
        """
        if isinstance(root_element, six.string_types):
            self.root = ElementTree.Element(root_element, attrib=OrderedDict())
        elif isinstance(root_element, ElementTree.Element):
            self.root = root_element
        else:
            raise TypeError("Unknown root_element parameter type: %s" % type(root_element))

    def __setitem__(self, name, value):
        """
        Create a new element or attribute:

        :param unicode name:
            A XML path including or not an attribute definition

        :param unicode value:
            The value to associate with the element or attribute

        :returns Element:
            Returns the element created.
            If setting an attribute value, returns the owner element.

        @examples:
            xml['alpha/bravo'] = 'XXX' # Create bravo tag with 'XXX' as text contents
            xml['alpha.class'] = 'CLS' # Create alpha with the attribute class='CLS'
        """
        if '@' in name:
            element_name, attr_name = name.rsplit('@')
            result = self._obtain_element(element_name)
            result.attrib[attr_name] = str(value)
        else:
            result = self._obtain_element(name)
            result.text = six.text_type(value)
        return XmlFactory(result)

    def __getitem__(self, name):
        """
        Create and returns xml element.

        :param unicode name:
            A XML path including or not an attribute definition.

        :rtype: Element
        :returns:
            Returns the element created.
        """
        assert '@' not in name, 'The "at" (@) is used for attribute definitions'
        result = self._obtain_element(name)
        return XmlFactory(result)

    def _obtain_element(self, name):
        """
        Create and returns a xml element with the given name.

        :param unicode name:
            A XML path including. Each sub-client tag separated by a slash.
            If any of the parts ends with a "+" it creates a new sub-element in that part even if
            it already exists.
        """
        parent = self.root
        if name == '':
            # On Python 2.7 parent.find('') returns None instead of the parent itself
            result = parent
        else:
            parts = name.split('/')
            for i_part in parts:
                if i_part.endswith('+'):
                    i_part = i_part[:-1]
                    result = ElementTree.SubElement(parent, i_part, attrib=OrderedDict())
                else:
                    result = parent.find(i_part)
                    if result is None:
                        result = ElementTree.SubElement(parent, i_part, attrib=OrderedDict())
                parent = result
        return result

    def print_(self, oss=None, xml_header=False):
        """
        Prints the resulting XML in the stdout or the given output stream.

        :type oss: file-like object | None
        :param oss:
            A file-like object where to write the XML output. If None, writes the output in the
            stdout.
        """

        if oss is None:
            import sys
            oss = sys.stdout

        if xml_header:
            oss.write('<?xml version="1.0" ?>\n')
        WritePrettyXMLElement(oss, self.root)

    def write(self, filename, xml_header=False):
        """
        Writes the XML in a file with the given filename.

        :param unicode filename:
            A filename.
        """
        with open(filename, 'w') as f:
            f.write(self.get_contents(xml_header=xml_header))

    def get_contents(self, xml_header=False):
        """
        Returns the resulting XML.

        :return unicode:
        """
        oss = StringIO()
        self.print_(oss, xml_header=xml_header)
        return oss.getvalue()

    def as_dict(self):
        """
        Returns the data-structure as dict.

        :return dict:

        Code from: http://code.activestate.com/recipes/410469-xml-as-dictionary/
        """

        def xml_to_list(aList):
            result = []
            for element in aList:
                if element:
                    # treat like dict
                    if len(element) == 1 or element[0].tag != element[1].tag:
                        result.append(xml_to_dict(element))
                    # treat like list
                    elif element[0].tag == element[1].tag:
                        result.append(xml_to_list(element))
                elif element.text:
                    text = element.text.strip()
                    if text:
                        result.append(text)
            return result

        def xml_to_dict(parent_element):
            """
            Example usage:

            >>> tree = ElementTree.parse('your_file.xml')
            >>> root = tree.getroot()
            >>> xmldict = XmlDictConfig(root)

            Or, if you want to use an XML string:

            >>> root = ElementTree.XML(xml_string)
            >>> xmldict = XmlDictConfig(root)

            And then use xmldict for what it is... a dict.
            """
            def _dict(*values):
                return OrderedDict(values)

            result = _dict()
            if parent_element.items():
                result.update(dict(parent_element.items()))
            for element in parent_element:
                if element:
                    # treat like dict - we assume that if the first two tags
                    # in a series are different, then they are all different.
                    if len(element) == 1 or element[0].tag != element[1].tag:
                        aDict = xml_to_dict(element)
                    # treat like list - we assume that if the first two tags
                    # in a series are the same, then the rest are the same.
                    else:
                        # here, we put the list in dictionary; the key is the
                        # tag name the list elements all share in common, and
                        # the value is the list itself
                        aDict = _dict((element[0].tag, xml_to_list(element)))
                    # if the tag has attributes, add those to the dict
                    if element.items():
                        aDict.update(dict(element.items()))
                    result.update(_dict((element.tag, aDict)))
                # this assumes that if you've got an attribute in a tag,
                # you won't be having any text. This may or may not be a
                # good idea -- time will tell. It works for the way we are
                # currently doing XML configuration files...
                elif element.items():
                    result.update(_dict((element.tag, OrderedDict(sorted(element.items())))))
                # finally, if there are no child tags and no attributes, extract
                # the text
                else:
                    result.update(_dict((element.tag, element.text)))
            return result

        # return _elem2list(self.root, return_children=True)
        return xml_to_dict(self.root)

    def as_json(self):
        """
        Returns the data-structure as a JSON.

        :return unicode:
        """
        import json
        return json.dumps(self.as_dict())
