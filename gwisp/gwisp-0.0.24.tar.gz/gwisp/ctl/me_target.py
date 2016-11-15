from falcon import HTTPNotFound, HTTPInternalServerError, HTTPBadRequest, \
                   HTTP_204
from bson import ObjectId

from ..repo import SchedulerRepo, CSchedulerRepo


class MeTargetCtl(object):
    def __init__(self, db, protector):
        self._sched_repo = SchedulerRepo(db)
        self._protector = protector

    def on_get(self, req, res):
        auth = self._protector.check(req, iacc=True)

        if 'scheduler' not in auth.account:
            raise HTTPNotFound(description='Not found target scheduler')

        if 'scheduler' not in auth.account:
            raise HTTPNotFound(description='No scheduler is using')
        target = auth.account['scheduler']

        real_item = self._sched_repo.find_by_id(target['_id'])
        if real_item is None:
            raise HTTPInternalServerError(
                description='Not found scheduler'
            )

        if real_item['modified'] > target['_cloned_date']:
            target['_updated'] = False
        else:
            target['_updated'] = True

        # remove data
        del target['_cloned_date']

        res.body = target


class MeTargetItemCtl(object):
    def __init__(self, db, protector):
        self._protector = protector
        self._csched_repo = CSchedulerRepo(db)

    def on_put(self, req, res, id):
        auth = self._protector.check(req)

        try:
            sched_id = ObjectId(id)
        except Exception as e:
            raise HTTPBadRequest(
                title='400 Bad Request',
                description='Identity is invalid'
            )

        self._csched_repo.use_scheduler(auth.account_id, sched_id)

        res.status = HTTP_204
