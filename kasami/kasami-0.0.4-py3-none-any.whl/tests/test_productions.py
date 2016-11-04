from nose.tools import assert_not_equals, eq_

from ..productions import SymbolProduction, TerminalProduction


def test_productions():
    tp = TerminalProduction("NN", "foo")
    eq_(tp.produces, "foo")
    eq_(str(tp), "(NN 'foo')")
    eq_(repr(tp), "TerminalProduction('NN', 'foo')")

    sp = SymbolProduction("NN", ["VP", "ADJ"])
    eq_(sp.produces, ("VP", "ADJ"))
    eq_(str(sp), "(NN VP ADJ)")
    eq_(repr(sp), "SymbolProduction('NN', ('VP', 'ADJ'))")

    eq_(SymbolProduction("NN", ["VP", "ADJ"]),
        SymbolProduction("NN", ["VP", "ADJ"]))

    assert_not_equals(SymbolProduction("NN", ["VP", "ADJ"]),
                      SymbolProduction("NN", ["VP", "DERP"]))

    eq_(TerminalProduction("NN", "foo"),
        TerminalProduction("NN", "foo"))

    assert_not_equals(TerminalProduction("NN", "foo"),
                      TerminalProduction("NN", "derp"))

    eq_(hash(TerminalProduction("NN", "foo")),
        hash(TerminalProduction("NN", "foo")))

    assert_not_equals(hash(TerminalProduction("NN", "foo")),
                      hash(TerminalProduction("NN", "derp")))

    eq_(hash(SymbolProduction("NN", ["VP", "ADJ"])),
        hash(SymbolProduction("NN", ["VP", "ADJ"])))

    assert_not_equals(hash(SymbolProduction("NN", ["VP", "ADJ"])),
                      hash(SymbolProduction("NN", ["VP", "DERP"])))
