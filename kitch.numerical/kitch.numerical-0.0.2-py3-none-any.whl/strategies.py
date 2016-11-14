import math

from hypothesis import assume
from hypothesis import strategies as st

__all__ = [
    'naturals',
    'finite_floats',
    'finite_decimals',
    'reals',
    'non_numeric',
    'sequences',
    'equal_len_sequences',
    'unequal_len_sequences',
]


@st.composite
def naturals(draw, zero=False):
    """A strategy that returns a natural number in 1, 2, 3, ...

    If zero is True, 0 is included in the natural numbers.
    """
    start = 0 if zero else 1
    return draw(st.integers(min_value=start))


@st.composite
def finite_floats(draw, min_value=None, max_value=None):
    """A strategy that returns floats without infinity, -infinity or NaN."""
    return draw(st.floats(min_value=min_value, max_value=max_value,
                          allow_nan=False, allow_infinity=False))


@st.composite
def finite_decimals(draw, min_value=None, max_value=None):
    """A strategy that returns decimals without infinity, -infinity or NaN."""
    dec = draw(st.decimals(min_value=min_value, max_value=max_value))
    assume(math.isfinite(dec))
    assume(not math.isnan(dec))
    return dec


@st.composite
def reals(draw, min_value=None, max_value=None):
    """A strategy that returns either an int, a float, or a decimal number,
    excluding infinity, -infinity and NaN.
    """
    kwargs = {'min_value': min_value, 'max_value': max_value}
    return draw(st.one_of(
        st.integers(**kwargs),
        finite_floats(**kwargs),
        finite_decimals(**kwargs),
    ))


@st.composite
def non_numeric(draw):
    """A strategy returning objects of any type except for numbers."""
    return draw(st.one_of(st.text(), st.characters(), st.booleans()))


@st.composite
def sequences(draw, elements, length=None):
    """A strategy returning lists/tuples of the element type and length."""
    min_size = length if length is not None else 1
    seq = draw(st.lists(elements, min_size=min_size, max_size=length))
    return draw(st.sampled_from((seq, tuple(seq))))


@st.composite
def equal_len_sequences(draw, elements):
    """A strategy returing a list of lists of the same length."""
    size = draw(st.sampled_from(range(1, 10)))
    return draw(st.lists(sequences(elements, size), min_size=1))


@st.composite
def unequal_len_sequences(draw, elements):
    """A strategy returning a list of lists of different lengths."""
    seq1 = draw(st.lists(elements, min_size=1))
    seq2 = draw(st.lists(elements, min_size=1))
    assume(len(seq1) != len(seq2))
    return (seq1, seq2)
