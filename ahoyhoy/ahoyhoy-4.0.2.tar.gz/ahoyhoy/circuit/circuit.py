"""
StateMachine pattern
http://python-3-patterns-idioms-test.readthedocs.io/en/latest/StateMachine.html
"""

from ..classifiers import raise_for_status


class CircuitClassifier(object):

    def __init__(self):
        self._state = None
        self._host = None
        self._pre = None
        self._post = None
        self._retry = None
        self._exc = None
        self._client = None

    def classify(self, func, *args, **kwargs):
        return self._state.classify(self, func, *args, **kwargs)

    def dispatch(self, name):
        return self._state.dispatch(self, name)


class Circuit(CircuitClassifier):
    """
    Simple base class to handle the transition between
    closed and open circuit states.
    """

    def __init__(self):
        super(Circuit, self).__init__()
        self._state = ClosedState

    def change_state(self, state):
        self._state = state

    def open(self):
        return self._state.open(self)

    def close(self):
        return self._state.close(self)

    def is_open(self):
        return self._state == OpenState

    def is_closed(self):
        return self._state == ClosedState

    @property
    def available(self):
        return self.is_closed()


class StateClassifier(object):
    
    @staticmethod
    def classify(circuit, func, *args, **kwargs):
        """
        Look at the result, and determine what to do, either with the response
        or any exceptions raised along the way.
        """
        try:
            if circuit._retry is None:
                result = func(*args, **kwargs)
            else:
                result = circuit._retry(func, fargs=args, fkwargs=kwargs)
        except Exception as e:
            # Eventually, we'll want to catch separate exceptions
            # and handle the reactions differently
            circuit.open()
            if circuit._exc is None:
                raise e

            return circuit._exc(e)
        else:
            return raise_for_status(result)

    @staticmethod
    def dispatch(circuit, name):
        """
        Return requested function so it can be then
        called in `classify` method and proccessed respectively.
        """
        return getattr(circuit._session, name)


class State(StateClassifier):

    @staticmethod
    def open(circuit):
        circuit.change_state(OpenState)

    @staticmethod
    def close(circuit):
        circuit.change_state(ClosedState)


class ClosedState(State):
    """
    Circuit in a closed state. Closing will throw RuntimeError.
    """
    @staticmethod
    def close(circuit):
        raise RuntimeError("State is already closed.")


class OpenState(State):
    """
    Circut in an open state. Opening as well as all other methods will throw RuntimeError.
    """
    @staticmethod
    def open(circuit):
        raise RuntimeError("State is already open.")

    @staticmethod
    def dispatch(circuit, name):
        raise RuntimeError("Circuit state is open, no connections possible.")

    @staticmethod
    def classify(circuit, func, *args, **kwargs):
        raise RuntimeError("Circuit state is open, dispatch should have \
                            already caught this, but no connections possible.")