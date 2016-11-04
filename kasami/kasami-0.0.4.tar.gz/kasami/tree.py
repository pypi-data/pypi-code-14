from deltas import RegexTokenizer

from .nodes import SymbolNode, TerminalNode

tokenizer = RegexTokenizer([
    ("open_b", r"\("),
    ("close_b", r"\)"),
    ("symbol", r"[^ \(\)'\"]+"),
    ("literal", r"'[^']+'|" + r'"[^"]+"')
])


def parse(line):
    tokens = tokenizer.tokenize(line)
    return _parse(tokens)


def _parse(tokens, offset=0):
    if tokens[offset].type != "open_b":
        raise ValueError("Parse at {0} does not start with {1}, but rather {2}"
                         .format(offset, "(", tokens[offset]))
    elif tokens[offset + 1].type != "symbol":
        raise ValueError("Parse at {0} does not have a symbol, but rather {2}"
                         .format(offset + 1, tokens[offset + 1].type))

    symbol = str(tokens[offset + 1])

    if tokens[offset + 2].type == "open_b":
        nodes = tuple(_parse(tokens, sub_offset)
                      for sub_offset in _get_sub_b_offsets(tokens, offset))

        return SymbolNode(symbol, nodes)

    elif tokens[offset + 2].type == "literal":
        return TerminalNode(symbol, str(tokens[offset + 2].strip("'\"")))


def _get_sub_b_offsets(tokens, offset):
    if tokens[offset].type != "open_b":
        raise ValueError("Parse at {0} does not start with {1}, but rather {2}"
                         .format(offset, "(", tokens[offset]))
    depth = 0
    for i, token in enumerate(tokens[offset:]):
        if token.type == "open_b":
            depth += 1
            if depth == 2:
                yield offset + i
        elif token.type == "close_b":
            depth -= 1

        if depth == 0:
            break
