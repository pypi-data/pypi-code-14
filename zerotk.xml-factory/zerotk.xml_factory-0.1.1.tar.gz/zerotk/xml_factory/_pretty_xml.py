from __future__ import unicode_literals
from xml.etree import ElementTree
import six



#===================================================================================================
# WritePrettyXML
#===================================================================================================
def WritePrettyXML(iss, oss):
    '''
    Writes the iss file in pretty xml.

    :type iss: unicode or file
    :param iss:
        The iss filename or file object.

    :type oss: unicode or file
    :param oss:
        The oss filename or file opened for writing.
    '''
    if isinstance(oss, six.string_types):
        out_stream = open(oss, 'w')
        close_output = True
    else:
        out_stream = oss
        close_output = False
    try:
        tree = ElementTree.parse(iss)  # @UndefinedVariable
        WritePrettyXMLElement(out_stream, tree.getroot())
    finally:
        if close_output:
            out_stream.close()



#===================================================================================================
# WritePrettyXMLElement
#===================================================================================================
def WritePrettyXMLElement(oss, element, indent=0):
    '''
    Writes an xml element in the given file (oss) recursively, in pretty xml.

    :param file oss:
        The output file to write

    :param Element element:
        The Element instance (ElementTree)

    :param int indent:
        The level of indentation to write the tag.
        This is used internally for pretty printing.
    '''
    from xml.sax.saxutils import escape

    INDENT = '  '

    # Start tag
    oss.write(INDENT * indent + '<%s' % element.tag)
    for i_name, i_value in sorted(six.iteritems(element.attrib)):
        oss.write(' %s="%s"' % (i_name, escape(i_value)))

    if len(element) == 0 and element.text is None:
        oss.write('/>')
        return

    oss.write('>')

    # Sub-elements
    for i_element in element:
        oss.write('\n')
        WritePrettyXMLElement(oss, i_element, indent + 1)

    # Text
    if element.text is not None:
        oss.write(escape(element.text))

    # End tag
    if element.text is None:
        oss.write('\n' + INDENT * indent)
    oss.write('</%s>' % element.tag)

