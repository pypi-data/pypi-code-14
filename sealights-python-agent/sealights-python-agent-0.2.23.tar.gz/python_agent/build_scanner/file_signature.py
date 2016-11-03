"""
    file_signature module is part of the build scan process.
    For a given full python file path and its relative path:
        - Parse the code to ast
        - Traverse the tree
        - Calculate method hash for functions and lambdas
        - Calculate file hash
"""
import logging
import ast
import hashlib

from python_agent.packages import astunparse
from python_agent.utils import ast_utils
from python_agent.utils import exception_handler


log = logging.getLogger(__name__)


def calculate_method_hash(node):
    code = astunparse.unparse(node)
    copied_node = ast_utils.parse(code)
    if isinstance(node, ast.FunctionDef):
        copied_node = copied_node.body[0]
    if isinstance(node, ast.Lambda):
        copied_node = copied_node.body[0].value
    for traverse_node in ast.walk(copied_node):

        # we skip ourselves
        if traverse_node == copied_node:
            continue

        # we want to preserve method code so we continue to the next node if it's not a method
        if not isinstance(traverse_node, ast.FunctionDef) and not isinstance(traverse_node, ast.Lambda):
            continue

        # we reached a child node which is a method. we clean it completely
        # so changes in inner methods won't affect the parent
        ast_utils.clean_method_body(traverse_node)

    m = hashlib.md5()
    m.update(astunparse.unparse(copied_node))
    return m.hexdigest()


def is_parameterless_method(args):
    if not args or not getattr(args, "args", None) or not args.args:
        return ""


def calculate_method_sig_hash(node):
    args = getattr(node, "args", None)
    if is_parameterless_method(args):
        return ""
    params_string = ",".join(map(astunparse.unparse, args.args))
    m = hashlib.md5()
    m.update(params_string)
    return m.hexdigest()


def calculate_method_position(node):
    lineno = node.lineno
    col_offset = node.col_offset
    if hasattr(node, "decorator_list") and node.decorator_list:
        lineno = node.decorator_list[-1].lineno + 1
        col_offset = min(node.decorator_list[-1].col_offset - 1, 0)
    return lineno, col_offset


def build_method(rel_path, name, node):
    method_hash = calculate_method_hash(node)
    last_node = ast_utils.get_last_node(node)
    last_node_lineno = last_node.lineno
    last_node_col_offset = last_node.col_offset + len(astunparse.unparse(last_node).strip("\n"))
    lineno, col_offset = calculate_method_position(node)

    return {
        "id": node.sl_id,
        "name": name,
        "uniqueName": "%(name)s@%(source)s@%(lineno)s,%(col_offset)s" % {
            "name": name, "source": rel_path, "lineno": node.lineno, "col_offset": node.col_offset
        },
        "position": [lineno, col_offset],
        "endPosition": [last_node_lineno, last_node_col_offset],
        "hash": method_hash,
        "sigHash": calculate_method_sig_hash(node),
        "constructor": True if name == "__init__" else False,
        "isAnonymous": True if isinstance(node, ast.Lambda) else False
    }


@exception_handler(log, quiet=True, message="failed calculating file signature")
def calculate_file_signature(full_path, rel_path):
    result = {"methods": [], "filename": rel_path}
    with open(full_path, 'r') as f:
        code = f.read()
    tree = ast_utils.parse(code)
    for node in ast_utils.walk(tree):
        # if a lambda method is assigned, we want its name. example: foo = lambda x + y: x + y
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Lambda):
            # klass.__str__ = lambda self: self.__unicode__().encode('utf-8') doesn't work
            if node.targets and hasattr(node.targets[-1], "id"):
                setattr(node.value, "name", node.targets[-1].id)

        ast_utils.set_node_id(node, tree, rel_path)

        if not isinstance(node, ast.FunctionDef) and not isinstance(node, ast.Lambda):
            continue
        if isinstance(node, ast.FunctionDef):
            name = node.name
        elif isinstance(node, ast.Lambda) and hasattr(node, "name"):
            # lambda nodes do not have a name attribute unless we assigned one ourselves
            name = node.name
        else:
            name = "(Anonymous)"
        result["methods"].append(build_method(rel_path, name, node))

    result["hash"] = calculate_method_hash(ast_utils.parse(code))
    return result
