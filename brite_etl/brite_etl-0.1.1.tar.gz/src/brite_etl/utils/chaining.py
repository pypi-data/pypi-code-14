"""Method chaining interface.

Taken from pydash - https://github.com/dgilland/pydash/blob/8b6f2687e2e61d27dc5ffd53e7021a766f19cf91/pydash/chaining.py
"""
# flake8: noqa
from __future__ import absolute_import, print_function

import brite_etl as btl
from brite_etl import NoValue


class Chain(object):
    """Enables chaining of :attr:`module` functions."""

    #: Object that contains attribute references to available methods.
    module = btl

    def __init__(self, value=NoValue):
        self._value = value

    def value(self):
        """Return current value of the chain operations.

        Returns:
            mixed: Current value of chain operations.

        See Also:
            - :meth:`value` (main definition)
            - :meth:`value_of` (alias)
        """
        return self(self._value)

    value_of = value
    run = value

    # def to_string(self):
    #     """Return current value as string.

    #     Returns:
    #         str: Current value of chain operations casted to ``str``.
    #     """
    #     return self.module.to_string(self.value())

    def commit(self):
        """Executes the chained sequence and returns the wrapped result.

        Returns:
            Chain: New instance of :class:`Chain` with resolved value from
                previous :class:`Class`.
        """
        return Chain(self.value())

    def plant(self, value):
        """Return a clone of the chained sequence planting `value` as the
        wrapped value.

        Args:
            value (mixed): Value to plant as the initial chain value.
        """
        # pylint: disable=no-member,maybe-no-member
        wrapper = self._value
        wrappers = []

        if hasattr(wrapper, '_value'):
            wrappers = [wrapper]

            while isinstance(wrapper._value, ChainWrapper):
                wrapper = wrapper._value
                wrappers.insert(0, wrapper)

        clone = Chain(value)

        for wrap in wrappers:
            clone = ChainWrapper(clone._value, wrap.method)(*wrap.args,
                                                            **wrap.kargs)

        return clone

    @classmethod
    def get_method(cls, name):
        """Return valid :attr:`module` method.

        Args:
            name (str): Name of pydash method to get.

        Returns:
            function: :attr:`module` callable.

        Raises:
            InvalidMethod: Raised if `name` is not a valid :attr:`module`
                method.
        """
        # Python 3.5 issue with pytest doctest call where inspect module tries
        # to unwrap this class. If we don't return here, we get an
        # InvalidMethod exception.
        if name in ('__wrapped__',):  # pragma: no cover
            return cls



        # Here we're loopling through each submodule in brite_etl.core to
        # try and find a method match. When found, we'll use it.
        method = None
        _all = getattr(cls.module.core, '__all__', None)
        _all_count = 0
        while (method is None) and (_all_count < len(_all)):
            _sub = getattr(cls.module.core, _all[_all_count], None)
            method = getattr(_sub, name, None)
            _all_count += 1


        # if method is None:
        #     print('vat')
        #     print(name)
        #     print(method)
        #     exit()

        # method = getattr(cls.module.utils, name, None)

        # if not callable(method) and not name.endswith('_'):
        #     # Alias method names not ending in underscore to their underscore
        #     # counterpart. This allows chaining of functions like "map_()"
        #     # using "map()" instead.
        #     method = getattr(cls.module.utils, name + '_', None)


        if not callable(method):
            raise Exception('Invalid btl method: {0}'.format(name))

        return method

    def __getattr__(self, attr):
        """Proxy attribute access to :attr:`module`.

        Args:
            attr (str): Name of :attr:`module` function to chain.

        Returns:
            ChainWrapper: New instance of :class:`ChainWrapper` with value
                passed on.

        Raises:
            InvalidMethod: Raised if `attr` is not a valid function.
        """
        return ChainWrapper(self._value, self.get_method(attr))

    def __call__(self, value):
        """Return result of passing `value` through chained methods.

        Args:
            value (mixed): Initial value to pass through chained methods.

        Returns:
            mixed: Result of method chain evaluation of `value`.
        """
        if isinstance(self._value, ChainWrapper):
            # pylint: disable=maybe-no-member
            value = self._value.unwrap(value)
        return value


class ChainWrapper(object):
    """Wrap :class:`Chain` method call within a :class:`ChainWrapper` context.
    """
    def __init__(self, value, method):
        self._value = value
        self.method = method
        self.args = ()
        self.kargs = {}

    def _generate(self):
        """Generate a copy of this instance."""
        # pylint: disable=attribute-defined-outside-init
        new = self.__class__.__new__(self.__class__)
        new.__dict__ = self.__dict__.copy()
        return new

    def unwrap(self, value=NoValue):
        """Execute :meth:`method` with :attr:`_value`, :attr:`args`, and
        :attr:`kargs`. If :attr:`_value` is an instance of
        :class:`ChainWrapper`, then unwrap it before calling :attr:`method`.
        """
        # Generate a copy of ourself so that we don't modify the chain wrapper
        # _value directly. This way if we are late passing a value, we don't
        # "freeze" the chain wrapper value when a value is first passed.
        # Otherwise, we'd locked the chain wrapper value permanently and not be
        # able to reuse it.
        wrapper = self._generate()

        if isinstance(wrapper._value, ChainWrapper):
            # pylint: disable=no-member,maybe-no-member
            wrapper._value = wrapper._value.unwrap(value)
        elif not isinstance(value, ChainWrapper) and value is not NoValue:
            # Override wrapper's initial value.
            wrapper._value = value

        if wrapper._value is not NoValue:
            value = wrapper._value

        return wrapper.method(value, *wrapper.args, **wrapper.kargs)

    def __call__(self, *args, **kargs):
        """Invoke the :attr:`method` with :attr:`value` as the first argument
        and return a new :class:`Chain` object with the return value.

        Returns:
            Chain: New instance of :class:`Chain` with the results of
                :attr:`method` passed in as value.
        """
        self.args = args
        self.kargs = kargs
        return Chain(self)


class _Chain(object):
    """Class that provides attribute access to valid :mod:`pydash` methods and
    callable access to :mod:`pydash` method chaining.
    """

    def __getattr__(self, attr):
        """Proxy to :meth:`Chain.get_method`."""
        return Chain.get_method(attr)

    def __call__(self, value=NoValue):
        """Return a new instance of :class:`Chain` with `value` as the seed."""
        return Chain(value)
