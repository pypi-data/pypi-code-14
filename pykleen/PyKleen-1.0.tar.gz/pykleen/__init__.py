# -*- coding: utf-8 -*-
import datetime as dt
import re
from decimal import Decimal, ROUND_HALF_UP, DecimalException, InvalidOperation
from typing import List, Dict, Any, Callable
from typing import Union

import bleach


class Undefined(object):
    pass


def flatten_error(error):
    if isinstance(error, Errors):
        return error.errors
    else:
        return str(error)


class Error(Exception):
    pass


class Errors(Error):
    def __init__(self, errors: Dict[str, str] = None, message: str = None):
        super(Errors, self).__init__(message)
        self.errors = errors or dict()

    def __str__(self):
        keys = sorted(str(x) for x in self.errors.keys())

        if self.args[0]:
            return '<Errors [%s] %s>' % (', '.join(keys), self.args[0])
        else:
            return '<Errors [%s]>' % ', '.join(keys)


class Test(object):
    def __init__(self, error: str = 'Do not use this class.'):
        self.error = error

    def __call__(self, value):
        # print('Calling %s on "%s"' % (self, value))
        return value


class One(Test):
    def __init__(self, callback: Union[Callable, Test],
                 error: str = 'Test failed.'):
        super().__init__(error)
        self.callback = callback

    def __call__(self, value):
        value = super().__call__(value)
        if isinstance(self.callback, (To, Yield)):
            value = self.callback(value)
        elif not self.callback(value):
            raise Error(self.error)

        return value


class All(Test):
    def __init__(self, callbacks: List[Union[Callable, Test]],
                 error: str = 'Test failed.'):
        super().__init__(error)
        self.callbacks = callbacks

    def __call__(self, value):
        value = super().__call__(value)
        for callback in self.callbacks:
            if isinstance(callback, (Test)):
                value = callback(value)
            elif not callback(value):
                raise Error(self.error)

        return value


class Or(Test):
    def __init__(self, callbacks: List[Union[Callable, Test]],
                 error: str = 'All tests failed.'):
        super().__init__(error)
        self.callbacks = callbacks

    def __call__(self, value):
        value = super().__call__(value)
        for callback in self.callbacks:
            try:
                return callback(value)
            except Error as exc:
                continue

        raise Error(self.error)


class To(Test):
    def __init__(self, into: Union[Callable, Test],
                 error: str = 'Conversion failed.'):
        super().__init__(error)
        self.into = into

    def __call__(self, value):
        value = super().__call__(value)
        exceptions = (ValueError, AssertionError, IndexError, KeyError,
                      InvalidOperation)

        try:
            return self.into(value)
        except exceptions:
            raise Error(self.error)


class Yield(Test):
    def __init__(self, callback: Union[Callable, Test],
                 fixed_result: Any, error: str = 'Test failed.'):
        super().__init__(error)
        self.callback = callback
        self.fixed_result = fixed_result

    def __call__(self, value):
        value = super().__call__(value)

        if self.callback(value):
            return self.fixed_result
        else:
            raise Error(self.error)


class Param(object):
    def __init__(self, name: str, default: Any = Undefined):
        self.name = name
        self._default = default

    @property
    def is_required(self):
        return self.default is Undefined

    @property
    def default(self):
        if self._default is Undefined:
            return Undefined
        elif callable(self._default):
            return self._default()
        else:
            return self._default


class Schema(Test):
    def __init__(self, items: Dict[Union[str, Param], Test],
                 error: str = None, required_error: str = 'Required.',
                 nothing_is_required: bool = False,
                 fail_to_none: bool = False):
        super().__init__(error)
        self.items = dict()  # type: Dict[str, Test]
        self.params = dict()  # type: Dict[str, Param]
        self.required_error = required_error
        self.nothing_is_required = nothing_is_required
        self.fail_to_none = fail_to_none

        for key, callback in items.items():
            if isinstance(key, str):
                key = Param(key, None if nothing_is_required else Undefined)
            self.items[key.name] = callback
            self.params[key.name] = key

    def __call__(self, value: Dict[str, Any], fail_to_none: bool = None):
        ftn = fail_to_none if fail_to_none is not None else self.fail_to_none
        errors = dict()
        result = dict()
        for key, callback in self.items.items():
            param = self.params[key]
            if key not in value:
                if param.is_required:
                    if ftn:
                        result[key] = None
                    else:
                        errors[key] = self.required_error
                else:
                    result[key] = param.default
            else:
                try:
                    result[key] = callback(value[key])
                except Error as exc:
                    if ftn:
                        result[key] = None
                    else:
                        errors[key] = flatten_error(exc)

        if len(errors):
            raise Errors(errors, self.error)
        else:
            return result


def is_instance(types, type_error: str = 'Invalid type %s.'):
    def _is_instance(value):
        if not isinstance(value, types):
            raise Error(type_error % type(value).__name__)
        return value

    return To(_is_instance)


SIZE_TYPES = (str, bytes, list, tuple, set)
SizeTypes = Union[str, bytes, list, tuple, set]


def size(min_len: int = None, max_len: int = None,
         min_len_error: str = 'Too short.', max_len_error: str = 'Too long.',
         type_error: str = 'Invalid type %s.') -> Callable[
    [SizeTypes], SizeTypes]:
    tests = [is_instance(SIZE_TYPES, type_error)]

    if min_len is not None:
        tests.append(One(lambda v: len(v) > min_len, min_len_error))
    if max_len is not None:
        tests.append(One(lambda v: len(v) < max_len, max_len_error))

    return All(tests)


def string(min_len: int = None, max_len: int = None,
           strip_tags: bool = True, allowed_tags: List[str] = None,
           allowed_attributes: Dict[str, List[str]] = None,
           strip: bool = True,
           min_len_error: str = 'Too short.',
           max_len_error: str = 'Too long.') -> Callable[[Any], str]:
    def _convert(value):
        if isinstance(value, bytes):
            return value.decode('utf-8')
        else:
            return str(value)

    tests = [
        To(_convert),
    ]
    if strip_tags:
        tests.append(To(lambda v: bleach.clean(
            v,
            tags=allowed_tags or list(),
            attributes=allowed_attributes or list(),
            strip=True)))
    if strip:
        tests.append(To(lambda v: v.strip()))

    if min_len or max_len:
        tests.append(size(min_len, max_len, min_len_error, max_len_error))

    return All(tests)


def regex(pattern: str, cast_to_string: Callable = None,
          error: str = 'Does not match.'):
    if cast_to_string is None:
        cast_to_string = string()

    return All([
        cast_to_string,
        One(lambda v: re.match(pattern, v) is not None, error),
    ])


def numeric(decimals: int = 0, rounding: str = ROUND_HALF_UP,
            at_least: int = None, at_most: int = None,
            at_least_error: str = 'Too small.',
            at_most_error: str = 'Too large.',
            cast_error: str = 'Invalid number.') -> Callable[[Any], Decimal]:
    def _convert(value):
        try:
            value = value.replace(',', '.')  # type: str
            if value.count('.') > 1:
                split = value.rsplit('.', 1)
                value = '%s.%s' % (split[0].replace('.', ''), split[1])
            result = Decimal(value)
            if result.is_infinite():
                raise Error(cast_error)
            elif result.is_nan():
                raise Error(cast_error)
            else:
                return result
        except DecimalException:
            raise Error(cast_error)

    tests = [
        To(str), To(_convert),
    ]

    if at_least is not None:
        tests.append(One(lambda v: v > at_least, at_least_error))
    if at_most is not None:
        tests.append(One(lambda v: v < at_most, at_most_error))

    tests.append(To(lambda v:
                    v.quantize(Decimal('1.' + '0' * decimals), rounding)))
    return All(tests)


def boolean(is_true_when: List[str] = None, is_false_when: List[str] = None,
            cast_error: str = 'Invalid boolean.') -> Callable[[Any], bool]:
    tests = [
        To(str),
    ]

    if not is_true_when and not is_false_when:
        is_true_when = ['True', 'true', '1', 'yes', 'y', 'on']

    if is_true_when and not is_false_when:
        tests.append(To(lambda v: v in is_true_when))
    elif not is_true_when and is_false_when:
        tests.append(To(lambda v: v not in is_false_when))
    else:
        tests.append(One(lambda v: v in is_true_when + is_false_when,
                         cast_error))
        tests.append(To(lambda v: v in is_true_when))

    return All(tests)


def datetime(formats: List[str] = None,
             parse_error: str = 'Invalid datetime.') -> Callable[[Any],
                                                                 dt.date]:
    if formats is None:
        formats = [
            '%Y-%m-%d %H:%M', '%d-%m-%Y %H:%M',
            '%Y-%m-%d %H:%M:%S', '%d-%m-%Y %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',
        ]

    def _convert(value):
        for f in iter(formats):
            try:
                return dt.datetime.strptime(value, f)
            except ValueError:
                continue
        raise Error(parse_error)

    return All([
        To(str),
        To(_convert),
    ])


def date(formats: List[str] = None,
         parse_error: str = 'Invalid date.') -> Callable[[Any], dt.date]:
    if formats is None:
        formats = ['%Y-%m-%d', '%d-%m-%Y']

    def _convert(value):
        for f in iter(formats):
            try:
                return dt.datetime.strptime(value, f).date()
            except ValueError:
                continue
        raise Error(parse_error)

    return All([
        To(str),
        To(_convert),
    ])


def minutes(error: str = 'Invalid format.') -> Callable[[Any], int]:
    def _convert(value: str):
        if not len(value):
            return 0

        if re.search(r'[:,.]', value):
            h, m = re.split(r'[:,.]', value)
            return int(h) * 60 + int(m)
        elif len(value) in [3, 4]:
            h = int(value[:-2])
            m = int(value[-2:])
            return int(h) * 60 + int(m)
        else:
            return int(value)

    return All([
        To(str),
        To(_convert, error=error),
    ])


def one_of(values: List[Any],
           cast: Union[Callable, Test] = None,
           invalid_error: str = 'Invalid value.') -> Callable[[Any], bool]:
    tests = list()

    if cast:
        tests.append(To(cast))

    tests.append(One(lambda v: v in values, invalid_error))

    return All(tests)


def convert_to_list(type_error: str = 'Invalid type %s.'):
    def _convert(value):
        if isinstance(value, (str, bytes)):
            return value.split(',')
        if isinstance(value, (int, Decimal, dt.datetime, dt.date)):
            return [value]
        elif isinstance(value, (list, tuple, set)):
            return value
        else:
            raise Error(type_error % type(value).__name__)

    return To(_convert)


def set_of(values: List[Any],
           cast: Union[Callable, Test] = None,
           invalid_error: str = 'Invalid value(s) %s.',
           type_error: str = 'Invalid type %s.') -> Callable[[Any], bool]:
    tests = [convert_to_list(type_error)]

    if cast:
        tests.append(To(lambda v: [cast(x) for x in v]))

    def _test(value):
        wrong = [v for v in value if v not in values]
        if len(wrong):
            raise Error(invalid_error % ', '.join(str(w) for w in wrong))
        return True

    tests.append(One(_test))

    return All(tests)


def list_of(cast: Union[Callable, Test],
            error: str = 'Invalid item(s).',
            type_error: str = 'Invalid type %s.'):
    def _run(values):
        errors = dict()
        result = list()

        for vx, value in enumerate(values):
            try:
                result.append(cast(value))
            except Error as exc:
                errors[vx] = flatten_error(exc)

        if len(errors):
            raise Errors(errors, error)
        else:
            return result

    return All([convert_to_list(type_error), To(_run)])
