# Quark 1.0.452 run at 2016-10-14 13:41:15.961212
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import str as unicode

from quark_runtime import *
_lazyImport.plug("mdk_runtime.promise")
import quark_runtime
import quark_threaded_runtime
import quark_runtime_logging
import quark_ws4py_fixup
import mdk_runtime_files
import quark.reflect
import quark.error
import quark
import mdk_runtime.actors



def _fullfilPromise(promise, value):
    """
    Resolve a Promise with a result.
    """
    if ((quark.reflect.Class.ERROR).hasInstance(value)):
        (promise)._reject(_cast(value, lambda: quark.error.Error));
    else:
        (promise)._resolve(value);


class _ChainPromise(_QObject):
    def _init(self):
        self._next = None

    def __init__(self, next):
        self._init()
        (self)._next = next

    def call(self, arg):
        _fullfilPromise((self)._next, arg);
        return None

    def _getClass(self):
        return u"mdk_runtime.promise._ChainPromise"

    def _getField(self, name):
        if ((name) == (u"_next")):
            return (self)._next

        return None

    def _setField(self, name, value):
        if ((name) == (u"_next")):
            (self)._next = _cast(value, lambda: Promise)


_ChainPromise.mdk_runtime_promise__ChainPromise_ref = None
class _CallbackEvent(_QObject):
    def _init(self):
        self._callable = None
        self._next = None
        self._value = None

    def __init__(self, callable, next, value):
        self._init()
        (self)._callable = callable
        (self)._next = next
        (self)._value = value

    def deliver(self):
        result = ((self)._callable)((self)._value) if callable((self)._callable) else ((self)._callable).call((self)._value);
        if ((quark.reflect.Class.get(u"mdk_runtime.promise.Promise")).hasInstance(result)):
            toChain = _cast(result, lambda: Promise);
            (toChain).andFinally(_ChainPromise((self)._next));
        else:
            _fullfilPromise((self)._next, result);

    def _getClass(self):
        return u"mdk_runtime.promise._CallbackEvent"

    def _getField(self, name):
        if ((name) == (u"_callable")):
            return (self)._callable

        if ((name) == (u"_next")):
            return (self)._next

        if ((name) == (u"_value")):
            return (self)._value

        return None

    def _setField(self, name, value):
        if ((name) == (u"_callable")):
            (self)._callable = _cast(value, lambda: quark.UnaryCallable)

        if ((name) == (u"_next")):
            (self)._next = _cast(value, lambda: Promise)

        if ((name) == (u"_value")):
            (self)._value = value


_CallbackEvent.mdk_runtime_promise__CallbackEvent_ref = None
class _Callback(_QObject):
    def _init(self):
        self._callable = None
        self._next = None

    def __init__(self, callable, next):
        self._init()
        (self)._callable = callable
        (self)._next = next

    def call(self, result):
        event = _CallbackEvent((self)._callable, (self)._next, result);
        ((self._next)._dispatcher)._queue(event);

    def _getClass(self):
        return u"mdk_runtime.promise._Callback"

    def _getField(self, name):
        if ((name) == (u"_callable")):
            return (self)._callable

        if ((name) == (u"_next")):
            return (self)._next

        return None

    def _setField(self, name, value):
        if ((name) == (u"_callable")):
            (self)._callable = _cast(value, lambda: quark.UnaryCallable)

        if ((name) == (u"_next")):
            (self)._next = _cast(value, lambda: Promise)


_Callback.mdk_runtime_promise__Callback_ref = None
class _Passthrough(_QObject):
    def _init(self):
        pass
    def __init__(self): self._init()

    def call(self, arg):
        return arg

    def _getClass(self):
        return u"mdk_runtime.promise._Passthrough"

    def _getField(self, name):
        return None

    def _setField(self, name, value):
        pass
_Passthrough.mdk_runtime_promise__Passthrough_ref = None
class _CallIfIsInstance(_QObject):
    def _init(self):
        self._underlying = None
        self._class = None

    def __init__(self, underlying, klass):
        self._init()
        (self)._underlying = underlying
        (self)._class = klass

    def call(self, arg):
        if (((self)._class).hasInstance(arg)):
            return ((self)._underlying)(arg) if callable((self)._underlying) else ((self)._underlying).call(arg)
        else:
            return arg

    def _getClass(self):
        return u"mdk_runtime.promise._CallIfIsInstance"

    def _getField(self, name):
        if ((name) == (u"_underlying")):
            return (self)._underlying

        if ((name) == (u"_class")):
            return (self)._class

        return None

    def _setField(self, name, value):
        if ((name) == (u"_underlying")):
            (self)._underlying = _cast(value, lambda: quark.UnaryCallable)

        if ((name) == (u"_class")):
            (self)._class = _cast(value, lambda: quark.reflect.Class)


_CallIfIsInstance.mdk_runtime_promise__CallIfIsInstance_ref = None
class PromiseValue(_QObject):
    """
    Snapshot of the value of a Promise, if it has one.
    """
    def _init(self):
        self._successResult = None
        self._failureResult = None
        self._hasValue = None

    def __init__(self, successResult, failureResult, hasValue):
        self._init()
        (self)._successResult = successResult
        (self)._failureResult = failureResult
        (self)._hasValue = hasValue

    def hasValue(self):
        """
        Return true if the Promise had a value at the time this was created.
        """
        return (self)._hasValue

    def isError(self):
        """
        Return true if value is error. Result is only valid if hasValue() is true.
        """
        return ((self)._failureResult) != (None)

    def getValue(self):
        """
        Return the value. Result is only valid if hasValue() is true.
        """
        if ((self).isError()):
            return (self)._failureResult
        else:
            return (self)._successResult

    def _getClass(self):
        return u"mdk_runtime.promise.PromiseValue"

    def _getField(self, name):
        if ((name) == (u"_successResult")):
            return (self)._successResult

        if ((name) == (u"_failureResult")):
            return (self)._failureResult

        if ((name) == (u"_hasValue")):
            return (self)._hasValue

        return None

    def _setField(self, name, value):
        if ((name) == (u"_successResult")):
            (self)._successResult = value

        if ((name) == (u"_failureResult")):
            (self)._failureResult = _cast(value, lambda: quark.error.Error)

        if ((name) == (u"_hasValue")):
            (self)._hasValue = _cast(value, lambda: bool)


PromiseValue.mdk_runtime_promise_PromiseValue_ref = None
class Promise(_QObject):
    """
    An object that will eventually have a result.
    Results are passed to callables whose return value is passed
    to resulting Promise. If a return result is a Promise it will
    be chained automatically, i.e. callables will never be called
    with a Promise, only with values.
    """
    def _init(self):
        self._lock = None
        self._successResult = None
        self._failureResult = None
        self._hasResult = None
        self._successCallbacks = None
        self._failureCallbacks = None
        self._dispatcher = None

    def __init__(self, dispatcher):
        self._init()
        (self)._dispatcher = dispatcher
        (self)._lock = _Lock()
        (self)._hasResult = False
        (self)._successResult = None
        (self)._failureResult = _cast(None, lambda: quark.error.Error)
        (self)._successCallbacks = _List([])
        (self)._failureCallbacks = _List([])

    def _maybeRunCallbacks(self):
        ((self)._lock).acquire();
        if (not ((self)._hasResult)):
            ((self)._lock).release();
            return

        callbacks = (self)._successCallbacks;
        value = (self)._successResult;
        if (((self)._failureResult) != (None)):
            callbacks = (self)._failureCallbacks
            value = (self)._failureResult

        (self)._failureCallbacks = _List([])
        (self)._successCallbacks = _List([])
        ((self)._lock).release();
        idx = 0;
        while ((idx) < (len(callbacks))):
            ((callbacks)[idx]).call(value);
            idx = (idx) + (1)

    def _resolve(self, result):
        if ((quark.reflect.Class.ERROR).hasInstance(result)):
            (self)._reject(_cast(result, lambda: quark.error.Error));
            return

        ((self)._lock).acquire();
        if ((self)._hasResult):
            _println(u"BUG: Resolved Promise that already has a value.");
            ((self)._lock).release();
            return

        (self)._hasResult = True
        (self)._successResult = result
        ((self)._lock).release();
        (self)._maybeRunCallbacks();

    def _reject(self, err):
        ((self)._lock).acquire();
        if ((self)._hasResult):
            _println(u"BUG: Rejected Promise that already has a value.");
            ((self)._lock).release();
            return

        (self)._hasResult = True
        (self)._failureResult = err
        ((self)._lock).release();
        (self)._maybeRunCallbacks();

    def andThen(self, callable):
        """
        Add callback that will be called on non-Error values.
        Its result will become the value of the returned Promise.
        """
        return self.andEither(callable, _Passthrough())

    def andCatch(self, errorClass, callable):
        """
        Add callback that will be called on Error values.
        Its result will become the value of the returned Promise.
        """
        return self.andEither(_Passthrough(), _CallIfIsInstance(callable, errorClass))

    def andFinally(self, callable):
        """
        Callback that will be called for both success and error results.
        """
        return self.andEither(callable, callable)

    def andEither(self, success, failure):
        """
        Two callbacks, one for success and one for error results.
        """
        result = Promise((self)._dispatcher);
        ((self)._lock).acquire();
        ((self)._successCallbacks).append(_Callback(success, result));
        ((self)._failureCallbacks).append(_Callback(failure, result));
        ((self)._lock).release();
        (self)._maybeRunCallbacks();
        return result

    def value(self):
        """
        Synchronous extraction of the promise's current value, if it has any.
        Its result will become the value of the returned Promise.
        """
        ((self)._lock).acquire();
        result = PromiseValue((self)._successResult, (self)._failureResult, (self)._hasResult);
        ((self)._lock).release();
        return result

    def _getClass(self):
        return u"mdk_runtime.promise.Promise"

    def _getField(self, name):
        if ((name) == (u"_lock")):
            return (self)._lock

        if ((name) == (u"_successResult")):
            return (self)._successResult

        if ((name) == (u"_failureResult")):
            return (self)._failureResult

        if ((name) == (u"_hasResult")):
            return (self)._hasResult

        if ((name) == (u"_successCallbacks")):
            return (self)._successCallbacks

        if ((name) == (u"_failureCallbacks")):
            return (self)._failureCallbacks

        if ((name) == (u"_dispatcher")):
            return (self)._dispatcher

        return None

    def _setField(self, name, value):
        if ((name) == (u"_lock")):
            (self)._lock = _cast(value, lambda: _Lock)

        if ((name) == (u"_successResult")):
            (self)._successResult = value

        if ((name) == (u"_failureResult")):
            (self)._failureResult = _cast(value, lambda: quark.error.Error)

        if ((name) == (u"_hasResult")):
            (self)._hasResult = _cast(value, lambda: bool)

        if ((name) == (u"_successCallbacks")):
            (self)._successCallbacks = _cast(value, lambda: _List)

        if ((name) == (u"_failureCallbacks")):
            (self)._failureCallbacks = _cast(value, lambda: _List)

        if ((name) == (u"_dispatcher")):
            (self)._dispatcher = _cast(value, lambda: mdk_runtime.actors.MessageDispatcher)


Promise.quark_List_mdk_runtime_promise__Callback__ref = None
Promise.mdk_runtime_promise_Promise_ref = None
class PromiseResolver(_QObject):
    """
    Create Promises and input their initial value.

    """
    def _init(self):
        self.promise = None

    def __init__(self, dispatcher):
        self._init()
        (self).promise = Promise(dispatcher)

    def resolve(self, result):
        """
        Set the attached Promise's initial value.
        """
        ((self).promise)._resolve(result);

    def reject(self, err):
        """
        Set the attached Promise's initial value to an Error.
        """
        ((self).promise)._reject(err);

    def _getClass(self):
        return u"mdk_runtime.promise.PromiseResolver"

    def _getField(self, name):
        if ((name) == (u"promise")):
            return (self).promise

        return None

    def _setField(self, name, value):
        if ((name) == (u"promise")):
            (self).promise = _cast(value, lambda: Promise)


PromiseResolver.mdk_runtime_promise_PromiseResolver_ref = None

def _lazy_import_datawire_mdk_md():
    import datawire_mdk_md
    globals().update(locals())
_lazyImport("import datawire_mdk_md", _lazy_import_datawire_mdk_md)



_lazyImport.pump("mdk_runtime.promise")
