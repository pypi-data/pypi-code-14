from nose.tools import eq_

from .. import tree
from ..nodes import SymbolNode, TerminalNode


def test_parse():
    my_tree = SymbolNode("S", (
        SymbolNode("NP", (
            TerminalNode("DET", "Every"),
            TerminalNode("NN", "cat")
        )),
        SymbolNode("VP", (
            TerminalNode("VBZ", "loves"),
            SymbolNode("NP", (
                TerminalNode("DET", "a"),
                TerminalNode("NN", "dog"),
            ))
        ))
    ))
    eq_(tree.parse(str(my_tree)), my_tree)
