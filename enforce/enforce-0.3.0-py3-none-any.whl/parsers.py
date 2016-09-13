import typing

from . import nodes
from .types import EnhancedTypeVar


def get_parser(node, hint, validator, parsers=None):
    """
    Yields a parser function for a given type hint
    """
    if parsers is None:
        parsers = TYPE_PARSERS

    if type(hint) == type:
        parser = parsers.get(hint, _parse_default)
    else:
        parser = parsers.get(type(hint), _parse_default)

    yield parser(node, hint, validator, parsers)


def _parse_default(node, hint, validator, parsers):
    new_node = yield nodes.SimpleNode(hint)
    validator.all_nodes.append(new_node)
    yield _yield_parsing_result(node, new_node)


def _parse_union(node, hint, validator, parsers):
    """
    Parses Union type
    Union type has to be parsed into multiple nodes
    in order to enable further validation of nested types
    """
    new_node = yield nodes.UnionNode()
    validator.all_nodes.append(new_node)
    for element in hint.__union_params__:
        yield get_parser(new_node, element, validator, parsers)
    yield _yield_parsing_result(node, new_node)


def _parse_type_var(node, hint, validator, parsers):
    try:
        new_node = validator.parent.roots[hint.__name__]
    except (KeyError, AttributeError):
        try:
            new_node = validator.globals[hint.__name__]
        except KeyError:
            covariant = hint.__covariant__
            contravariant = hint.__contravariant__
            new_node = yield nodes.TypeVarNode(covariant=covariant, contravariant=contravariant)
            if hint.__bound__ is not None:
                yield get_parser(new_node, hint.__bound__, validator, parsers)
            elif hint.__constraints__:
                for constraint in hint.__constraints__:
                    yield get_parser(new_node, constraint, validator, parsers)
            else:
                yield get_parser(new_node, typing.Any, validator, parsers)
            validator.globals[hint.__name__] = new_node
            validator.all_nodes.append(new_node)

    yield _yield_parsing_result(node, new_node)


def _parse_tuple(node, hint, validator, parsers):
    if hint.__tuple_params__ is None:
        yield _parse_default(node, hint, validator, parsers)
    else:
        new_node = yield nodes.TupleNode(variable_length=hint.__tuple_use_ellipsis__)
        for element in hint.__tuple_params__:
            yield get_parser(new_node, element, validator, parsers)
        yield _yield_parsing_result(node, new_node)


def _parse_callable(node, hint, validator, parsers):
    new_node = yield nodes.CallableNode(hint)
    validator.all_nodes.append(new_node)
    yield _yield_parsing_result(node, new_node)


def _parse_complex(node, hint, validator, parsers):
    """
    In Python both float and integer numbers can be used in place where
    complex numbers are expected
    """
    hints = [complex, int, float]
    yield _yield_unified_node(node, hints, validator, parsers)


def _parse_bytes(node, hint, validator, parsers):
    """
    Bytes should sldo accept bytearray and memoryview, but not otherwise
    """
    hints = [bytearray, memoryview, bytes]
    yield _yield_unified_node(node, hints, validator, parsers)


def _parse_generic(node, hint, validator, parsers):
    if issubclass(hint, typing.List):
        yield _parse_list(node, hint, validator, parsers)
    elif issubclass(hint, typing.Dict):
        yield _parse_default(node, hint, validator, parsers)
    else:
        new_node = yield nodes.GenericNode(hint)
        validator.all_nodes.append(new_node)
        yield _yield_parsing_result(node, new_node)


def _parse_list(node, hint, validator, parsers):
    new_node = yield nodes.SimpleNode(hint.__extra__)
    validator.all_nodes.append(new_node)

    # add its type as child
    # We can index first as Lists only ever have 1 parameter
    if hint.__args__:
        yield get_parser(new_node, hint.__args__[0], validator, parsers)

    yield _yield_parsing_result(node, new_node)


def _yield_unified_node(node, hints, validator, parsers):
    new_node = yield nodes.UnionNode()
    validator.all_nodes.append(new_node)
    for element in hints:
        yield _parse_default(new_node, element, validator, parsers)
    yield _yield_parsing_result(node, new_node)


def _yield_parsing_result(node, new_node):
    # Potentially reducing the runtime efficiency
    # Need some evidences to decide what to do
    # with this piece of code next
    if node:
        node.add_child(new_node)
    else:
        yield new_node


TYPE_PARSERS = {
    typing.UnionMeta: _parse_union,
    typing.TupleMeta: _parse_tuple,
    typing.GenericMeta: _parse_generic,
    typing.CallableMeta: _parse_callable,
    typing.TypeVar: _parse_type_var,
    EnhancedTypeVar: _parse_type_var,
    complex: _parse_complex,
    bytes: _parse_bytes
    }
