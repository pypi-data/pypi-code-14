import copy

from .get_scheduler import res_body as get_sched_res_body
from ..repo import cscheduler as rmodel_csched


res_body = copy.deepcopy(get_sched_res_body)
res_body['items']['required'].extend(['_cloned', '_updated'])
res_body['items']['properties'].update({
    '_cloned': rmodel_csched.attr_cloned,
    '_updated': rmodel_csched.attr_updated
})
res = {'body': res_body}
