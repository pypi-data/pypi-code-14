import json
import datetime
import time
from tests.apis import request
from tests.apis import get


def create_qubit(entangle, name='a qubit'):
    qubit_data = {
        'name': name,
        'entangle': entangle,
    }
    res = json.loads(request(path='/qubit/', data=json.dumps(qubit_data), method='POST'))
    assert res['result'] == 'ok'
    qid = res['id']
    return qid


def entangle(q1, q2):
    res = json.loads(request(path='/qubit/entangle/%s/' % q1, data=json.dumps({
        'id': q2
    }), method='POST'))
    assert res['result'] == 'ok'
    return res


def get_hours_data(qid):
    end = datetime.datetime.now()
    delta = datetime.timedelta(hours=1)
    start = end - delta
    res = json.loads(get(path='/qubit/%s/from/%s/to/%s/' % (
        qid, str(start), str(end))))
    return res['data']


def feed_random_data(spout='tester'):
    data = {
        'datum': {
            'a': time.time()
        },
        'ts': str(datetime.datetime.now())
    }
    res = json.loads(request(path='/qubit/spout/%s/' % spout,
                             data=json.dumps(data), method='PUT'))
    assert res['result'] == 'ok'


def create_mapper(name='new mapper'):
    data = {
        'name': name,
        'body': 'lambda x: dict(x, added=True)',
        'closure': {
            'a': 1
        }
    }
    resp = request(path='/qubit/mapper/',
                   data=json.dumps(data), method='POST')
    print(resp)
    res = json.loads(resp)
    assert res['result'] == 'ok'
    return res['id']


def add_mapper(mid, qid):
    resp = request(path='/qubit/%s/mapper/%s/' % (qid, mid), method='PUT')
    res = json.loads(resp)
    assert res['result'] == 'ok'


def add_reducer(rid, qid):
    resp = request(path='/qubit/%s/reducer/%s/' % (qid, rid), method='PUT')
    res = json.loads(resp)
    assert res['result'] == 'ok'
    return res['id']


def create_reducer():
    data = {
        'name': 'test_qubit',
        'entangle': 'Spout:tester',
        'mappers': [1],
        'reducer': 1,
        'closure': {},
        'flying': True
    }
    res = json.loads(request(path='/qubit/reducer/',
                             data=json.dumps(data), method='POST'))
    assert res['result'] == 'ok'
    return res['id']


def test_crud():
    code = '1'
    data = {
        'name': 'tester',
        'body': code,
        'closure': {},
        'rate': 1
    }
    res = json.loads(request(path='/qubit/spout/',
                             data=json.dumps(data), method='POST'))
    assert res['result'] == 'ok'
    res = json.loads(get('/qubit/spout/tester/'))
    assert res['result'] == 'ok'
    qid = create_qubit('Spout:tester')

    feed_random_data()
    feed_random_data()
    feed_random_data()

    assert len(get_hours_data(qid)) == 3
    qid2 = create_qubit('none', 'another')
    entangle(qid2, qid)

    feed_random_data()
    feed_random_data()
    feed_random_data()
    assert len(get_hours_data(qid2)) == 3
    assert len(get_hours_data(qid)) == 6
    mid = create_mapper()
    add_mapper(mid, qid2)
    feed_random_data()
    feed_random_data()
    feed_random_data()
    res1 = get_hours_data(qid2)
    res2 = get_hours_data(qid)
    assert len(res1) == 6
    assert len(res2) == 9
    assert 'added' in res1[-1]['datum'].keys()
