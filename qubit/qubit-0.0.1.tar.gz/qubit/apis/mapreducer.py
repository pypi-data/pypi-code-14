from qubit.types import Mapper, Reducer
from flask import request
from qubit.core import app
from .utils import resp_wrapper as wrapper
from .utils import jsonize

__all__ = ['mapper', 'reducer']


@app.route('/qubit/mapper/<id>/', methods=['GET', 'DELETE'])
@app.route('/qubit/mapper/', methods=['POST'])
@jsonize
@wrapper
def mapper(id=None):
    def create():
        return dict(id=Mapper.create(**request.json))

    def fetch():
        return Mapper.get_raw(id=id)._asdict()

    def update():
        pass

    return {
        'GET': fetch,
        'POST': create
    }.get(request.method)()


@app.route('/qubit/reducer/<id>/', methods=['GET', 'DELETE'])
@app.route('/qubit/reducer/', methods=['POST'])
@jsonize
@wrapper
def reducer(id=None):
    def create():
        return dict(id=Reducer.create(**request.json))

    def fetch():
        return Reducer.get_raw(id=id)._asdict()

    def update():
        pass

    return {
        'GET': fetch,
        'POST': create
    }.get(request.method)()
