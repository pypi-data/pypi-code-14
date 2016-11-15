import copy

from .get_scheduler import res_body as get_sched_res_body


res_body = copy.deepcopy(get_sched_res_body)
res_body['items']['required'].remove('author')
res_body['items']['properties'].pop('author')
res = {'body': res_body}
