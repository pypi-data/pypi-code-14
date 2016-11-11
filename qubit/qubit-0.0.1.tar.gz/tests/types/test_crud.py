from qubit.types import Mapper
from qubit.types import Reducer
from qubit.types import Spout
from qubit.types import Qubit


def test_mapper():
    data = {
        'name': 'test_mapper',
        'body': 'lambda x: a + x',
        'closure': {
            'a': 1
        }
    }
    mid = Mapper.create(**data)
    mapper = Mapper.get_raw(mid)
    assert isinstance(mapper, Mapper.prototype)
    m_fn = Mapper.activate(mapper)
    assert m_fn(1) == 2


def test_reducer():
    data = {
        'name': 'test_reducer',
        'body': 'lambda x, y: x + y',
    }
    mid = Reducer.create(**data)
    reducer = Reducer.get_raw(mid)
    assert isinstance(reducer, Reducer.prototype)
    m_fn = Reducer.activate(reducer)
    assert m_fn(1, 2) == 3


def test_spout():
    code = '1'
    data = {
        'name': 'test_spout',
        'body': code,
        'closure': {},
        'rate': 1
    }
    Spout.create(**data)


def test_qubit():
    data = {
        'name': 'test_qubit',
        'entangle': 'Spout:tester',
        'mappers': [1],
        'reducer': 1,
        'closure': {},
        'flying': True
    }
    Qubit.create(**data)
