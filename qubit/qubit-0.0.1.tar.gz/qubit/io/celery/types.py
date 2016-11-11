import celery
from typing import NamedTuple

PeriodTask = NamedTuple('PeriodTask', [
    ('period', float),
    ('task', celery.Task),
    ('name', str)
])
