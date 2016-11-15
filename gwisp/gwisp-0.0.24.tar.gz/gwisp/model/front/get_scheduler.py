import copy

from ..repo import scheduler as rmodel_sched


res_body = copy.deepcopy(rmodel_sched.search)

res = {'body': res_body}
