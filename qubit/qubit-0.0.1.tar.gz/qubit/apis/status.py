import datetime
from qubit.types import Status, Qubit
from qubit.core import app
from .utils import resp_wrapper as wrapper
from .utils import jsonize


__all__ = ['status_api']


@app.route('/qubit/<qid>/from/<start>/to/<end>/', methods=['GET'])
@jsonize
@wrapper
def status_api(qid, start, end):
    def format(v):
        if isinstance(v, datetime.datetime):
            return str(v)
        return v

    def strize(d: dict):
        return {k: format(v) for k, v in d._asdict().items()}
    status = Qubit.get(qid)
    data = Status.select(status.id, start, end)
    return [strize(d) for d in data]
