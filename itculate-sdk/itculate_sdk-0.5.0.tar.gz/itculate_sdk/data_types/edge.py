from .utils import ReadOnlyDict, check_keys

_EDGE_TYPE_ATTR = "_type"
_EDGE_SOURCE_KEYS_ATTR = "_source_keys"
_EDGE_TARGET_KEYS_ATTR = "_target_keys"


class Edge(object):
    def __init__(self, edge_type, source_keys=None, source_vertex=None, target_keys=None, target_vertex=None):
        """
        :param str edge_type: Edge type
        :param dict[str, str] source_keys: Dictionary of source keys to point to a vertex (can be a partial set of keys)
        :param Vertex source_vertex: Alternative to source_keys - provide a vertex to take keys from
        :param dict[str, str] target_keys: Same as source_keys - but for target vertex
        :param Vertex target_vertex: Alternative to target_keys - provide a vertex to take keys from
        """

        if source_keys is not None:
            check_keys(source_keys)

        else:
            assert source_vertex is not None, "Must provide either source_keys or source_vertex"
            source_keys = source_vertex.keys

        if target_keys is not None:
            check_keys(target_keys)

        else:
            assert target_vertex is not None, "Must provide either source_keys or source_vertex"
            target_keys = target_vertex.keys

        assert source_keys != target_keys, "Source and target are the same (Edge cannot point to itself)"

        self._d = ReadOnlyDict({
            _EDGE_TYPE_ATTR: edge_type,
            _EDGE_SOURCE_KEYS_ATTR: source_keys,
            _EDGE_TARGET_KEYS_ATTR: target_keys,
        })

    def __str__(self):
        return "Edge {}: {} => {}".format(self.type, self.source_keys, self.target_keys)

    @property
    def type(self):
        """ :rtype: str """
        return self._d[_EDGE_TYPE_ATTR]

    @property
    def source_keys(self):
        """ :rtype: dict[str, str] """
        return self._d[_EDGE_SOURCE_KEYS_ATTR]

    @property
    def target_keys(self):
        """ :rtype: dict[str, str] """
        return self._d[_EDGE_TARGET_KEYS_ATTR]

    # noinspection PyProtectedMember
    def __cmp__(self, other):
        c = cmp(self.source_keys, other.source_keys)
        if c != 0:
            return c

        return cmp(self.target_keys, other.target_keys)

    @property
    def document(self):
        """
        :rtype: dict[str, str]
        :return: Document (Read-only) representing this edge
        """
        return self._d