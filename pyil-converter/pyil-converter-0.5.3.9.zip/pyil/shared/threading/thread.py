import os as _os
import dill as _dill

from .__launcher import Launcher as _la


class IsoThread:
    threads = []

    @classmethod
    def join(cls):
        """Equal to Thread.join"""
        from timeit import default_timer
        temp=default_timer()
        for i in cls.threads:
            i.wait()
        return temp-default_timer()

    def __init__(self, target, args: tuple = None, kwargs: dict = None, required_module: list = None):
        """This is true threading. The reason why it is called
        "IsoThread" is that the thread it creates is completely
        separated from the main thread. Therefore it cannot
        print or do modify the variable in the main thread. This
        is used for background process, which needs to be
        separated from the main thread and run quietly."""
        from .._coll import random_word
        self.src_name = 'src' + random_word(5, word_only=True) + ".func"
        self.run = target
        self.args = args
        self.kwargs = kwargs
        self.mds = required_module
        IsoThread.threads.append(self)

    def _prepare(self):
        _dill.dump(self.run, open(self.src_name, 'wb'))
        return _la(self.src_name, args=self.args, kwargs=self.kwargs, required=self.mds)

    def start(self):
        """Start the thread(process)."""
        self._pcs = self._prepare()
        self._pcs.prepare()
        self._pcs.start()

    def wait(self):
        """Wait and return the exit code."""
        return self._pcs.wait()

    @property
    def finished(self):
        """Finished or not."""
        return self._pcs.finished

    @property
    def result(self):
        """Result, will raise ProcessError if not
        finished yet or some exception occurred."""
        import pyil.shared._coll
        try:

            return self._pcs.result
        except pyil.shared._coll.ProcessError:
            self.clean()
            raise

    def terminate(self) -> 0:
        """terminate the thread."""
        self._pcs.end()
        return 0

    def clean(self) -> int:
        """Clean up the file being created."""
        self._pcs.clean()
        try:
            _os.unlink(self.src_name)
        except FileNotFoundError:
            return 1
        return 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clean()
