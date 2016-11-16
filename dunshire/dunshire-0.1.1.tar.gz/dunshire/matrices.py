"""
Utility functions for working with CVXOPT matrices (instances of the
class:`cvxopt.base.matrix` class).
"""

from copy import copy
from math import sqrt
from cvxopt import matrix
from cvxopt.lapack import gees, gesdd, syevr

from . import options


def append_col(left, right):
    """
    Append two matrices side-by-side.

    Parameters
    ----------

    left : matrix
        The "original" matrix, the one that will wind up on the left.

    right : matrix
        The matrix to be appended on the right of ``left``.

    Returns
    -------

    matrix
        A new matrix consisting of ``right`` appended to the right
        of ``left``.

    Examples
    --------

        >>> A = matrix([1,2,3,4], (2,2))
        >>> B = matrix([5,6,7,8,9,10], (2,3))
        >>> print(A)
        [ 1  3]
        [ 2  4]
        <BLANKLINE>
        >>> print(B)
        [  5   7   9]
        [  6   8  10]
        <BLANKLINE>
        >>> print(append_col(A,B))
        [  1   3   5   7   9]
        [  2   4   6   8  10]
        <BLANKLINE>

    """
    return matrix([left.trans(), right.trans()]).trans()


def append_row(top, bottom):
    """
    Append two matrices top-to-bottom.

    Parameters
    ----------

    top : matrix
        The "original" matrix, the one that will wind up on top.

    bottom : matrix
        The matrix to be appended below ``top``.

    Returns
    -------

    matrix
        A new matrix consisting of ``bottom`` appended below ``top``.

    Examples
    --------

        >>> A = matrix([1,2,3,4], (2,2))
        >>> B = matrix([5,6,7,8,9,10], (3,2))
        >>> print(A)
        [ 1  3]
        [ 2  4]
        <BLANKLINE>
        >>> print(B)
        [  5   8]
        [  6   9]
        [  7  10]
        <BLANKLINE>
        >>> print(append_row(A,B))
        [  1   3]
        [  2   4]
        [  5   8]
        [  6   9]
        [  7  10]
        <BLANKLINE>

    """
    return matrix([top, bottom])


def eigenvalues(symmat):
    """
    Return the eigenvalues of the given symmetric real matrix.

    On the surface, this appears redundant to the :func:`eigenvalues_re`
    function. However, if we know in advance that our input is
    symmetric, a better algorithm can be used.

    Parameters
    ----------

    symmat : matrix
        The real symmetric matrix whose eigenvalues you want.

    Returns
    -------

    list of float
       A list of the eigenvalues (in no particular order) of ``symmat``.

    Raises
    ------

    TypeError
        If the input matrix is not symmetric.

    Examples
    --------

        >>> A = matrix([[2,1],[1,2]], tc='d')
        >>> eigenvalues(A)
        [1.0, 3.0]

    If the input matrix is not symmetric, it may not have real
    eigenvalues, and we don't know what to do::

        >>> A = matrix([[1,2],[3,4]])
        >>> eigenvalues(A)
        Traceback (most recent call last):
        ...
        TypeError: input must be a symmetric real matrix

    """
    if not norm(symmat.trans() - symmat) < options.ABS_TOL:
        # Ensure that ``symmat`` is symmetric (and thus square).
        raise TypeError('input must be a symmetric real matrix')

    domain_dim = symmat.size[0]
    eigs = matrix(0, (domain_dim, 1), tc='d')

    # Create a copy of ``symmat`` here because ``syevr`` clobbers it.
    dummy = copy(symmat)
    syevr(dummy, eigs)
    return list(eigs)


def eigenvalues_re(anymat):
    """
    Return the real parts of the eigenvalues of the given square matrix.

    Parameters
    ----------

    anymat : matrix
        The square matrix whose eigenvalues you want.

    Returns
    -------

    list of float
       A list of the real parts (in no particular order) of the
       eigenvalues of ``anymat``.

    Raises
    ------

    TypeError
        If the input matrix is not square.

    Examples
    --------

    This is symmetric and has two real eigenvalues:

        >>> A = matrix([[2,1],[1,2]], tc='d')
        >>> sorted(eigenvalues_re(A))
        [1.0, 3.0]

    But this rotation matrix has eigenvalues `i` and `-i`, both of whose
    real parts are zero:

        >>> A = matrix([[0,-1],[1,0]])
        >>> eigenvalues_re(A)
        [0.0, 0.0]

    If the input matrix is not square, it doesn't have eigenvalues::

        >>> A = matrix([[1,2],[3,4],[5,6]])
        >>> eigenvalues_re(A)
        Traceback (most recent call last):
        ...
        TypeError: input matrix must be square

    """
    if not anymat.size[0] == anymat.size[1]:
        raise TypeError('input matrix must be square')

    domain_dim = anymat.size[0]
    eigs = matrix(0, (domain_dim, 1), tc='z')

    # Create a copy of ``anymat`` here for two reasons:
    #
    #   1. ``gees`` clobbers its input.
    #   2. We need to ensure that the type code of ``dummy`` is 'd' or 'z'.
    #
    dummy = matrix(anymat, anymat.size, tc='d')

    gees(dummy, eigs)
    return [eig.real for eig in eigs]


def identity(domain_dim, typecode='i'):
    """
    Create an identity matrix of the given dimensions.

    Parameters
    ----------

    domain_dim : int
        The dimension of the vector space on which the identity will act.

    typecode : {'i', 'd', 'z'}, optional
        The type code for the returned matrix, defaults to 'i' for integers.
        Can also be 'd' for real double, or 'z' for complex double.

    Returns
    -------

    matrix
        A ``domain_dim``-by-``domain_dim`` dense integer identity matrix.

    Raises
    ------

    ValueError
        If you ask for the identity on zero or fewer dimensions.

    Examples
    --------

       >>> print(identity(3))
       [ 1  0  0]
       [ 0  1  0]
       [ 0  0  1]
       <BLANKLINE>

    """
    if domain_dim <= 0:
        raise ValueError('domain dimension must be positive')

    entries = [int(i == j)
               for i in range(domain_dim)
               for j in range(domain_dim)]
    return matrix(entries, (domain_dim, domain_dim), tc=typecode)


def inner_product(vec1, vec2):
    """
    Compute the Euclidean inner product of two vectors.

    Parameters
    ----------

    vec1 : matrix
        The first vector, whose inner product with ``vec2`` you want.

    vec2 : matrix
        The second vector, whose inner product with ``vec1`` you want.

    Returns
    -------

    float
        The inner product of ``vec1`` and ``vec2``.

    Raises
    ------

    TypeError
        If the lengths of ``vec1`` and ``vec2`` differ.

    Examples
    --------

        >>> x = [1,2,3]
        >>> y = [3,4,1]
        >>> inner_product(x,y)
        14

        >>> x = matrix([1,1,1])
        >>> y = matrix([2,3,4], (1,3))
        >>> inner_product(x,y)
        9

        >>> x = [1,2,3]
        >>> y = [1,1]
        >>> inner_product(x,y)
        Traceback (most recent call last):
        ...
        TypeError: the lengths of vec1 and vec2 must match

    """
    if not len(vec1) == len(vec2):
        raise TypeError('the lengths of vec1 and vec2 must match')

    return sum([x*y for (x, y) in zip(vec1, vec2)])


def norm(matrix_or_vector):
    """
    Return the Frobenius norm of a matrix or vector.

    When the input is a vector, its matrix-Frobenius norm is the same
    thing as its vector-Euclidean norm.

    Parameters
    ----------

    matrix_or_vector : matrix
        The matrix or vector whose norm you want.

    Returns
    -------

    float
        The norm of ``matrix_or_vector``.

    Examples
    --------

        >>> v = matrix([1,1])
        >>> norm(v)
        1.414...

        >>> A = matrix([1,1,1,1], (2,2))
        >>> norm(A)
        2.0...

    """
    return sqrt(inner_product(matrix_or_vector, matrix_or_vector))


def specnorm(mat):
    """
    Return the spectral norm of a matrix.

    The spectral norm of a matrix is its largest singular value, and it
    corresponds to the operator norm induced by the vector Euclidean norm.

    Parameters
    ----------

    mat : matrix
        The matrix whose spectral norm you want.

    Examples:

        >>> specnorm(identity(3))
        1.0

        >>> specnorm(5*identity(4))
        5.0

    """
    num_eigs = min(mat.size)
    eigs = matrix(0, (num_eigs, 1), tc='d')
    typecode = 'd'
    if any([isinstance(entry, complex) for entry in mat]):
        typecode = 'z'
    dummy = matrix(mat, mat.size, tc=typecode)
    gesdd(dummy, eigs)

    if len(eigs) > 0:
        return eigs[0]
    else:
        return 0


def vec(mat):
    """
    Create a long vector in column-major order from ``mat``.

    Parameters
    ----------

    mat : matrix
        Any sort of real matrix that you want written as a long vector.

    Returns
    -------

    matrix
        An ``len(mat)``-by-``1`` long column vector containign the
        entries of ``mat`` in column major order.

    Examples
    --------

        >>> A = matrix([[1,2],[3,4]])
        >>> print(A)
        [ 1  3]
        [ 2  4]
        <BLANKLINE>

        >>> print(vec(A))
        [ 1]
        [ 2]
        [ 3]
        [ 4]
        <BLANKLINE>

    Note that if ``mat`` is a vector, this function is a no-op:

        >>> v = matrix([1,2,3,4], (4,1))
        >>> print(v)
        [ 1]
        [ 2]
        [ 3]
        [ 4]
        <BLANKLINE>
        >>> print(vec(v))
        [ 1]
        [ 2]
        [ 3]
        [ 4]
        <BLANKLINE>

    """
    return matrix(mat, (len(mat), 1))


def condition_number(mat):
    """
    Return the condition number of the given matrix.

    The condition number of a matrix quantifies how hard it is to do
    numerical computation with that matrix. It is usually defined as
    the ratio of the norm of the matrix to the norm of its inverse, and
    therefore depends on the norm used. One way to compute the condition
    number with respect to the 2-norm is as the ratio of the matrix's
    largest and smallest singular values. Since we have easy access to
    those singular values, that is the algorithm we use.

    The larger the condition number is, the worse the matrix is.

    Parameters
    ----------
    mat : matrix
        The matrix whose condition number you want.

    Returns
    -------

    float
        The nonnegative condition number of ``mat``.

    Examples
    --------

    >>> condition_number(identity(3))
    1.0

    >>> A = matrix([[2,1],[1,2]])
    >>> abs(condition_number(A) - 3.0) < options.ABS_TOL
    True

    >>> A = matrix([[2,1j],[-1j,2]])
    >>> abs(condition_number(A) - 3.0) < options.ABS_TOL
    True

    """
    num_eigs = min(mat.size)
    eigs = matrix(0, (num_eigs, 1), tc='d')
    typecode = 'd'
    if any([isinstance(entry, complex) for entry in mat]):
        typecode = 'z'
    dummy = matrix(mat, mat.size, tc=typecode)
    gesdd(dummy, eigs)

    if len(eigs) > 0:
        return eigs[0]/eigs[-1]
    else:
        return 0
