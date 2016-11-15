import copy

from .ess import account_id
from .scheduler import storage as sched_storage

#: Account identity who is used scheduler
attr_cloner = account_id

#: Cloned date
attr_cloned_date = {
    'type': 'integer'
}

#: Model store in database
storage = copy.deepcopy(sched_storage)
storage['required'].extend(['_cloner', '_cloned_date'])
storage['properties'].update({
    '_cloner': attr_cloner,
    '_cloned_date': attr_cloned_date
})
