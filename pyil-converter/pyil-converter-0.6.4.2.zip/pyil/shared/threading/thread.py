import os as _os
import dill as _dill
from .__launcher import Launcher as _la


class IsoThread:
    threads = []

    @classmethod
    def join(cls):
        """Equal to Thread.join"""
        from timeit import default_timer
        temp = default_timer()
        for i in cls.threads:
            i.wait()
        return temp - default_timer()

    def __init__(self, target, name='Thread No.'+str(len(threads)), args: tuple = None,
                 kwargs: dict = None, required_module: list = None):
        """This is true threading. The reason why it is called
        "IsoThread" is that the thread it creates is completely
        separated from the main thread. Therefore it cannot
        print or do modify the variable in the main thread. This
        is used for background process, which needs to be
        separated from the main thread and run quietly."""
        from .._coll import random_word
        self.name = name
        self.src_name = 'src_' + name + ".func"
        self.run = target
        self.args = args
        self.kwargs = kwargs
        self.mds = required_module
        self.status = 'waiting'
        IsoThread.threads.append(self)

    def _prepare(self):
        _dill.dump(self.run, open(self.src_name, 'wb'))
        self.status = 'starting'
        return _la(self.src_name, name=self.name, args=self.args, kwargs=self.kwargs, required=self.mds)

    def start(self):
        """Start the thread(process)."""
        self._pcs = self._prepare()
        self._pcs.prepare()
        self._pcs.start()
        self.status = 'running'

    def wait(self):
        """Wait and return the exit code."""
        return self._pcs.wait()

    @property
    def finished(self):
        """Finished or not."""
        if self._pcs.finished:
            self.status = 'finished'
            return True
        return False

    @property
    def result(self):
        """Result, will raise ProcessError if not
        finished yet or some exception occurred."""
        import pyil.shared._coll
        try:
            temp = self._pcs.result
            self.status = 'finished'
            return temp
        except pyil.shared._coll.ProcessError:
            self.clean()
            self.status = 'paused'
            raise

    def terminate(self) -> 0:
        """terminate the thread."""
        self._pcs.end()
        self.status = 'ended'
        return 0

    def clean(self) -> int:
        """Clean up the file being created."""
        self._pcs.clean()
        try:
            _os.unlink(self.src_name)
        except FileNotFoundError:
            self.status = 'cleaned'
            return 1
        self.status = 'cleaned'
        return 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clean()

    def __str__(self):
        return self.name + ": " + self.status
