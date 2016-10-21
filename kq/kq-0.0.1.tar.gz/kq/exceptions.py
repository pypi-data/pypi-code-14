from __future__ import absolute_import, print_function, unicode_literals


class WorkerInitError(Exception):
    """Raised when there is an issue with a KQ worker."""


class QueueInitError(Exception):
    """Raised when there is an issue with a KQ queue."""


class JobEnqueueError(Exception):
    """Raised when there is an issue with enqueuing a KQ job."""


class JobDecoratorError(Exception):
    """Raised when there is an issue with the job decorator."""
