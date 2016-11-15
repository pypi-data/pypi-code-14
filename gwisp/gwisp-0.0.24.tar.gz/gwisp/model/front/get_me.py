import copy

from ..lowest import account


res_body = copy.deepcopy(account.storage)
res_body['required'].remove('scheduler')
res_body['properties'].pop('scheduler')

res = {'body': res_body}
