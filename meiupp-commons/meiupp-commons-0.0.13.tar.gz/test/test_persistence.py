from asterix.test import dummy_master
from py2neo import Node, Relationship


class Related(Relationship):
    pass

def test_create(mocker):
    from commons import persistence

    master = dummy_master()
    mocker.patch.object(persistence, "current_app", master)
    persistence.create("asdf")
    graph = master.get("neo4j")
    assert graph.create.call_count == 1

def test_match_with_node_and_string_relationship(mocker):
    from commons import persistence

    master = dummy_master()
    node = Node("asdf")
    mocker.patch.object(persistence, "current_app", master)

    persistence._match(node, "RELATED")

    graph = master.get("neo4j")
    assert graph.match_one.call_count == 1
    graph.match_one.assert_called_once_with(node, "RELATED",
                                            bidirectional=False)


def test_match_with_node_and_relationship_class(mocker):
    from commons import persistence

    master = dummy_master()
    node = Node("asdf")
    mocker.patch.object(persistence, "current_app", master)

    persistence._match(node, Related)

    graph = master.get("neo4j")
    assert graph.match_one.call_count == 1
    graph.match_one.assert_called_once_with(node, "RELATED",
                                            bidirectional=False)

def test_match_with_node_and_relationship_object(mocker):
    from commons import persistence

    master = dummy_master()
    node = Node("asdf")
    mocker.patch.object(persistence, "current_app", master)

    persistence._match(node, Related(node))

    graph = master.get("neo4j")
    assert graph.match_one.call_count == 1
    graph.match_one.assert_called_once_with(node, "RELATED",
                                            bidirectional=False)


def test_get_related(mocker):
    from commons import persistence

    master = dummy_master()
    node = Node("asdf")
    mocker.patch.object(persistence, "current_app", master)

    persistence.get_related(node, "RELATED")

    graph = master.get("neo4j")
    assert graph.match_one.call_count == 1
    graph.match_one.assert_called_once_with(node, "RELATED",
                                            bidirectional=False)

def test_get_all_related(mocker):
    from commons import persistence

    master = dummy_master()
    node = Node("asdf")
    mocker.patch.object(persistence, "current_app", master)

    graph = getattr(master, "__components").get("neo4j")

    # Test that function does not break if returning value
    graph.match.return_value = [Related(node, node)]

    persistence.get_all_related(node, "RELATED")

    assert graph.match.call_count == 1
    graph.match.assert_called_once_with(node, "RELATED", bidirectional=False)
