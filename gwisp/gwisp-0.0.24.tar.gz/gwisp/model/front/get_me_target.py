import copy

from ..lowest import scheduler as lmodel_sched
from ..repo import cscheduler as rmodel_csched


res_body = copy.deepcopy(lmodel_sched.storage)
res_body['required'].extend(['_updated'])
res_body['properties'].update({
    '_updated': rmodel_csched.attr_updated
})
res = {'body': res_body}
