import jinja2
from jinja2.compiler import CodeGenerator


class ReferenceFinderGenerator(CodeGenerator):
    def __init__(self, environment):
        CodeGenerator.__init__(self, environment, '<introspection>',
                               '<introspection>')
        
        self._getattr_stack = 0 
        self._varstack = []
        self._undeclared = set()

    def write(self, x):
        pass
    
    def visit_Name(self, node, frame):
        if self._getattr_stack == 0:
            self._undeclared.add(node.name)
        else:
            self._varstack.append(node.name)

    def visit_Getattr(self, node, frame):
        self._getattr_stack+=1
        self.visit(node.node, frame)
        self._varstack.append(node.attr)
        self._getattr_stack-=1

        if(self._getattr_stack == 0):
            self._undeclared.add('.'.join(self._varstack))
            self._varstack = []


def get_referenced_template_vars(ast):
    codegen = ReferenceFinderGenerator(ast.environment)
    codegen.visit(ast)

    return codegen._undeclared