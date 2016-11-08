import nicecall


class ProcessStub(nicecall.Process):
    def __init__(
            self, on_stdout=None, on_stderr=None, filters=None,
            raise_if_error=False, matches=None):
        self._matches = matches or {}
        super().__init__(on_stdout, on_stderr, filters, raise_if_error)

    def add_match(self, args, exitcode, stdout=[], stderr=[]):
        key = self._generate_key(args)
        self._matches[key] = (exitcode, stdout, stderr)

    def execute(self, args=None):
        key = self._generate_key(args)
        exitcode, stdout, stderr = self._matches[key]

        for line in stdout:
            for action in self._on_stdout:
                action(line)

        for line in stderr:
            for action in self._on_stderr:
                action(line)

        return exitcode

    def _generate_key(self, args):
        parts = [a.replace("\\", "\\\\").replace(",", "\\,") for a in args]
        return ",".join(parts)

    def _clone(self):
        return self.__class__(
            self._on_stdout, self._on_stderr, self._filters,
            self._raise_if_error, self._matches)
