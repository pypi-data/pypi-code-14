from nose.tools import eq_

from ..nodes import SymbolNode, TerminalNode


def test_nodes():
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
    expected_line = \
        ("(S " +
         "(NP (DET 'Every') (NN 'cat')) " +
         "(VP (VBZ 'loves') (NP (DET 'a') (NN 'dog')))" +
         ")")
    eq_(str(my_tree), expected_line)
