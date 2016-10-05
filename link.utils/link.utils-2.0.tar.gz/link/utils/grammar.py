
from grako.parser import GrakoGrammarGenerator
from grako.codegen.python import codegen as pythoncg
from grako.util import Mapping
from grako.model import Node

from six import exec_
import imp
import sys


def codegenerator(modname, prefix, grammar):
    """
    Parse grammar model and generate Python code allowing to parse it.

    Example:

    .. code-block:: python

       with open('grammar.bnf') as f:
           module = codegenerator('mydsl', 'MyDSL', f.read())

       assert module.__name__ == 'mydsl'
       parser = module.MyDSLParser()

    :param modname: Name of the generated Python module
    :type modname: str

    :param prefix: Prefix used to name the parser
    :type prefix: str

    :param grammar: Grammar describing the language to parse
    :type grammar: str

    :returns: Generated Python module
    :rtype: module
    """

    parser = GrakoGrammarGenerator(prefix, filename=modname)
    model = parser.parse(grammar)
    code = pythoncg(model)

    module = imp.new_module(modname)
    exec_(code, module.__dict__)
    sys.modules[modname] = module

    return module


def find_ancestor(node, classname):
    """
    Find first node's ancestor which match class' name.

    :param node: Grako Node
    :type node: grako.model.Node

    :param classname: Class' name
    :type classname: str

    :returns: Node's ancestor or None if not found
    :rtype: grako.model.Node
    """

    pnode = node.parent

    while pnode is not None:
        if pnode.__class__.__name__ == classname:
            break

        pnode = pnode.parent

    return pnode
