# -*- coding: utf-8 -*-
from __future__ import print_function
import shlex
import click
from hashlib import sha1
from . import config
from .basexml import BaseXML
from .fucking_string import ensure_utf8, is_string_type


def read_python_file(pypath):
    vars = {}
    with open(pypath, 'rb') as fp:
        exec(compile(fp.read(), pypath, 'exec'), {}, vars)
    return vars


def get_checksum(s):
    return sha1(ensure_utf8(s).encode('utf-8')).hexdigest()[:7]


def escape_string(s):
    """Keep char unchanged if char is number or letter or unicode"""
    chs = []
    for ch in s:
        ch = ch if ord(ch) > 128 or ch.isalnum() else ' '
        chs.append(ch)

    # remove multiple whitespaces and replace whitespace with '_'
    return '_'.join(''.join(chs).split())


def encode_with_utf8(o):
    """Encode object `o` with UTF-8 recursively"""
    if is_string_type(o):
        return ensure_utf8(o)

    if is_list_or_tuple(o):
        return type(o)([encode_with_utf8(item) for item in o])
    elif isinstance(o, dict):
        for k in o.keys():
            o[encode_with_utf8(k)] = encode_with_utf8(o.pop(k))
        return o
    else:
        raise TypeError('Cannot encode %s with UTF-8' % o.__repr__())


def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False


def is_list_or_tuple(obj):
    return isinstance(obj, (list, tuple))


def split_ignore_quote(s):
    return shlex.split(s)


def remove_all_space(s):
    return ''.join(s.split())


def is_xml_element_equal(node1, node2):
    if len(node1) != len(node2):
        return False
    if node1.tag != node2.tag:
        return False
    if node1.attrib != node2.attrib:
        return False

    text1 = '' if node1.text is None else remove_all_space(node1.text)
    text2 = '' if node2.text is None else remove_all_space(node2.text)
    return text1 == text2


def is_xml_tree_equal(tree1, tree2, ignore_tags=tuple()):
    if tree1.tag == tree2.tag and tree1.tag in ignore_tags:
        return True
    elif is_xml_element_equal(tree1, tree2):
        elems1 = list(tree1)
        elems2 = list(tree2)

        for i in range(len(elems1)):
            if not is_xml_tree_equal(elems1[i], elems2[i], ignore_tags=ignore_tags):
                return False
        return True
    else:
        return False


def assert_xml_equal(xml_tree1, xml_tree2, ignore_tags=tuple()):
    if isinstance(xml_tree1, BaseXML):
        xml_tree1 = xml_tree1.__str__()
    if isinstance(xml_tree2, BaseXML):
        xml_tree2 = xml_tree2.__str__()

    nospaces1 = ''.join(xml_tree1.split())
    nospaces2 = ''.join(xml_tree2.split())
    xml_tree1 = BaseXML.parse_string(xml_tree1)
    xml_tree2 = BaseXML.parse_string(xml_tree2)

    if nospaces1 != nospaces2:
        assert(is_xml_tree_equal(xml_tree1, xml_tree2, ignore_tags=ignore_tags))


def print_message(msg, color=None, err=False):
    """Seems `click.echo` has fixed the problem of UnicodeDecodeError when redirecting (See
    https://stackoverflow.com/questions/4545661/unicodedecodeerror-when-redirecting-to-file
    for detail). As a result, the below code used to solve the problem is conflict with `click.echo`.
    To avoid the problem, you should always use `print` with below code or `click.echo` in `__main__.py`

        if sys.version_info[0] == 2:
            sys.stdout = codecs.getwriter("utf-8")(sys.stdout)
        else:
            sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    """
    if not is_string_type(msg):
        msg = str(msg)
    click.secho(msg, fg=color, err=err)


def print_error(msg, print_stack=False):
    print_message(msg, color='red', err=True)
    if config.get('verbose'):
        import traceback
        traceback.print_exc()


def print_warning(msg):
    print_message(msg, color='yellow', err=True)


def print_info(msg):
    print_message(msg, color='green')
