from ..nodes import SymbolNode, TerminalNode


def normalize_tree(bllip_tree):
    if len(bllip_tree.subtrees()) == 0:
        return TerminalNode(bllip_tree.label, str(bllip_tree.token))
    else:

        produces = tuple(normalize_tree(sub_tree)
                         for sub_tree in bllip_tree.subtrees())
        return SymbolNode(bllip_tree.label, produces)
