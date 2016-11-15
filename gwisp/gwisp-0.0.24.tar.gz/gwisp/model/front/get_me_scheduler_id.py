import copy


from ..lowest import scheduler
from ..repo import cscheduler as rmodel_sched


res_body = copy.deepcopy(scheduler.storage)
res_body['required'].extend(['_updated'])
res_body['properties'].update({
    '_updated': rmodel_sched.attr_updated
})
res = {'body': res_body}
