import copy

from .get_scheduler_id import res_body as get_sched_res_body
from ..repo import cscheduler as rmodel_sched


res_body = copy.deepcopy(get_sched_res_body)
res_body['required'].extend(['_cloned', '_updated'])
res_body['properties'].update({
    '_cloned': rmodel_sched.attr_cloned,
    '_updated': rmodel_sched.attr_updated
})
res = {'body': res_body}
