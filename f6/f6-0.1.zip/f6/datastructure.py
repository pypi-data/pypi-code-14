class Trie(object):
    '''
    >>> t = Trie()
    >>> t.add('foo', 1)
    True
    >>> 'foo' in t
    True
    >>> t.pop('foo')
    1
    >>> t['foo'] = 656
    >>> t['foo']
    656

    >>> t = Trie()
    >>> t.add('bat')
    True
    >>> t.add('bak')
    True
    >>> t.discard('bak')
    >>> t.keys()
    [['b', 'a', 't']]
    '''

    class Node(object):

        def __init__(self, parent, key, value=None):
            self.key = key
            self.parent = parent
            self.count = 1
            self.has_value = False
            self.value = value
            self.children = {}

        def __getitem__(self, key):
            return self.children[key]

        def __setitem__(self, key, node):
            self.children[key] = node
            return node

        def __contains__(self, key):
            return key in self.children

        def __str__(self):
            return '{}({}) -> {}'.format(
                self.key,
                self.count,
                self.value,
            )

    def __init__(self, keys=None):
        self.root = Trie.Node(None, None)
        if keys:
            for key in keys:
                self.add(key)

    def add(self, key, value=None):
        '''
        O(k) where k is the length of the key
        '''
        try:
            node = self._get_node(key)
            if not node.has_value:
                self._do_add(key, value)
                return True
            else:
                if node.value == value:
                    return False
                else:
                    node.value = value
                    return True
        except KeyError:
            self._do_add(key, value)
            return True

    def _do_add(self, key, value):
        node = self.root
        for c in key:
            if c not in node:
                node[c] = Trie.Node(node, c)
            else:
                node[c].count += 1
            node = node[c]
        node.has_value = True
        node.value = value

    def __contains__(self, key):
        '''
        O(k) where k is the length of the key
        '''
        try:
            return self._get_node(key).has_value
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key):
        '''
        O(k) where k is the length of the key
        '''
        return self._get_node(key).value

    def __setitem__(self, key, value):
        '''
        O(k) where k is the length of the key
        '''
        self.add(key, value)
        return value

    def remove(self, key):
        '''
        O(k) where k is the length of the key
        '''
        self.pop(key)

    def discard(self, key):
        '''
        O(k) where k is the length of the key
        '''
        try:
            self.remove(key)
        except KeyError:
            pass

    def pop(self, key):
        '''
        O(k) where k is the length of the key

        >>> t = Trie()
        >>> t.add('foo')
        True
        >>> t.pop('foo')

        >>> t.add('foo')
        True
        >>> t.add('fo')
        True
        >>> t.pop('fo')
        >>> 'foo' in t
        True
        '''
        if not key in self:
            raise KeyError
        node = self.root
        for c in key:
            node = node[c]
            node.count -= 1
            if node.count == 0:
                del node.parent.children[c]
        node.has_value = False
        return node.value

    def keys(self):

        def key(node):
            r = []
            while node.parent:
                r.append(node.key)
                node = node.parent
            return list(reversed(r))

        res = []
        st = [self.root]
        while st:
            node = st.pop()
            if not node.children:
                res.append(key(node))
            else:
                st.extend(node.children.values())
        return res

    def _get_node(self, key):
        '''
        O(k) where k is the length of the key
        '''
        node = self.root
        for c in key:
            if c not in node:
                raise KeyError
            node = node[c]
        return node

    def show(self):

        def show(node, depth=0):
            indent = ' ' * depth * 4
            print indent + str(node)
            for child in node.children.values():
                show(child, depth + 1)

        show(self.root)

class SuffixTrie(object):
    '''
    https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/suffixtrees.pdf
    '''

    class Node(object):

        def __init__(self):
            self.children = {}
            self.link = None

        def add_child(self, c, node):
            self.children[c] = node
            node.c = c

    def __init__(self, s):
        s += '$'
        self.root = root = SuffixTrie.Node()
        root.link = root
        last = SuffixTrie.Node()
        last.link = root
        root.add_child(s[0], last)
        for c in s[1:]:
            cur = last
            pre = None
            while c not in cur.children:
                new = SuffixTrie.Node()
                cur.add_child(c, new)
                if pre:
                    pre.link = new
                pre = new
                cur = cur.link
            if cur.children[c] is pre:
                pre.link = cur
            else:
                pre.link = cur.children[c]
            last = last.children[c]

    def __contains__(self, s):
        cur = self.root
        for c in s:
            if not c in cur.children:
                return False
            cur = cur.children[c]
        return bool(cur.children)

    def is_suffix(self, s):
        s += '$'
        cur = self.root
        for c in s:
            if not c in cur.children:
                return False
            cur = cur.children[c]
        return not cur.children

    def positions(self, substr):
        pass

    def show(self):

        def show_(c, root, depth=0):
            indent = depth * 4 * ' '
            print indent + c
            for child_c, child_node in root.children.items():
                show_(child_c, child_node, depth + 1)

        show_('', self.root)

    def get_node(self, s):
        cur = self.root
        for c in s:
            cur = cur.children[c]
        return cur

if __name__ == '__main__':
    import doctest as d;d.testmod()

    # test SuffixTrie
    s = 'abaaba'
    t = SuffixTrie(s)
    # contains
    for i in xrange(len(s)):
        for j in xrange(i, len(s) + 1):
            assert s[i:j] in t
    # is_suffix
    for i in xrange(len(s)):
        assert t.is_suffix(s[i:])
    t = SuffixTrie('')
    assert '' in t
    assert 'a' not in t
