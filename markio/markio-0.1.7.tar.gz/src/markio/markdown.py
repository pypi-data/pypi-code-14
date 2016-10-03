import mistune


def parse_markdown(source):
    """
    Parse markdown and return an mistune AST.
    """

    return mistune.BlockLexer()(source)


def markdown_source(nodes):
    """
    Convert markdown AST to a string of markdown source.
    """

    nodes = list(nodes)
    nodes.reverse()
    source = []
    list_env = []
    list_item_env = []

    while nodes:
        node = nodes.pop()
        tt = node['type']

        # Regular paragraph
        if tt == 'paragraph':
            source.append(node['text'] + '\n')

        # Code
        elif tt == 'code':
            code = '\n'.join('    ' + x for x in node['text'].splitlines())
            source.append(code + '\n')

        # List handling
        elif tt == 'list_start':
            node = dict(node, num_items=0)
            list_env.append(node)
        elif tt == 'list_item_start':
            list_env[-1]['num_items'] += 1
            list_item_env.append([])
        elif tt == 'text':
            text = node['text']
            if list_env:
                if list_env[-1]['ordered']:
                    number = list_env[-1]['num_items']
                    source.append('%s. %s' % (number, text))
                else:
                    source.append('* %s' % text)
            else:
                raise ValueError(node)
        elif tt == 'list_item_end':
            list_item_env.pop()
        elif tt == 'list_end':
            list_env.pop()

        # Not implemented
        else:
            raise NotImplementedError('unsupported node type: %r' % tt)

    return '\n'.join(source).rstrip('\n')
