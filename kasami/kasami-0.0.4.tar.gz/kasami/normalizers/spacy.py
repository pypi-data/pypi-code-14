from ..nodes import SymbolNode, TerminalNode


def normalize_tree(spacy_doc):
    for t in spacy_doc:
        if t.head is t:
            root = t
    return _treeify_at(root, spacy_doc)


def _treeify_at(token, spacy_doc):
    if token.left_edge == token.right_edge:
        return TerminalNode(spacy_doc.vocab.strings[token.tag], str(token))
    else:
        root = TerminalNode(spacy_doc.vocab.strings[token.tag], str(token))
        sorted_i_trees = sorted([(child.i, _treeify_at(child, spacy_doc))
                                 for child in token.children] +
                                [(token.i, root)])

        return SymbolNode(spacy_doc.vocab.strings[token.dep],
                          tuple(tree for _, tree in sorted_i_trees))
