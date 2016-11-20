import re
from decimal import Decimal, InvalidOperation
from dimana import exc
from dimana.typecheck import typecheck


class Units (object):

    class Mismatch (TypeError):
        """Represents binary operations on incompatible unit dimensions."""
        def __init__(self, tmpl, *a):
            TypeError.__init__(self, tmpl.format(*a))

    class ParseError (exc.ParseError):
        pass

    @classmethod
    def parse(cls, text):
        m = cls._rgx_frac.match(text)
        if m is None:
            raise cls.ParseError('Could not parse Units: {!r}', text)

        loopinfo = []

        numertext = m.group('numer')
        if numertext != '1':
            loopinfo.append((numertext, 1))

        denomtext = m.group('denom')
        if denomtext is not None:
            if denomtext[0] == '(' and denomtext[-1] == ')':
                denomtext = denomtext[1:-1]
            loopinfo.append((denomtext, -1))

        dp = {}
        for t, inv in loopinfo:
            for term in t.split('*'):
                term = term.strip()
                parts = term.split('^', 1)
                if len(parts) == 1:
                    parts.append('1')
                try:
                    [uname, powtext] = parts
                    pow = Decimal(powtext) * inv

                    if cls._rgx_uname.match(uname) is None:
                        raise ValueError()

                except (ValueError, InvalidOperation):
                    raise cls.ParseError(
                        'Could not parse Units term: {!r} in {!r}',
                        term,
                        text,
                    )
                pow += dp.pop(uname, 0)
                if pow != 0:
                    dp[uname] = pow

        return cls(dp)

    def __new__(cls, dimpowers):
        dpkey = tuple(sorted(dimpowers.iteritems()))
        inst = cls._instances.get(dpkey)
        if inst is None:
            inst = super(Units, cls).__new__(cls, dimpowers)
            cls._instances[dpkey] = inst
        return inst

    def __init__(self, dimpowers):
        if not hasattr(self, '_dimpowers'):
            self._dimpowers = dimpowers
        # Else: this instance has already been initialized.

    # Custom Methods:
    def match(self, other):
        typecheck(other, Units)
        if self is not other:
            raise Units.Mismatch(
                'Units mismatch: {!r} vs {!r}',
                str(self),
                str(other),
            )

    # str/repr Methods:
    def __str__(self):
        numer = []
        denom = []

        def append_power(l, n, p):
            l.append(n if p == 1 else '{}^{}'.format(n, p))

        for n, p in sorted(self._dimpowers.iteritems()):
            if p > 0:
                append_power(numer, n, p)
            else:
                append_power(denom, n, -p)

        result = ' * '.join(numer) if numer else '1'
        if denom:
            dnr = ' * '.join(denom)
            if len(denom) > 1:
                dnr = '({})'.format(dnr)
            result = '{} / {}'.format(result, dnr)
        return result

    def __repr__(self):
        return '<{} {!r}>'.format(type(self).__name__, str(self))

    # Arithmethic Methods:
    def __add__(self, other):
        self.match(other)
        return self

    __sub__ = __add__

    def __neg__(self):
        return self

    def __mul__(self, other):
        if isinstance(other, Units):
            newdp = {}

            def set_dp(n, p):
                assert n not in newdp, repr((newdp, n, p))
                if p != 0:
                    newdp[n] = p

            tmpdp = dict(self._dimpowers)
            for uname, power in other._dimpowers.iteritems():
                set_dp(uname, power + tmpdp.pop(uname, 0))
            for uname, power in tmpdp.iteritems():
                set_dp(uname, power)
            return Units(newdp)
        else:
            raise TypeError(
                'Units multiplied against non-Units {!r}'
                .format(type(other))
            )

    def __div__(self, other):
        return self * (other ** -1)

    __truediv__ = __div__

    def __pow__(self, p):
        newdp = {}
        if p != 0:
            for uname, power in self._dimpowers.iteritems():
                newdp[uname] = power * p
        return Units(newdp)

    # Private:
    _rgx_frac = re.compile(
        r'''
          ^(?P<numer>
            1
            | [a-z]([a-z0-9_ *^.-]*?[a-z0-9_])?
          )(
            \ */\ *(?P<denom>
              [a-z]([a-z0-9_ *^.-]*?[a-z0-9_])?
              | \([a-z0-9_ *^.-]*?\)
            )
          )?$
        ''',
        re.IGNORECASE | re.VERBOSE,
    )
    _rgx_uname = re.compile(
        r'^[a-z][a-z0-9_]*$',
        re.IGNORECASE,
    )

    _instances = {}


Units.scalar = Units({})
