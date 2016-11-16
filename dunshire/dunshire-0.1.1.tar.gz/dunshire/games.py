"""
Symmetric linear games and their solutions.

This module contains the main :class:`SymmetricLinearGame` class that
knows how to solve a linear game.
"""
from cvxopt import matrix, printing, solvers
from .cones import CartesianProduct
from .errors import GameUnsolvableException, PoorScalingException
from .matrices import (append_col, append_row, condition_number, identity,
                       inner_product, norm, specnorm)
from .options import ABS_TOL, FLOAT_FORMAT, DEBUG_FLOAT_FORMAT

printing.options['dformat'] = FLOAT_FORMAT


class Solution:
    """
    A representation of the solution of a linear game. It should contain
    the value of the game, and both players' strategies.

    Examples
    --------

        >>> print(Solution(10, matrix([1,2]), matrix([3,4])))
        Game value: 10.000...
        Player 1 optimal:
          [ 1]
          [ 2]
        Player 2 optimal:
          [ 3]
          [ 4]

    """
    def __init__(self, game_value, p1_optimal, p2_optimal):
        """
        Create a new Solution object from a game value and two optimal
        strategies for the players.
        """
        self._game_value = game_value
        self._player1_optimal = p1_optimal
        self._player2_optimal = p2_optimal

    def __str__(self):
        """
        Return a string describing the solution of a linear game.

        The three data that are described are,

          * The value of the game.
          * The optimal strategy of player one.
          * The optimal strategy of player two.

        The two optimal strategy vectors are indented by two spaces.
        """
        tpl = 'Game value: {:.7f}\n' \
              'Player 1 optimal:{:s}\n' \
              'Player 2 optimal:{:s}'

        p1_str = '\n{!s}'.format(self.player1_optimal())
        p1_str = '\n  '.join(p1_str.splitlines())
        p2_str = '\n{!s}'.format(self.player2_optimal())
        p2_str = '\n  '.join(p2_str.splitlines())

        return tpl.format(self.game_value(), p1_str, p2_str)


    def game_value(self):
        """
        Return the game value for this solution.

        Examples
        --------

            >>> s = Solution(10, matrix([1,2]), matrix([3,4]))
            >>> s.game_value()
            10

        """
        return self._game_value


    def player1_optimal(self):
        """
        Return player one's optimal strategy in this solution.

        Examples
        --------

            >>> s = Solution(10, matrix([1,2]), matrix([3,4]))
            >>> print(s.player1_optimal())
            [ 1]
            [ 2]
            <BLANKLINE>

        """
        return self._player1_optimal


    def player2_optimal(self):
        """
        Return player two's optimal strategy in this solution.

        Examples
        --------

            >>> s = Solution(10, matrix([1,2]), matrix([3,4]))
            >>> print(s.player2_optimal())
            [ 3]
            [ 4]
            <BLANKLINE>

        """
        return self._player2_optimal


class SymmetricLinearGame:
    r"""
    A representation of a symmetric linear game.

    The data for a symmetric linear game are,

      * A "payoff" operator ``L``.
      * A symmetric cone ``K``.
      * Two points ``e1`` and ``e2`` in the interior of ``K``.

    The ambient space is assumed to be the span of ``K``.

    With those data understood, the game is played as follows. Players
    one and two choose points :math:`x` and :math:`y` respectively, from
    their respective strategy sets,

    .. math::
        \begin{aligned}
            \Delta_{1}
            &=
            \left\{
              x \in K \ \middle|\ \left\langle x, e_{2} \right\rangle = 1
            \right\}\\
            \Delta_{2}
            &=
            \left\{
              y \in K \ \middle|\ \left\langle y, e_{1} \right\rangle = 1
            \right\}.
        \end{aligned}

    Afterwards, a "payout" is computed as :math:`\left\langle
    L\left(x\right), y \right\rangle` and is paid to player one out of
    player two's pocket. The game is therefore zero sum, and we suppose
    that player one would like to guarantee himself the largest minimum
    payout possible. That is, player one wishes to,

    .. math::
        \begin{aligned}
            \text{maximize }
              &\underset{y \in \Delta_{2}}{\min}\left(
                \left\langle L\left(x\right), y \right\rangle
              \right)\\
            \text{subject to } & x \in \Delta_{1}.
        \end{aligned}

    Player two has the simultaneous goal to,

    .. math::
        \begin{aligned}
            \text{minimize }
              &\underset{x \in \Delta_{1}}{\max}\left(
                \left\langle L\left(x\right), y \right\rangle
              \right)\\
            \text{subject to } & y \in \Delta_{2}.
        \end{aligned}

    These goals obviously conflict (the game is zero sum), but an
    existence theorem guarantees at least one optimal min-max solution
    from which neither player would like to deviate. This class is
    able to find such a solution.

    Parameters
    ----------

    L : list of list of float
        A matrix represented as a list of **rows**. This representation
        agrees with (for example) `SageMath <http://www.sagemath.org/>`_
        and `NumPy <http://www.numpy.org/>`_, but not with CVXOPT (whose
        matrix constructor accepts a list of columns). In reality, ``L``
        can be any iterable type of the correct length; however, you
        should be extremely wary of the way we interpret anything other
        than a list of rows.

    K : dunshire.cones.SymmetricCone
        The symmetric cone instance over which the game is played.

    e1 : iterable float
        The interior point of ``K`` belonging to player one; it
        can be of any iterable type having the correct length.

    e2 : iterable float
        The interior point of ``K`` belonging to player two; it
        can be of any enumerable type having the correct length.

    Raises
    ------

    ValueError
        If either ``e1`` or ``e2`` lie outside of the cone ``K``.

    Examples
    --------

        >>> from dunshire import *
        >>> K = NonnegativeOrthant(3)
        >>> L = [[1,-5,-15],[-1,2,-3],[-12,-15,1]]
        >>> e1 = [1,1,1]
        >>> e2 = [1,2,3]
        >>> SLG = SymmetricLinearGame(L, K, e1, e2)
        >>> print(SLG)
        The linear game (L, K, e1, e2) where
          L = [  1  -5 -15]
              [ -1   2  -3]
              [-12 -15   1],
          K = Nonnegative orthant in the real 3-space,
          e1 = [ 1]
               [ 1]
               [ 1],
          e2 = [ 1]
               [ 2]
               [ 3]

    Lists can (and probably should) be used for every argument::

        >>> from dunshire import *
        >>> K = NonnegativeOrthant(2)
        >>> L = [[1,0],[0,1]]
        >>> e1 = [1,1]
        >>> e2 = [1,1]
        >>> G = SymmetricLinearGame(L, K, e1, e2)
        >>> print(G)
        The linear game (L, K, e1, e2) where
          L = [ 1  0]
              [ 0  1],
          K = Nonnegative orthant in the real 2-space,
          e1 = [ 1]
               [ 1],
          e2 = [ 1]
               [ 1]

    The points ``e1`` and ``e2`` can also be passed as some other
    enumerable type (of the correct length) without much harm, since
    there is no row/column ambiguity::

        >>> import cvxopt
        >>> import numpy
        >>> from dunshire import *
        >>> K = NonnegativeOrthant(2)
        >>> L = [[1,0],[0,1]]
        >>> e1 = cvxopt.matrix([1,1])
        >>> e2 = numpy.matrix([1,1])
        >>> G = SymmetricLinearGame(L, K, e1, e2)
        >>> print(G)
        The linear game (L, K, e1, e2) where
          L = [ 1  0]
              [ 0  1],
          K = Nonnegative orthant in the real 2-space,
          e1 = [ 1]
               [ 1],
          e2 = [ 1]
               [ 1]

    However, ``L`` will always be intepreted as a list of rows, even
    if it is passed as a :class:`cvxopt.base.matrix` which is
    otherwise indexed by columns::

        >>> import cvxopt
        >>> from dunshire import *
        >>> K = NonnegativeOrthant(2)
        >>> L = [[1,2],[3,4]]
        >>> e1 = [1,1]
        >>> e2 = e1
        >>> G = SymmetricLinearGame(L, K, e1, e2)
        >>> print(G)
        The linear game (L, K, e1, e2) where
          L = [ 1  2]
              [ 3  4],
          K = Nonnegative orthant in the real 2-space,
          e1 = [ 1]
               [ 1],
          e2 = [ 1]
               [ 1]
        >>> L = cvxopt.matrix(L)
        >>> print(L)
        [ 1  3]
        [ 2  4]
        <BLANKLINE>
        >>> G = SymmetricLinearGame(L, K, e1, e2)
        >>> print(G)
        The linear game (L, K, e1, e2) where
          L = [ 1  2]
              [ 3  4],
          K = Nonnegative orthant in the real 2-space,
          e1 = [ 1]
               [ 1],
          e2 = [ 1]
               [ 1]

    """
    def __init__(self, L, K, e1, e2):
        """
        Create a new SymmetricLinearGame object.
        """
        self._K = K
        self._e1 = matrix(e1, (K.dimension(), 1))
        self._e2 = matrix(e2, (K.dimension(), 1))

        # Our input ``L`` is indexed by rows but CVXOPT matrices are
        # indexed by columns, so we need to transpose the input before
        # feeding it to CVXOPT.
        self._L = matrix(L, (K.dimension(), K.dimension())).trans()

        if not self._e1 in K:
            raise ValueError('the point e1 must lie in the interior of K')

        if not self._e2 in K:
            raise ValueError('the point e2 must lie in the interior of K')

        # Initial value of cached method.
        self._L_specnorm_value = None


    def __str__(self):
        """
        Return a string representation of this game.
        """
        tpl = 'The linear game (L, K, e1, e2) where\n' \
              '  L = {:s},\n' \
              '  K = {!s},\n' \
              '  e1 = {:s},\n' \
              '  e2 = {:s}'
        indented_L = '\n      '.join(str(self.L()).splitlines())
        indented_e1 = '\n       '.join(str(self.e1()).splitlines())
        indented_e2 = '\n       '.join(str(self.e2()).splitlines())

        return tpl.format(indented_L,
                          str(self.K()),
                          indented_e1,
                          indented_e2)


    def L(self):
        """
        Return the matrix ``L`` passed to the constructor.

        Returns
        -------

        matrix
            The matrix that defines this game's :meth:`payoff` operator.

        Examples
        --------

            >>> from dunshire import *
            >>> K = NonnegativeOrthant(3)
            >>> L = [[1,-5,-15],[-1,2,-3],[-12,-15,1]]
            >>> e1 = [1,1,1]
            >>> e2 = [1,2,3]
            >>> SLG = SymmetricLinearGame(L, K, e1, e2)
            >>> print(SLG.L())
            [  1  -5 -15]
            [ -1   2  -3]
            [-12 -15   1]
            <BLANKLINE>

        """
        return self._L


    def K(self):
        """
        Return the cone over which this game is played.

        Returns
        -------

        SymmetricCone
            The :class:`SymmetricCone` over which this game is played.

        Examples
        --------

            >>> from dunshire import *
            >>> K = NonnegativeOrthant(3)
            >>> L = [[1,-5,-15],[-1,2,-3],[-12,-15,1]]
            >>> e1 = [1,1,1]
            >>> e2 = [1,2,3]
            >>> SLG = SymmetricLinearGame(L, K, e1, e2)
            >>> print(SLG.K())
            Nonnegative orthant in the real 3-space

        """
        return self._K


    def e1(self):
        """
        Return player one's interior point.

        Returns
        -------

        matrix
            The point interior to :meth:`K` affiliated with player one.

        Examples
        --------

            >>> from dunshire import *
            >>> K = NonnegativeOrthant(3)
            >>> L = [[1,-5,-15],[-1,2,-3],[-12,-15,1]]
            >>> e1 = [1,1,1]
            >>> e2 = [1,2,3]
            >>> SLG = SymmetricLinearGame(L, K, e1, e2)
            >>> print(SLG.e1())
            [ 1]
            [ 1]
            [ 1]
            <BLANKLINE>

        """
        return self._e1


    def e2(self):
        """
        Return player two's interior point.

        Returns
        -------

        matrix
            The point interior to :meth:`K` affiliated with player one.

        Examples
        --------

            >>> from dunshire import *
            >>> K = NonnegativeOrthant(3)
            >>> L = [[1,-5,-15],[-1,2,-3],[-12,-15,1]]
            >>> e1 = [1,1,1]
            >>> e2 = [1,2,3]
            >>> SLG = SymmetricLinearGame(L, K, e1, e2)
            >>> print(SLG.e2())
            [ 1]
            [ 2]
            [ 3]
            <BLANKLINE>

        """
        return self._e2


    def payoff(self, strategy1, strategy2):
        r"""
        Return the payoff associated with ``strategy1`` and ``strategy2``.

        The payoff operator takes pairs of strategies to a real
        number. For example, if player one's strategy is :math:`x` and
        player two's strategy is :math:`y`, then the associated payoff
        is :math:`\left\langle L\left(x\right),y \right\rangle \in
        \mathbb{R}`. Here, :math:`L` denotes the same linear operator as
        :meth:`L`. This method computes the payoff given the two
        players' strategies.

        Parameters
        ----------

        strategy1 : matrix
            Player one's strategy.

        strategy2 : matrix
            Player two's strategy.

        Returns
        -------

        float
            The payoff for the game when player one plays ``strategy1``
            and player two plays ``strategy2``.

        Examples
        --------

        The value of the game should be the payoff at the optimal
        strategies::

            >>> from dunshire import *
            >>> K = NonnegativeOrthant(3)
            >>> L = [[1,-5,-15],[-1,2,-3],[-12,-15,1]]
            >>> e1 = [1,1,1]
            >>> e2 = [1,1,1]
            >>> SLG = SymmetricLinearGame(L, K, e1, e2)
            >>> soln = SLG.solution()
            >>> x_bar = soln.player1_optimal()
            >>> y_bar = soln.player2_optimal()
            >>> SLG.payoff(x_bar, y_bar) == soln.game_value()
            True

        """
        return inner_product(self.L()*strategy1, strategy2)


    def dimension(self):
        """
        Return the dimension of this game.

        The dimension of a game is not needed for the theory, but it is
        useful for the implementation. We define the dimension of a game
        to be the dimension of its underlying cone. Or what is the same,
        the dimension of the space from which the strategies are chosen.

        Returns
        -------

        int
            The dimension of the cone :meth:`K`, or of the space where
            this game is played.

        Examples
        --------

        The dimension of a game over the nonnegative quadrant in the
        plane should be two (the dimension of the plane)::

            >>> from dunshire import *
            >>> K = NonnegativeOrthant(2)
            >>> L = [[1,-5],[-1,2]]
            >>> e1 = [1,1]
            >>> e2 = [1,4]
            >>> SLG = SymmetricLinearGame(L, K, e1, e2)
            >>> SLG.dimension()
            2

        """
        return self.K().dimension()


    def _zero(self):
        """
        Return a column of zeros that fits ``K``.

        This is used in our CVXOPT construction.

        .. warning::

            It is not safe to cache any of the matrices passed to
            CVXOPT, because it can clobber them.

        Returns
        -------

        matrix
            A ``self.dimension()``-by-``1`` column vector of zeros.

        Examples
        --------

            >>> from dunshire import *
            >>> K = NonnegativeOrthant(3)
            >>> L = identity(3)
            >>> e1 = [1,1,1]
            >>> e2 = e1
            >>> SLG = SymmetricLinearGame(L, K, e1, e2)
            >>> print(SLG._zero())
            [0.0000000]
            [0.0000000]
            [0.0000000]
            <BLANKLINE>

        """
        return matrix(0, (self.dimension(), 1), tc='d')


    def A(self):
        r"""
        Return the matrix ``A`` used in our CVXOPT construction.

        This matrix :math:`A` appears on the right-hand side of
        :math:`Ax = b` in the `statement of the CVXOPT conelp program
        <http://cvxopt.org/userguide/coneprog.html#linear-cone-programs>`_.

        .. warning::

            It is not safe to cache any of the matrices passed to
            CVXOPT, because it can clobber them.

        Returns
        -------

        matrix
            A ``1``-by-``(1 + self.dimension())`` row vector. Its first
            entry is zero, and the rest are the entries of :meth:`e2`.

        Examples
        --------

            >>> from dunshire import *
            >>> K = NonnegativeOrthant(3)
            >>> L = [[1,1,1],[1,1,1],[1,1,1]]
            >>> e1 = [1,1,1]
            >>> e2 = [1,2,3]
            >>> SLG = SymmetricLinearGame(L, K, e1, e2)
            >>> print(SLG.A())
            [0.0000000 1.0000000 2.0000000 3.0000000]
            <BLANKLINE>

        """
        return matrix([0, self.e2()], (1, self.dimension() + 1), 'd')



    def G(self):
        r"""
        Return the matrix ``G`` used in our CVXOPT construction.

        Thus matrix :math:`G` appears on the left-hand side of :math:`Gx
        + s = h` in the `statement of the CVXOPT conelp program
        <http://cvxopt.org/userguide/coneprog.html#linear-cone-programs>`_.

        .. warning::

            It is not safe to cache any of the matrices passed to
            CVXOPT, because it can clobber them.

        Returns
        -------

        matrix
            A ``2*self.dimension()``-by-``(1 + self.dimension())`` matrix.

        Examples
        --------

            >>> from dunshire import *
            >>> K = NonnegativeOrthant(3)
            >>> L = [[4,5,6],[7,8,9],[10,11,12]]
            >>> e1 = [1,2,3]
            >>> e2 = [1,1,1]
            >>> SLG = SymmetricLinearGame(L, K, e1, e2)
            >>> print(SLG.G())
            [  0.0000000  -1.0000000   0.0000000   0.0000000]
            [  0.0000000   0.0000000  -1.0000000   0.0000000]
            [  0.0000000   0.0000000   0.0000000  -1.0000000]
            [  1.0000000  -4.0000000  -5.0000000  -6.0000000]
            [  2.0000000  -7.0000000  -8.0000000  -9.0000000]
            [  3.0000000 -10.0000000 -11.0000000 -12.0000000]
            <BLANKLINE>

        """
        identity_matrix = identity(self.dimension())
        return append_row(append_col(self._zero(), -identity_matrix),
                          append_col(self.e1(), -self.L()))


    def c(self):
        r"""
        Return the vector ``c`` used in our CVXOPT construction.

        The column vector :math:`c` appears in the objective function
        value :math:`\left\langle c,x \right\rangle` in the `statement
        of the CVXOPT conelp program
        <http://cvxopt.org/userguide/coneprog.html#linear-cone-programs>`_.

        .. warning::

            It is not safe to cache any of the matrices passed to
            CVXOPT, because it can clobber them.

        Returns
        -------

        matrix
            A :meth:`dimension`-by-``1`` column vector.

        Examples
        --------

            >>> from dunshire import *
            >>> K = NonnegativeOrthant(3)
            >>> L = [[4,5,6],[7,8,9],[10,11,12]]
            >>> e1 = [1,2,3]
            >>> e2 = [1,1,1]
            >>> SLG = SymmetricLinearGame(L, K, e1, e2)
            >>> print(SLG.c())
            [-1.0000000]
            [ 0.0000000]
            [ 0.0000000]
            [ 0.0000000]
            <BLANKLINE>

        """
        return matrix([-1, self._zero()])


    def C(self):
        """
        Return the cone ``C`` used in our CVXOPT construction.

        This is the cone over which the `CVXOPT conelp program
        <http://cvxopt.org/userguide/coneprog.html#linear-cone-programs>`_
        takes place.

        Returns
        -------

        CartesianProduct
            The cartesian product of ``K`` with itself.

        Examples
        --------

            >>> from dunshire import *
            >>> K = NonnegativeOrthant(3)
            >>> L = [[4,5,6],[7,8,9],[10,11,12]]
            >>> e1 = [1,2,3]
            >>> e2 = [1,1,1]
            >>> SLG = SymmetricLinearGame(L, K, e1, e2)
            >>> print(SLG.C())
            Cartesian product of dimension 6 with 2 factors:
              * Nonnegative orthant in the real 3-space
              * Nonnegative orthant in the real 3-space

        """
        return CartesianProduct(self._K, self._K)

    def h(self):
        r"""
        Return the ``h`` vector used in our CVXOPT construction.

        The :math:`h` vector appears on the right-hand side of :math:`Gx
        + s = h` in the `statement of the CVXOPT conelp program
        <http://cvxopt.org/userguide/coneprog.html#linear-cone-programs>`_.

        .. warning::

            It is not safe to cache any of the matrices passed to
            CVXOPT, because it can clobber them.

        Returns
        -------

        matrix
            A ``2*self.dimension()``-by-``1`` column vector of zeros.

        Examples
        --------

            >>> from dunshire import *
            >>> K = NonnegativeOrthant(3)
            >>> L = [[4,5,6],[7,8,9],[10,11,12]]
            >>> e1 = [1,2,3]
            >>> e2 = [1,1,1]
            >>> SLG = SymmetricLinearGame(L, K, e1, e2)
            >>> print(SLG.h())
            [0.0000000]
            [0.0000000]
            [0.0000000]
            [0.0000000]
            [0.0000000]
            [0.0000000]
            <BLANKLINE>

        """

        return matrix([self._zero(), self._zero()])


    @staticmethod
    def b():
        r"""
        Return the ``b`` vector used in our CVXOPT construction.

        The vector :math:`b` appears on the right-hand side of :math:`Ax
        = b` in the `statement of the CVXOPT conelp program
        <http://cvxopt.org/userguide/coneprog.html#linear-cone-programs>`_.

        This method is static because the dimensions and entries of
        ``b`` are known beforehand, and don't depend on any other
        properties of the game.

        .. warning::

            It is not safe to cache any of the matrices passed to
            CVXOPT, because it can clobber them.

        Returns
        -------

        matrix
            A ``1``-by-``1`` matrix containing a single entry ``1``.

        Examples
        --------

            >>> from dunshire import *
            >>> K = NonnegativeOrthant(3)
            >>> L = [[4,5,6],[7,8,9],[10,11,12]]
            >>> e1 = [1,2,3]
            >>> e2 = [1,1,1]
            >>> SLG = SymmetricLinearGame(L, K, e1, e2)
            >>> print(SLG.b())
            [1.0000000]
            <BLANKLINE>

        """
        return matrix([1], tc='d')


    def player1_start(self):
        """
        Return a feasible starting point for player one.

        This starting point is for the CVXOPT formulation and not for
        the original game. The basic premise is that if you scale
        :meth:`e2` by the reciprocal of its squared norm, then you get a
        point in :meth:`K` that makes a unit inner product with
        :meth:`e2`. We then get to choose the primal objective function
        value such that the constraint involving :meth:`L` is satisfied.

        Returns
        -------

        dict
            A dictionary with two keys, ``'x'`` and ``'s'``, which
            contain the vectors of the same name in the CVXOPT primal
            problem formulation.

            The vector ``x`` consists of the primal objective function
            value concatenated with the strategy (for player one) that
            achieves it. The vector ``s`` is essentially a dummy
            variable, and is computed from the equality constraing in
            the CVXOPT primal problem.

        """
        p = self.e2() / (norm(self.e2()) ** 2)
        dist = self.K().ball_radius(self.e1())
        nu = - self._L_specnorm()/(dist*norm(self.e2()))
        x = matrix([nu, p], (self.dimension() + 1, 1))
        s = - self.G()*x

        return {'x': x, 's': s}


    def player2_start(self):
        """
        Return a feasible starting point for player two.

        This starting point is for the CVXOPT formulation and not for
        the original game. The basic premise is that if you scale
        :meth:`e1` by the reciprocal of its squared norm, then you get a
        point in :meth:`K` that makes a unit inner product with
        :meth:`e1`. We then get to choose the dual objective function
        value such that the constraint involving :meth:`L` is satisfied.

        Returns
        -------

        dict
            A dictionary with two keys, ``'y'`` and ``'z'``, which
            contain the vectors of the same name in the CVXOPT dual
            problem formulation.

            The ``1``-by-``1`` vector ``y`` consists of the dual
            objective function value. The last :meth:`dimension` entries
            of the vector ``z`` contain the strategy (for player two)
            that achieves it. The remaining entries of ``z`` are
            essentially dummy variables, computed from the equality
            constraint in the CVXOPT dual problem.

        """
        q = self.e1() / (norm(self.e1()) ** 2)
        dist = self.K().ball_radius(self.e2())
        omega = self._L_specnorm()/(dist*norm(self.e1()))
        y = matrix([omega])
        z2 = q
        z1 = y*self.e2() - self.L().trans()*z2
        z = matrix([z1, z2], (self.dimension()*2, 1))

        return {'y': y, 'z': z}


    def _L_specnorm(self):
        """
        Compute the spectral norm of :meth:`L` and cache it.

        The spectral norm of the matrix :meth:`L` is used in a few
        places. Since it can be expensive to compute, we want to cache
        its value. That is not possible in :func:`specnorm`, which lies
        outside of a class, so this is the place to do it.

        Returns
        -------

        float
            A nonnegative real number; the largest singular value of
            the matrix :meth:`L`.

        Examples
        --------

            >>> from dunshire import *
            >>> from dunshire.matrices import specnorm
            >>> L = [[1,2],[3,4]]
            >>> K = NonnegativeOrthant(2)
            >>> e1 = [1,1]
            >>> e2 = e1
            >>> SLG = SymmetricLinearGame(L,K,e1,e2)
            >>> specnorm(SLG.L()) == SLG._L_specnorm()
            True

        """
        if self._L_specnorm_value is None:
            self._L_specnorm_value = specnorm(self.L())
        return self._L_specnorm_value


    def tolerance_scale(self, solution):
        r"""

        Return a scaling factor that should be applied to
        :const:`dunshire.options.ABS_TOL` for this game.

        When performing certain comparisons, the default tolerance
        :const:`dunshire.options.ABS_TOL` may not be appropriate. For
        example, if we expect ``x`` and ``y`` to be within
        :const:`dunshire.options.ABS_TOL` of each other, than the inner
        product of ``L*x`` and ``y`` can be as far apart as the spectral
        norm of ``L`` times the sum of the norms of ``x`` and
        ``y``. Such a comparison is made in :meth:`solution`, and in
        many of our unit tests.

        The returned scaling factor found from the inner product
        mentioned above is

        .. math::

            \left\lVert L \right\rVert_{2}
            \left( \left\lVert \bar{x} \right\rVert
                   + \left\lVert \bar{y} \right\rVert
            \right),

        where :math:`\bar{x}` and :math:`\bar{y}` are optimal solutions
        for players one and two respectively. This scaling factor is not
        formally justified, but attempting anything smaller leads to
        test failures.

        .. warning::

            Optimal solutions are not unique, so the scaling factor
            obtained from ``solution`` may not work when comparing other
            solutions.

        Parameters
        ----------

        solution : Solution
            A solution of this game, used to obtain the norms of the
            optimal strategies.

        Returns
        -------

        float
            A scaling factor to be multiplied by
            :const:`dunshire.options.ABS_TOL` when
            making comparisons involving solutions of this game.

        Examples
        --------

        The spectral norm of ``L`` in this case is around ``5.464``, and
        the optimal strategies both have norm one, so we expect the
        tolerance scale to be somewhere around ``2 * 5.464``, or
        ``10.929``::

            >>> from dunshire import *
            >>> L = [[1,2],[3,4]]
            >>> K = NonnegativeOrthant(2)
            >>> e1 = [1,1]
            >>> e2 = e1
            >>> SLG = SymmetricLinearGame(L,K,e1,e2)
            >>> SLG.tolerance_scale(SLG.solution())
            10.929...

        """
        norm_p1_opt = norm(solution.player1_optimal())
        norm_p2_opt = norm(solution.player2_optimal())
        scale = self._L_specnorm()*(norm_p1_opt + norm_p2_opt)

        # Don't return anything smaller than 1... we can't go below
        # out "minimum tolerance."
        return max(1, scale)


    def solution(self):
        """
        Solve this linear game and return a :class:`Solution`.

        Returns
        -------

        Solution
            A :class:`Solution` object describing the game's value and
            the optimal strategies of both players.

        Raises
        ------
        GameUnsolvableException
            If the game could not be solved (if an optimal solution to its
            associated cone program was not found).

        PoorScalingException
            If the game could not be solved because CVXOPT crashed while
            trying to take the square root of a negative number.

        Examples
        --------

        This example is computed in Gowda and Ravindran in the section
        "The value of a Z-transformation"::

            >>> from dunshire import *
            >>> K = NonnegativeOrthant(3)
            >>> L = [[1,-5,-15],[-1,2,-3],[-12,-15,1]]
            >>> e1 = [1,1,1]
            >>> e2 = [1,1,1]
            >>> SLG = SymmetricLinearGame(L, K, e1, e2)
            >>> print(SLG.solution())
            Game value: -6.172...
            Player 1 optimal:
              [0.551...]
              [0.000...]
              [0.448...]
            Player 2 optimal:
              [0.448...]
              [0.000...]
              [0.551...]

        The value of the following game can be computed using the fact
        that the identity is invertible::

            >>> from dunshire import *
            >>> K = NonnegativeOrthant(3)
            >>> L = [[1,0,0],[0,1,0],[0,0,1]]
            >>> e1 = [1,2,3]
            >>> e2 = [4,5,6]
            >>> SLG = SymmetricLinearGame(L, K, e1, e2)
            >>> print(SLG.solution())
            Game value: 0.031...
            Player 1 optimal:
              [0.031...]
              [0.062...]
              [0.093...]
            Player 2 optimal:
              [0.125...]
              [0.156...]
              [0.187...]

        This is another Gowda/Ravindran example that is supposed to have
        a negative game value::

            >>> from dunshire import *
            >>> from dunshire.options import ABS_TOL
            >>> L = [[1, -2], [-2, 1]]
            >>> K = NonnegativeOrthant(2)
            >>> e1 = [1, 1]
            >>> e2 = e1
            >>> SLG = SymmetricLinearGame(L, K, e1, e2)
            >>> SLG.solution().game_value() < -ABS_TOL
            True

        The following two games are problematic numerically, but we
        should be able to solve them::

            >>> from dunshire import *
            >>> L = [[-0.95237953890954685221, 1.83474556206462535712],
            ...      [ 1.30481749924621448500, 1.65278664543326403447]]
            >>> K = NonnegativeOrthant(2)
            >>> e1 = [0.95477167524644313001, 0.63270781756540095397]
            >>> e2 = [0.39633793037154141370, 0.10239281495640320530]
            >>> SLG = SymmetricLinearGame(L, K, e1, e2)
            >>> print(SLG.solution())
            Game value: 18.767...
            Player 1 optimal:
              [0.000...]
              [9.766...]
            Player 2 optimal:
              [1.047...]
              [0.000...]

        ::

            >>> from dunshire import *
            >>> L = [[1.54159395026049472754, 2.21344728574316684799],
            ...      [1.33147433507846657541, 1.17913616272988108769]]
            >>> K = NonnegativeOrthant(2)
            >>> e1 = [0.39903040089404784307, 0.12377403622479113410]
            >>> e2 = [0.15695181142215544612, 0.85527381344651265405]
            >>> SLG = SymmetricLinearGame(L, K, e1, e2)
            >>> print(SLG.solution())
            Game value: 24.614...
            Player 1 optimal:
              [6.371...]
              [0.000...]
            Player 2 optimal:
              [2.506...]
              [0.000...]

        This is another one that was difficult numerically, and caused
        trouble even after we fixed the first two::

            >>> from dunshire import *
            >>> L = [[57.22233908627052301199, 41.70631373437460354126],
            ...      [83.04512571985074487202, 57.82581810406928468637]]
            >>> K = NonnegativeOrthant(2)
            >>> e1 = [7.31887017043399268346, 0.89744171905822367474]
            >>> e2 = [0.11099824781179848388, 6.12564670639315345113]
            >>> SLG = SymmetricLinearGame(L,K,e1,e2)
            >>> print(SLG.solution())
            Game value: 70.437...
            Player 1 optimal:
              [9.009...]
              [0.000...]
            Player 2 optimal:
              [0.136...]
              [0.000...]

        And finally, here's one that returns an "optimal" solution, but
        whose primal/dual objective function values are far apart::

            >>> from dunshire import *
            >>> L = [[ 6.49260076597376212248, -0.60528030227678542019],
            ...      [ 2.59896077096751731972, -0.97685530240286766457]]
            >>> K = IceCream(2)
            >>> e1 = [1, 0.43749513972645248661]
            >>> e2 = [1, 0.46008379832200291260]
            >>> SLG = SymmetricLinearGame(L, K, e1, e2)
            >>> print(SLG.solution())
            Game value: 11.596...
            Player 1 optimal:
              [ 1.852...]
              [-1.852...]
            Player 2 optimal:
              [ 1.777...]
              [-1.777...]

        """
        try:
            opts = {'show_progress': False}
            soln_dict = solvers.conelp(self.c(),
                                       self.G(),
                                       self.h(),
                                       self.C().cvxopt_dims(),
                                       self.A(),
                                       self.b(),
                                       primalstart=self.player1_start(),
                                       dualstart=self.player2_start(),
                                       options=opts)
        except ValueError as error:
            if str(error) == 'math domain error':
                # Oops, CVXOPT tried to take the square root of a
                # negative number. Report some details about the game
                # rather than just the underlying CVXOPT crash.
                printing.options['dformat'] = DEBUG_FLOAT_FORMAT
                raise PoorScalingException(self)
            else:
                raise error

        # The optimal strategies are named ``p`` and ``q`` in the
        # background documentation, and we need to extract them from
        # the CVXOPT ``x`` and ``z`` variables. The objective values
        # :math:`nu` and :math:`omega` can also be found in the CVXOPT
        # ``x`` and ``y`` variables; however, they're stored
        # conveniently as separate entries in the solution dictionary.
        p1_value = -soln_dict['primal objective']
        p2_value = -soln_dict['dual objective']
        p1_optimal = soln_dict['x'][1:]
        p2_optimal = soln_dict['z'][self.dimension():]

        # The "status" field contains "optimal" if everything went
        # according to plan. Other possible values are "primal
        # infeasible", "dual infeasible", "unknown", all of which mean
        # we didn't get a solution.
        #
        # The "infeasible" ones are the worst, since they indicate
        # that CVXOPT is convinced the problem is infeasible (and that
        # cannot happen).
        if soln_dict['status'] in ['primal infeasible', 'dual infeasible']:
            printing.options['dformat'] = DEBUG_FLOAT_FORMAT
            raise GameUnsolvableException(self, soln_dict)

        # For the game value, we could use any of:
        #
        #   * p1_value
        #   * p2_value
        #   * (p1_value + p2_value)/2
        #   * the game payoff
        #
        # We want the game value to be the payoff, however, so it
        # makes the most sense to just use that, even if it means we
        # can't test the fact that p1_value/p2_value are close to the
        # payoff.
        payoff = self.payoff(p1_optimal, p2_optimal)
        soln = Solution(payoff, p1_optimal, p2_optimal)

        # The "optimal" and "unknown" results, we actually treat the
        # same. Even if CVXOPT bails out due to numerical difficulty,
        # it will have some candidate points in mind. If those
        # candidates are good enough, we take them. We do the same
        # check for "optimal" results.
        #
        # First we check that the primal/dual objective values are
        # close enough because otherwise CVXOPT might return "unknown"
        # and give us two points in the cone that are nowhere near
        # optimal. And in fact, we need to ensure that they're close
        # for "optimal" results, too, because we need to know how
        # lenient to be in our testing.
        #
        if abs(p1_value - p2_value) > self.tolerance_scale(soln)*ABS_TOL:
            printing.options['dformat'] = DEBUG_FLOAT_FORMAT
            raise GameUnsolvableException(self, soln_dict)

        # And we also check that the points it gave us belong to the
        # cone, just in case...
        if (p1_optimal not in self._K) or (p2_optimal not in self._K):
            printing.options['dformat'] = DEBUG_FLOAT_FORMAT
            raise GameUnsolvableException(self, soln_dict)

        return soln


    def condition(self):
        r"""
        Return the condition number of this game.

        In the CVXOPT construction of this game, two matrices ``G`` and
        ``A`` appear. When those matrices are nasty, numerical problems
        can show up. We define the condition number of this game to be
        the average of the condition numbers of ``G`` and ``A`` in the
        CVXOPT construction. If the condition number of this game is
        high, you can problems like :class:`PoorScalingException`.

        Random testing shows that a condition number of around ``125``
        is about the best that we can solve reliably. However, the
        failures are intermittent, and you may get lucky with an
        ill-conditioned game.

        Returns
        -------

        float
            A real number greater than or equal to one that measures how
            bad this game is numerically.

        Examples
        --------

        >>> from dunshire import *
        >>> K = NonnegativeOrthant(1)
        >>> L = [[1]]
        >>> e1 = [1]
        >>> e2 = e1
        >>> SLG = SymmetricLinearGame(L, K, e1, e2)
        >>> SLG.condition()
        1.809...

        """
        return (condition_number(self.G()) + condition_number(self.A()))/2


    def dual(self):
        r"""
        Return the dual game to this game.

        If :math:`G = \left(L,K,e_{1},e_{2}\right)` is a linear game,
        then its dual is :math:`G^{*} =
        \left(L^{*},K^{*},e_{2},e_{1}\right)`. However, since this cone
        is symmetric, :math:`K^{*} = K`.

        Examples
        --------

            >>> from dunshire import *
            >>> K = NonnegativeOrthant(3)
            >>> L = [[1,-5,-15],[-1,2,-3],[-12,-15,1]]
            >>> e1 = [1,1,1]
            >>> e2 = [1,2,3]
            >>> SLG = SymmetricLinearGame(L, K, e1, e2)
            >>> print(SLG.dual())
            The linear game (L, K, e1, e2) where
              L = [  1  -1 -12]
                  [ -5   2 -15]
                  [-15  -3   1],
              K = Nonnegative orthant in the real 3-space,
              e1 = [ 1]
                   [ 2]
                   [ 3],
              e2 = [ 1]
                   [ 1]
                   [ 1]

        """
        # We pass ``self.L()`` right back into the constructor, because
        # it will be transposed there. And keep in mind that ``self._K``
        # is its own dual.
        return SymmetricLinearGame(self.L(),
                                   self.K(),
                                   self.e2(),
                                   self.e1())
