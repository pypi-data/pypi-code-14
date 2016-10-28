from pylib.misc import dictutils


def test_remove_nones():
    cleaned = dictutils.remove_nones(dict(id=12, name=None))
    assert len(cleaned) == 1
    assert 'id' in cleaned


def test_remove_empty():
    cleaned = dictutils.remove_empty(dict(id=12, name=None))
    assert len(cleaned) == 1
    assert 'id' in cleaned


def test_merge_dict():
    one, two = dict(id=1), dict(name='Arewa')
    three = dictutils.merge_dict(one, two)
    assert one != three
    assert two != three
    assert len(three) == 2


def test_dict_items():
    items = dictutils.dict_items(dict(id=2, name='Arewa'))
    assert isinstance(items[0], tuple)
    assert len(items) == 2
    assert len(items[0]) == 2


def test_only():
    clean = dictutils.only(['name', 'age'])
    cleaned = clean(dict(id=1, name='Arewa', age=23))
    assert len(cleaned) == 2


def test_but():
    clean = dictutils.but(['name', 'age'])
    cleaned = clean(dict(id=1, name='Arewa', age=23))
    assert len(cleaned) == 1


def has_content():
    empty = dict(id=None, age='', name=None)
    partialempty = dict(id=None, age=0, name=None)
    assert not dictutils.is_empty(empty)
    assert dictutils.is_empty(partialempty)
