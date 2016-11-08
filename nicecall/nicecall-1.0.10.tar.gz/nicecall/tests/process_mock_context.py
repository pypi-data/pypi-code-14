import nicecall


class ProcessMockContext():
    def __init__(self, wrapped=None):
        self._wrapped = wrapped

    def __enter__(self):
        self._executed_args = []
        self._ignore_predicates = []
        self._keep_predicates = []
        self._on_stdout_actions = []
        self._on_stderr_actions = []
        return self

    def __exit__(self, type, value, tb):
        pass

    @property
    def mock(self):
        return ProcessMock(context=self, wrapped=self._wrapped)

    @property
    def executed_args(self):
        return self._executed_args

    @property
    def ignore_predicates(self):
        return self._ignore_predicates

    @property
    def keep_predicates(self):
        return self._keep_predicates

    @property
    def on_stdout_actions(self):
        return self._on_stdout_actions

    @property
    def on_stderr_actions(self):
        return self._on_stderr_actions


class ProcessMock(nicecall.Process):
    def __init__(self, context=None, wrapped=None):
        self._context = context
        self._wrapped = wrapped or nicecall.tests.NullProcess()

    def execute(self, args=None):
        self._context._executed_args.append(args)
        return self._wrapped.execute(args)

    def ignore(self, predicate):
        result = self._clone(self._wrapped.ignore(predicate))
        result._context._ignore_predicates.append(predicate)
        return result

    def keep(self, predicate):
        result = self._clone(self._wrapped.keep(predicate))
        result._context._keep_predicates.append(predicate)
        return result

    def on_stdout(self, action):
        result = self._clone(self._wrapped.on_stdout(action))
        result._context._on_stdout_actions.append(action)
        return result

    def on_stderr(self, action):
        result = self._clone(self._wrapped.on_stderr(action))
        result._context._on_stderr_actions.append(action)
        return result

    def _clone(self, wrapped):
        return ProcessMock(context=self._context, wrapped=self._wrapped)
