import yaml, collections, os
from jinja2 import Template, Environment
from .context import Context
import ast
from .meta import get_referenced_template_vars
from collections import namedtuple


class DependencyGraph(object):

    def __init__(self, template, refs, parent, node_key, resolved=False):
        self.template = template
        self.refs = refs or set()
        self.parent = parent
        self.node_key = node_key
        self.resolved = resolved

class TYamlProcessors(object):

    @classmethod
    def mixins(cls, resolver, current_context, template_env, value):
        for mixin in value:
            base_dir = os.path.dirname(resolver._original_file) if resolver._original_file else os.getcwd()
            base_file_path = os.path.abspath(os.path.join(
                base_dir,
                mixin
            ))

            parent_resolver = TYamlResolver.new_from_path(base_file_path)
            parent_context = parent_resolver.resolve(Context(), template_env=template_env)
            
            current_context.add(parent_context.data)
            current_context.add_parent(parent_context) 
        

class TYamlResolver(object):

    processors = {
        'tyaml.mixins': TYamlProcessors.mixins
    }

    def __init__(self, data):
        self._original_file = None
        self._data = data

    @classmethod
    def new_from_path(cls, abs_path):
        yaml_source = None

        with open(abs_path, 'r') as stream:
            yaml_source = yaml.load(stream)

        resolver = TYamlResolver(yaml_source)
        resolver._original_file = abs_path

        return resolver

    @classmethod
    def new_from_string(cls, content):
        resolver = TYamlResolver(yaml.load(content))
        resolver._original_file = None

        return resolver

    def resolve(self, context=None, globals=None, template_env=None):
        if context is None: context = Context()
        if template_env is None: 
            template_env = Environment()
            template_env.globals.update(globals) 

        context.add(self._data)
        def enumerate_object(obj):
            try:
                return obj.items()
            except:
                return enumerate(obj)

        def walk_dict(node, keys=None):
            if not keys: keys = []

            for key, item in enumerate_object(node):
                key_chain = keys + [key,]

                yield node, key_chain, item

                if isinstance(item, collections.Mapping) or isinstance(item, list):
                    for i in walk_dict(item, key_chain): yield i

        pre_processors = []
        
        # get a list of pre-processors to handle tyaml directives easier
        for parent, key_chain, item in walk_dict(context._data):
            key = join_key_chain(key_chain)
            
            processor = TYamlResolver.processors.get(key, None)
            if processor:
                pre_processors += [(processor, item, parent, key_chain[-1], key_chain)]
        
        # apply the pre-processors
        for processor, item, node_parent, node_key, key_chain in pre_processors:
            processor(self, context, template_env, item)
            context.delete_node(key_chain)

        dependent_nodes = {
            ROOT_REF_KEY: DependencyGraph(self._data, set(), None, None)
        }

        def resolve(parent, key, item):
            if isinstance(item, str):
                template = template_env.from_string(item)
                value = template.render(context.data)
                
                try:
                    value = ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    pass # We just leave it as a string

                parent[key] = value
            else:
                parent[key] = item

        # do variable substitution on any strings, since they may contain template variables
        for parent, key_chain, item in walk_dict(context._data):
            syntax_tree = template_env.parse(item)
            referenced_vars = get_referenced_template_vars(syntax_tree)
            dep = DependencyGraph(item, referenced_vars, parent, key_chain[-1])
            
            dependent_nodes[join_key_chain(key_chain[:-1])].refs.add(join_key_chain(key_chain))
                
            dependent_nodes[join_key_chain(key_chain)] = dep 
                

        def solve_dependencies(dep):
            for ref_key in dep.refs:
                ref = dependent_nodes.get(ref_key, None)

                if ref and not ref.resolved:
                    solve_dependencies(ref)

            # The root node will not have any possible substitutions,
            # so we can skip resolving it
            if dep.parent:
                resolve(dep.parent, dep.node_key, dep.template)

            dep.resolved = True

        for dep in dependent_nodes.values():
            solve_dependencies(dep)

        return context

ROOT_REF_KEY = ''
def join_key_chain(key_chain):
    return '.'.join([str(i) for i in key_chain]).lower()