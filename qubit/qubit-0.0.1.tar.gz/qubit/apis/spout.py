from qubit.types import Spout
from qubit.core import app
from flask import request
from .utils import resp_wrapper as wrapper
from .utils import jsonize

__all__ = ['spout_api']


@app.route('/qubit/spout/<name>/', methods=['GET', 'UPDATE', 'PUT'])
@app.route('/qubit/spout/', methods=['POST'])
@jsonize
@wrapper
def spout_api(name=None):
    def create():
        return Spout.create(**request.json)

    def push():
        spout = Spout.get_via_name(name=name)
        data = Spout.data(**request.json)
        Spout.measure(spout, data)

    def fetch():
        return Spout.get_via_name(name=name)._asdict()

    def update():
        pass

    return {
        'GET': fetch,
        'PUT': push,
        'POST': create
    }.get(request.method)()
