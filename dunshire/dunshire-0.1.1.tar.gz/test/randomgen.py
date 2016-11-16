"""
Random thing generators used in the rest of the test suite.
"""
from random import randint, uniform

from math import sqrt
from cvxopt import matrix
from dunshire.cones import NonnegativeOrthant, IceCream
from dunshire.games import SymmetricLinearGame
from dunshire.matrices import (append_col, append_row, identity)

MAX_COND = 125
"""
The maximum condition number of a randomly-generated game. When the
condition number of the games gets too high, we start to see
:class:`PoorScalingException` being thrown. There's no science to
choosing the upper bound -- it got lowered until those exceptions
stopped popping up. It's at ``125`` because ``129`` doesn't work.
"""

RANDOM_MAX = 10
"""
When generating random real numbers or integers, this is used as the
largest allowed magnitude. It keeps our condition numbers down and other
properties within reason.
"""

def random_scalar():
    """
    Generate a random scalar.

    Returns
    -------

    float
        A random real number between negative and positive
        :const:`RANDOM_MAX`, inclusive.

    Examples
    --------

        >>> abs(random_scalar()) <= RANDOM_MAX
        True

    """
    return uniform(-RANDOM_MAX, RANDOM_MAX)


def random_nn_scalar():
    """
    Generate a random nonnegative scalar.

    Returns
    -------

    float
        A random nonnegative real number between zero and
        :const:`RANDOM_MAX`, inclusive.

    Examples
    --------

        >>> 0 <= random_nn_scalar() <= RANDOM_MAX
        True

    """
    return abs(random_scalar())


def random_natural():
    """
    Generate a random natural number.

    Returns
    -------

    int
        A random natural number between ``1`` and :const:`RANDOM_MAX`,
        inclusive.

    Examples
    --------

        >>> 1 <= random_natural() <= RANDOM_MAX
        True

    """
    return randint(1, RANDOM_MAX)


def random_matrix(row_count, column_count=None):
    """
    Generate a random matrix.

    Parameters
    ----------

    row_count : int
        The number of rows you want in the returned matrix.

    column_count: int
        The number of columns you want in the returned matrix (default:
        the same as ``row_count``).

    Returns
    -------

    matrix
        A new matrix whose entries are random floats chosen uniformly
        between negative and positive :const:`RANDOM_MAX`.

    Examples
    --------

        >>> A = random_matrix(3)
        >>> A.size
        (3, 3)

        >>> A = random_matrix(3,2)
        >>> A.size
        (3, 2)

    """
    if column_count is None:
        column_count = row_count

    entries = [random_scalar() for _ in range(row_count*column_count)]
    return matrix(entries, (row_count, column_count))


def random_nonnegative_matrix(row_count, column_count=None):
    """
    Generate a random matrix with nonnegative entries.

    Parameters
    ----------

    row_count : int
        The number of rows you want in the returned matrix.

    column_count : int
        The number of columns you want in the returned matrix (default:
        the same as ``row_count``).

    Returns
    -------

    matrix
        A new matrix whose entries are chosen by :func:`random_nn_scalar`.

    Examples
    --------

        >>> A = random_nonnegative_matrix(3)
        >>> A.size
        (3, 3)
        >>> all([entry >= 0 for entry in A])
        True

        >>> A = random_nonnegative_matrix(3,2)
        >>> A.size
        (3, 2)
        >>> all([entry >= 0 for entry in A])
        True

    """
    if column_count is None:
        column_count = row_count

    entries = [random_nn_scalar() for _ in range(row_count*column_count)]
    return matrix(entries, (row_count, column_count))


def random_diagonal_matrix(dims):
    """
    Generate a random square matrix with zero off-diagonal entries.

    These matrices are Lyapunov-like on the nonnegative orthant, as is
    fairly easy to see.

    Parameters
    ----------

    dims : int
        The number of rows/columns you want in the returned matrix.

    Returns
    -------

    matrix
        A new matrix whose diagonal entries are random floats chosen
        using :func:`random_scalar` and whose off-diagonal entries are
        zero.

    Examples
    --------

        >>> A = random_diagonal_matrix(3)
        >>> A.size
        (3, 3)
        >>> A[0,1] == A[0,2] == A[1,0] == A[2,0] == A[1,2] == A[2,1] == 0
        True

    """
    return matrix([[random_scalar()*int(i == j)
                    for i in range(dims)]
                   for j in range(dims)])


def random_skew_symmetric_matrix(dims):
    """
    Generate a random skew-symmetrix matrix.

    Parameters
    ----------

    dims : int
        The number of rows/columns you want in the returned matrix.

    Returns
    -------

    matrix
        A new skew-matrix whose strictly above-diagonal entries are
        random floats chosen with :func:`random_scalar`.

    Examples
    --------

        >>> A = random_skew_symmetric_matrix(3)
        >>> A.size
        (3, 3)

        >>> from dunshire.options import ABS_TOL
        >>> from dunshire.matrices import norm
        >>> A = random_skew_symmetric_matrix(random_natural())
        >>> norm(A + A.trans()) < ABS_TOL
        True

    """
    strict_ut = [[random_scalar()*int(i < j)
                  for i in range(dims)]
                 for j in range(dims)]

    strict_ut = matrix(strict_ut, (dims, dims))
    return strict_ut - strict_ut.trans()


def random_lyapunov_like_icecream(dims):
    r"""
    Generate a random matrix Lyapunov-like on the ice-cream cone.

    The form of these matrices is cited in Gowda and Tao
    [GowdaTao]_. The scalar ``a`` and the vector ``b`` (using their
    notation) are easy to generate. The submatrix ``D`` is a little
    trickier, but it can be found noticing that :math:`C + C^{T} = 0`
    for a skew-symmetric matrix :math:`C` implying that :math:`C + C^{T}
    + \left(2a\right)I = \left(2a\right)I`. Thus we can stick an
    :math:`aI` with each of :math:`C,C^{T}` and let those be our
    :math:`D,D^{T}`.

    Parameters
    ----------

    dims : int
        The dimension of the ice-cream cone (not of the matrix you want!)
        on which the returned matrix should be Lyapunov-like.

    Returns
    -------

    matrix
        A new matrix, Lyapunov-like on the ice-cream cone in ``dims``
        dimensions, whose free entries are random floats chosen uniformly
        between negative and positive :const:`RANDOM_MAX`.

    References
    ----------

    .. [GowdaTao] M. S. Gowda and J. Tao. On the bilinearity rank of a
       proper cone and Lyapunov-like transformations. Mathematical
       Programming, 147:155-170, 2014.

    Examples
    --------

        >>> L = random_lyapunov_like_icecream(3)
        >>> L.size
        (3, 3)

        >>> from dunshire.options import ABS_TOL
        >>> from dunshire.matrices import inner_product
        >>> x = matrix([1,1,0])
        >>> s = matrix([1,-1,0])
        >>> abs(inner_product(L*x, s)) < ABS_TOL
        True

    """
    a = matrix([random_scalar()], (1, 1))
    b = matrix([random_scalar() for _ in range(dims-1)], (dims-1, 1))
    D = random_skew_symmetric_matrix(dims-1) + a*identity(dims-1)
    row1 = append_col(a, b.trans())
    row2 = append_col(b, D)
    return append_row(row1, row2)


def random_orthant_game():
    """
    Generate a random game over the nonnegative orthant.

    We generate each of ``L``, ``K``, ``e1``, and ``e2`` randomly within
    the constraints of the nonnegative orthant, and then construct a
    game from them. The process is repeated until we generate a game with
    a condition number under :const:`MAX_COND`.

    Returns
    -------

    SymmetricLinearGame
        A random game over some nonnegative orthant.

    Examples
    --------

        >>> random_orthant_game()
        <dunshire.games.SymmetricLinearGame object at 0x...>

    """
    ambient_dim = random_natural() + 1
    K = NonnegativeOrthant(ambient_dim)
    e1 = [0.1 + random_nn_scalar() for _ in range(K.dimension())]
    e2 = [0.1 + random_nn_scalar() for _ in range(K.dimension())]
    L = random_matrix(K.dimension())
    G = SymmetricLinearGame(L, K, e1, e2)

    if G.condition() <= MAX_COND:
        return G
    else:
        return random_orthant_game()


def random_icecream_game():
    """
    Generate a random game over the ice-cream cone.

    We generate each of ``L``, ``K``, ``e1``, and ``e2`` randomly within
    the constraints of the ice-cream cone, and then construct a game
    from them. The process is repeated until we generate a game with a
    condition number under :const:`MAX_COND`.

    Returns
    -------

    SymmetricLinearGame
        A random game over some ice-cream cone.

    Examples
    --------

        >>> random_icecream_game()
        <dunshire.games.SymmetricLinearGame object at 0x...>

    """
    # Use a minimum dimension of two to avoid divide-by-zero in
    # the fudge factor we make up later.
    ambient_dim = random_natural() + 1
    K = IceCream(ambient_dim)
    e1 = [1] # Set the "height" of e1 to one
    e2 = [1] # And the same for e2

    # If we choose the rest of the components of e1,e2 randomly
    # between 0 and 1, then the largest the squared norm of the
    # non-height part of e1,e2 could be is the 1*(dim(K) - 1). We
    # need to make it less than one (the height of the cone) so
    # that the whole thing is in the cone. The norm of the
    # non-height part is sqrt(dim(K) - 1), and we can divide by
    # twice that.
    fudge_factor = 1.0 / (2.0*sqrt(K.dimension() - 1.0))
    e1 += [fudge_factor*uniform(0, 1) for _ in range(K.dimension() - 1)]
    e2 += [fudge_factor*uniform(0, 1) for _ in range(K.dimension() - 1)]
    L = random_matrix(K.dimension())
    G = SymmetricLinearGame(L, K, e1, e2)

    if G.condition() <= MAX_COND:
        return G
    else:
        return random_icecream_game()


def random_ll_orthant_game():
    """
    Return a random Lyapunov game over some nonnegative orthant.

    We first construct a :func:`random_orthant_game` and then modify it
    to have a :func:`random_diagonal_matrix` as its operator. Such
    things are Lyapunov-like on the nonnegative orthant. That process is
    repeated until the condition number of the resulting game is within
    :const:`MAX_COND`.

    Returns
    -------

    SymmetricLinearGame

        A random game over some nonnegative orthant whose
        :meth:`dunshire.games.SymmetricLinearGame.payoff` method is
        based on a Lyapunov-like
        :meth:`dunshire.games.SymmetricLinearGame.L` operator.

    Examples
    --------

        >>> random_ll_orthant_game()
        <dunshire.games.SymmetricLinearGame object at 0x...>

    """
    G = random_orthant_game()
    L = random_diagonal_matrix(G.dimension())

    # Replace the totally-random ``L`` with random Lyapunov-like one.
    G = SymmetricLinearGame(L, G.K(), G.e1(), G.e2())

    while G.condition() > MAX_COND:
        # Try again until the condition number is satisfactory.
        G = random_orthant_game()
        L = random_diagonal_matrix(G.dimension())
        G = SymmetricLinearGame(L, G.K(), G.e1(), G.e2())

    return G


def random_ll_icecream_game():
    """
    Return a random Lyapunov game over some ice-cream cone.

    We first construct a :func:`random_icecream_game` and then modify it
    to have a :func:`random_lyapunov_like_icecream` operator. That
    process is repeated until the condition number of the resulting game
    is within :const:`MAX_COND`.

    Returns
    -------

    SymmetricLinearGame
        A random game over some ice-cream cone whose
        :meth:`dunshire.games.SymmetricLinearGame.payoff` method
        is based on a Lyapunov-like
        :meth:`dunshire.games.SymmetricLinearGame.L` operator.

    Examples
    --------

        >>> random_ll_icecream_game()
        <dunshire.games.SymmetricLinearGame object at 0x...>

    """
    G = random_icecream_game()
    L = random_lyapunov_like_icecream(G.dimension())

    # Replace the totally-random ``L`` with random Lyapunov-like one.
    G = SymmetricLinearGame(L, G.K(), G.e1(), G.e2())

    while G.condition() > MAX_COND:
        # Try again until the condition number is satisfactory.
        G = random_icecream_game()
        L = random_lyapunov_like_icecream(G.dimension())
        G = SymmetricLinearGame(L, G.K(), G.e1(), G.e2())

    return G


def random_positive_orthant_game():
    """
    Return a random game over the nonnegative orthant with a positive
    operator.

    We first construct a :func:`random_orthant_game` and then modify it
    to have a :func:`random_nonnegative_matrix` as its operator. That
    process is repeated until the condition number of the resulting game
    is within :const:`MAX_COND`.

    Returns
    -------

    SymmetricLinearGame
        A random game over some nonnegative orthant whose
        :meth:`dunshire.games.SymmetricLinearGame.payoff` method
        is based on a positive
        :meth:`dunshire.games.SymmetricLinearGame.L` operator.

    Examples
    --------

        >>> random_positive_orthant_game()
        <dunshire.games.SymmetricLinearGame object at 0x...>

    """

    G = random_orthant_game()
    L = random_nonnegative_matrix(G.dimension())

    # Replace the totally-random ``L`` with the random nonnegative one.
    G = SymmetricLinearGame(L, G.K(), G.e1(), G.e2())

    while G.condition() > MAX_COND:
        # Try again until the condition number is satisfactory.
        G = random_orthant_game()
        L = random_nonnegative_matrix(G.dimension())
        G = SymmetricLinearGame(L, G.K(), G.e1(), G.e2())

    return G


def random_nn_scaling(G):
    """
    Scale the given game by a random nonnegative amount.

    We re-attempt the scaling with a new random number until the
    resulting scaled game has an acceptable condition number.

    Parameters
    ----------

    G : SymmetricLinearGame
        The game that you would like to scale.

    Returns
    -------
    (float, SymmetricLinearGame)
        A pair containing the both the scaling factor and the new scaled game.

    Examples
    --------

        >>> from dunshire.matrices import norm
        >>> from dunshire.options import ABS_TOL
        >>> G = random_orthant_game()
        >>> (alpha, H) = random_nn_scaling(G)
        >>> alpha >= 0
        True
        >>> G.K() == H.K()
        True
        >>> norm(G.e1() - H.e1()) < ABS_TOL
        True
        >>> norm(G.e2() - H.e2()) < ABS_TOL
        True

    """
    alpha = random_nn_scalar()
    H = SymmetricLinearGame(alpha*G.L().trans(), G.K(), G.e1(), G.e2())

    while H.condition() > MAX_COND:
        # Loop until the condition number of H doesn't suck.
        alpha = random_nn_scalar()
        H = SymmetricLinearGame(alpha*G.L().trans(), G.K(), G.e1(), G.e2())

    return (alpha, H)


def random_translation(G):
    """
    Translate the given game by a random amount.

    We re-attempt the translation with new random scalars until the
    resulting translated game has an acceptable condition number.

    Parameters
    ----------

    G : SymmetricLinearGame
        The game that you would like to translate.

    Returns
    -------
    (float, SymmetricLinearGame)
        A pair containing the both the translation distance and the new
        scaled game.

    Examples
    --------

        >>> from dunshire.matrices import norm
        >>> from dunshire.options import ABS_TOL
        >>> G = random_orthant_game()
        >>> (alpha, H) = random_translation(G)
        >>> G.K() == H.K()
        True
        >>> norm(G.e1() - H.e1()) < ABS_TOL
        True
        >>> norm(G.e2() - H.e2()) < ABS_TOL
        True

    """
    alpha = random_scalar()
    tensor_prod = G.e1() * G.e2().trans()
    M = G.L() + alpha*tensor_prod

    H = SymmetricLinearGame(M.trans(), G.K(), G.e1(), G.e2())
    while H.condition() > MAX_COND:
        # Loop until the condition number of H doesn't suck.
        alpha = random_scalar()
        M = G.L() + alpha*tensor_prod
        H = SymmetricLinearGame(M.trans(), G.K(), G.e1(), G.e2())

    return (alpha, H)
