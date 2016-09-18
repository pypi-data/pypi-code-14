from importlib import import_module
from django.conf import settings

def experiment_access(request):
    ctx = {}
    experiments = settings.__dict__.keys()
    for experiment in experiments:
        if not experiment.startswith('AB_'):
            continue
        ctx[experiment] = getattr(settings, experiment, False)
    return ctx
