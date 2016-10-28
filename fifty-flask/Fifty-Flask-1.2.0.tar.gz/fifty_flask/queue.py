from __future__ import absolute_import
from flask import current_app
from flask_rq import job


def smart_job(func_or_queue=None, should_noop=False, **smart_job_kwargs):
    noop = lambda: should_noop() if callable(should_noop) else should_noop

    def inner(fn):
        wrapper = job(func_or_queue)
        if not callable(func_or_queue):
            wrapper = wrapper(fn)

        # We're going to replace this with a new function, but internally call the original one.
        real_delay = wrapper.delay

        def delay(*args, **kwargs):
            # Decide if we should run this job at all
            if noop():
                return

            # We need these later on for RQ, but they shouldn't be passed to the function that's
            # being delayed when we're doing a synchronous call
            rq_kwargs = kwargs.pop('rq_kwargs', {})

            # Bypass RQ when appropriate
            if current_app.config.get('RQ_SYNC_SMART_JOB', current_app.debug or current_app.testing):
                return fn(*args, **kwargs)

            # Smart job kwargs first
            # Updated with the fn kwargs
            # Updated with rq_kwargs
            delay_kwargs = {}
            delay_kwargs.update(smart_job_kwargs)
            delay_kwargs.update(kwargs)
            delay_kwargs.update(rq_kwargs)

            return real_delay(*args, **delay_kwargs)

        wrapper.delay = delay

        return wrapper

    # No decorator arguments (use the default behavior)
    if callable(func_or_queue):
        return inner(func_or_queue)

    return inner
