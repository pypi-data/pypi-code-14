"""
Class definitions for all of the symmetric cones (and their superclass,
:class:`SymmetricCone`) supported by CVXOPT.
"""

from cvxopt import matrix

from .matrices import eigenvalues, norm
from . import options

class SymmetricCone:
    """
    An instance of a symmetric (self-dual and homogeneous) cone.

    There are three types of symmetric cones supported by CVXOPT:

      1. The nonnegative orthant in the real n-space.
      2. The Lorentz "ice cream" cone, or the second-order cone.
      3. The cone of symmetric positive-semidefinite matrices.

    This class is intended to encompass them all.

    When constructing a single symmetric cone (i.e. not a
    :class:`CartesianProduct` of them), the only information that we
    need is its dimension. We take that dimension as a parameter, and
    store it for later.

    Parameters
    ----------

    dimension : int
        The dimension of this cone.

    Raises
    ------

    ValueError
        If you try to create a cone with dimension zero or less.

    """
    def __init__(self, dimension):
        """
        A generic constructor for symmetric cones.
        """
        if dimension <= 0:
            raise ValueError('cones must have dimension greater than zero')

        self._dimension = dimension


    def __contains__(self, point):
        """
        Return whether or not ``point`` belongs to this cone.

        Parameters
        ----------

        point : matrix
            The point to test for membership in this cone.

        Raises
        ------

        NotImplementedError
            Always, this method must be implemented in subclasses.

        Examples
        --------

            >>> K = SymmetricCone(5)
            >>> matrix([1,2]) in K
            Traceback (most recent call last):
            ...
            NotImplementedError

        """
        raise NotImplementedError


    def ball_radius(self, point):
        """
        Return the radius of a ball around ``point`` in this cone.

        Since a radius cannot be negative, the ``point`` must be
        contained in this cone; otherwise, an error is raised.

        Parameters
        ----------

        point : matrix
            A point contained in this cone.

        Returns
        -------

        float
            A radius ``r`` such that the ball of radius ``r`` centered at
            ``point`` is contained entirely within this cone.

        Raises
        ------

        NotImplementedError
            Always, this method must be implemented in subclasses.

        Examples
        --------

            >>> K = SymmetricCone(5)
            >>> K.ball_radius(matrix([1,1,1,1,1]))
            Traceback (most recent call last):
            ...
            NotImplementedError

        """
        raise NotImplementedError


    def dimension(self):
        """
        Return the dimension of this symmetric cone.

        The dimension of this symmetric cone is recorded during its
        creation. This method simply returns the recorded value, and
        should not need to be overridden in subclasses. We prefer to do
        any special computation in ``__init__()`` and record the result
        in ``self._dimension``.

        Returns
        -------

        int
            The stored dimension (from when this cone was constructed)
            of this cone.

        Examples
        --------

            >>> K = SymmetricCone(5)
            >>> K.dimension()
            5

        """
        return self._dimension


class NonnegativeOrthant(SymmetricCone):
    """
    The nonnegative orthant in the given number of dimensions.

    Examples
    --------

        >>> K = NonnegativeOrthant(3)
        >>> print(K)
        Nonnegative orthant in the real 3-space

    """
    def __str__(self):
        """
        Output a human-readable description of myself.
        """
        tpl = 'Nonnegative orthant in the real {:d}-space'
        return tpl.format(self.dimension())


    def __contains__(self, point):
        """
        Return whether or not ``point`` belongs to this cone.

        Since this test is expected to work on points whose components
        are floating point numbers, it doesn't make any sense to
        distinguish between strict and non-strict containment -- the
        test uses a tolerance parameter.

        Parameters
        ----------

        point : matrix
            A :class:`cvxopt.base.matrix` having dimensions ``(n,1)``
            where ``n`` is the :meth:`dimension` of this cone.

        Returns
        -------

        bool

           ``True`` if ``point`` belongs to this cone, ``False`` otherwise.

        Raises
        ------

        TypeError
            If ``point`` is not a :class:`cvxopt.base.matrix`.

        TypeError
            If ``point`` has the wrong dimensions.

        Examples
        --------

        All of these coordinates are positive enough:

            >>> K = NonnegativeOrthant(3)
            >>> matrix([1,2,3]) in K
            True

        The one negative coordinate pushes this point outside of ``K``:

            >>> K = NonnegativeOrthant(3)
            >>> matrix([1,-0.1,3]) in K
            False

        A boundary point is considered inside of ``K``:
            >>> K = NonnegativeOrthant(3)
            >>> matrix([1,0,3]) in K
            True

        Junk arguments don't work:

            >>> K = NonnegativeOrthant(3)
            >>> [1,2,3] in K
            Traceback (most recent call last):
            ...
            TypeError: the given point is not a cvxopt.base.matrix

            >>> K = NonnegativeOrthant(3)
            >>> matrix([1,2]) in K
            Traceback (most recent call last):
            ...
            TypeError: the given point has the wrong dimensions

        """
        if not isinstance(point, matrix):
            raise TypeError('the given point is not a cvxopt.base.matrix')
        if not point.size == (self.dimension(), 1):
            raise TypeError('the given point has the wrong dimensions')

        return all([x > -options.ABS_TOL for x in point])


    def ball_radius(self, point):
        """
        Return the radius of a ball around ``point`` in this cone.

        Since a radius cannot be negative, the ``point`` must be
        contained in this cone; otherwise, an error is raised.

        The minimum distance from ``point`` to the complement of this
        cone will always occur at its projection onto that set. It is
        not hard to see that the projection is directly along one of the
        coordinates, and so the minimum distance from ``point`` to the
        boundary of this cone is the smallest coordinate of
        ``point``. Therefore any radius less than that will work; we
        divide it in half somewhat arbitrarily.

        Parameters
        ----------

        point : matrix
            A point contained in this cone.

        Returns
        -------

        float
            A radius ``r`` such that the ball of radius ``r`` centered at
            ``point`` is contained entirely within this cone.

        Raises
        ------

        TypeError
            If ``point`` is not a :class:`cvxopt.base.matrix`.

        TypeError
            If ``point`` has the wrong dimensions.

        ValueError
            if ``point`` is not contained in this cone.

        Examples
        --------

            >>> K = NonnegativeOrthant(5)
            >>> K.ball_radius(matrix([1,2,3,4,5]))
            0.5

        """
        if not isinstance(point, matrix):
            raise TypeError('the given point is not a cvxopt.base.matrix')
        if not point.size == (self.dimension(), 1):
            raise TypeError('the given point has the wrong dimensions')
        if not point in self:
            raise ValueError('the given point does not lie in the cone')

        return min(list(point)) / 2.0



class IceCream(SymmetricCone):
    """
    The Lorentz "ice cream" cone in the given number of dimensions.

    Examples
    --------

        >>> K = IceCream(3)
        >>> print(K)
        Lorentz "ice cream" cone in the real 3-space

    """
    def __str__(self):
        """
        Output a human-readable description of myself.
        """
        tpl = 'Lorentz "ice cream" cone in the real {:d}-space'
        return tpl.format(self.dimension())


    def __contains__(self, point):
        """
        Return whether or not ``point`` belongs to this cone.

        Since this test is expected to work on points whose components
        are floating point numbers, it doesn't make any sense to
        distinguish between strict and non-strict containment -- the
        test uses a tolerance parameter.

        Parameters
        ----------

        point : matrix
            A :class:`cvxopt.base.matrix` having dimensions ``(n,1)``
            where ``n`` is the :meth:`dimension` of this cone.

        Returns
        -------

        bool

           ``True`` if ``point`` belongs to this cone, ``False`` otherwise.

        Raises
        ------

        TypeError
            If ``point`` is not a :class:`cvxopt.base.matrix`.

        TypeError
            If ``point`` has the wrong dimensions.

        Examples
        --------

        This point lies well within the ice cream cone:

            >>> K = IceCream(3)
            >>> matrix([1,0.5,0.5]) in K
            True

        This one lies on its boundary:

            >>> K = IceCream(3)
            >>> matrix([1,0,1]) in K
            True

        This point lies entirely outside of the ice cream cone:

            >>> K = IceCream(3)
            >>> matrix([1,1,1]) in K
            False

        Junk arguments don't work:

            >>> K = IceCream(3)
            >>> [1,2,3] in K
            Traceback (most recent call last):
            ...
            TypeError: the given point is not a cvxopt.base.matrix

            >>> K = IceCream(3)
            >>> matrix([1,2]) in K
            Traceback (most recent call last):
            ...
            TypeError: the given point has the wrong dimensions

        """
        if not isinstance(point, matrix):
            raise TypeError('the given point is not a cvxopt.base.matrix')
        if not point.size == (self.dimension(), 1):
            raise TypeError('the given point has the wrong dimensions')

        height = point[0]
        if self.dimension() == 1:
            # In one dimension, the ice cream cone is the nonnegative
            # orthant.
            return height > -options.ABS_TOL
        else:
            radius = point[1:]
            return norm(radius) < (height + options.ABS_TOL)


    def ball_radius(self, point):
        r"""
        Return the radius of a ball around ``point`` in this cone.

        Since a radius cannot be negative, the ``point`` must be
        contained in this cone; otherwise, an error is raised.

        The minimum distance from ``point`` to the complement of this
        cone will always occur at its projection onto that set. It is
        not hard to see that the projection is at a "down and out" angle
        of :math:`\pi/4` towards the outside of the cone. If one draws a
        right triangle involving the ``point`` and that projection, it
        becomes clear that the distance between ``point`` and its
        projection is a factor of :math:`1/\sqrt(2)` times the "horizontal"
        distance from ``point`` to boundary of this cone. For simplicity
        we take :math:`1/2` instead.

        Parameters
        ----------

        point : matrix
            A point contained in this cone.

        Returns
        -------

        float
            A radius ``r`` such that the ball of radius ``r`` centered at
            ``point`` is contained entirely within this cone.

        Raises
        ------

        TypeError
            If ``point`` is not a :class:`cvxopt.base.matrix`.

        TypeError
            If ``point`` has the wrong dimensions.

        ValueError
            if ``point`` is not contained in this cone.

        Examples
        --------

        The height of ``x`` below is one (its first coordinate), and so
        the radius of the circle obtained from a height-one cross
        section is also one. Note that the last two coordinates of ``x``
        are half of the way to the boundary of the cone, and in the
        direction of a 30-60-90 triangle. If one follows those
        coordinates, they hit at :math:`\left(1, \frac{\sqrt(3)}{2},
        \frac{1}{2}\right)` having unit norm. Thus the "horizontal"
        distance to the boundary of the cone is :math:`1 - \left\lVert x
        \right\rVert`, which simplifies to :math:`1/2`. And rather than
        involve a square root, we divide by two for a final safe radius
        of :math:`1/4`.

            >>> from math import sqrt
            >>> K = IceCream(3)
            >>> x = matrix([1, sqrt(3)/4.0, 1/4.0])
            >>> K.ball_radius(x)
            0.25

        """
        if not isinstance(point, matrix):
            raise TypeError('the given point is not a cvxopt.base.matrix')
        if not point.size == (self.dimension(), 1):
            raise TypeError('the given point has the wrong dimensions')
        if not point in self:
            raise ValueError('the given point does not lie in the cone')

        height = point[0]
        radius = norm(point[1:])
        return (height - radius) / 2.0


class SymmetricPSD(SymmetricCone):
    r"""
    The cone of real symmetric positive-semidefinite matrices.

    This cone has a dimension ``n`` associated with it, but we let ``n``
    refer to the dimension of the domain of our matrices and not the
    dimension of the (much larger) space in which the matrices
    themselves live. In other words, our ``n`` is the ``n`` that appears
    in the usual notation :math:`S^{n}` for symmetric matrices.

    As a result, the cone ``SymmetricPSD(n)`` lives in a space of dimension
    :math:`\left(n^{2} + n\right)/2)`.

    Examples
    --------

        >>> K = SymmetricPSD(3)
        >>> print(K)
        Cone of symmetric positive-semidefinite matrices on the real 3-space
        >>> K.dimension()
        3

    """
    def __str__(self):
        """
        Output a human-readable description of myself.
        """
        tpl = 'Cone of symmetric positive-semidefinite matrices ' \
              'on the real {:d}-space'
        return tpl.format(self.dimension())


    def __contains__(self, point):
        """
        Return whether or not ``point`` belongs to this cone.

        Since this test is expected to work on points whose components
        are floating point numbers, it doesn't make any sense to
        distinguish between strict and non-strict containment -- the
        test uses a tolerance parameter.

        Parameters
        ----------

        point : matrix
            A :class:`cvxopt.base.matrix` having dimensions ``(n,n)``
            where ``n`` is the :meth:`dimension` of this cone.

        Returns
        -------

        bool

           ``True`` if ``point`` belongs to this cone, ``False`` otherwise.

        Raises
        ------

        TypeError
            If ``point`` is not a :class:`cvxopt.base.matrix`.

        TypeError
            If ``point`` has the wrong dimensions.

        Examples
        --------

        These all lie in the interior of the Symmetric PSD cone:

            >>> K = SymmetricPSD(2)
            >>> matrix([[1,0],[0,1]]) in K
            True

            >>> K = SymmetricPSD(3)
            >>> matrix([[2,-1,0],[-1,2,-1],[0,-1,2]]) in K
            True

            >>> K = SymmetricPSD(5)
            >>> A = matrix([[5,4,3,2,1],
            ...             [4,5,4,3,2],
            ...             [3,4,5,4,3],
            ...             [2,3,4,5,4],
            ...             [1,2,3,4,5]])
            >>> A in K
            True

        Boundary points lie in the cone as well:

            >>> K = SymmetricPSD(2)
            >>> matrix([[0,0],[0,0]]) in K
            True

            >>> K = SymmetricPSD(5)
            >>> A = matrix([[1,0,0,0,0],
            ...             [0,1,0,0,0],
            ...             [0,0,0,0,0],
            ...             [0,0,0,1,0],
            ...             [0,0,0,0,1]])
            >>> A in K
            True

        However, this matrix has a negative eigenvalue:

           >>> K = SymmetricPSD(2)
           >>> A = matrix([[ 1, -2],
           ...             [-2,  1]])
           >>> A in K
           False

        An asymmetric cone with positive eigenvalues is not in the cone:

           >>> K = SymmetricPSD(2)
           >>> A = matrix([[10, 2],
           ...             [4,  8]])
           >>> A in K
           False

        Junk arguments don't work:

            >>> K = SymmetricPSD(2)
            >>> [[1,2],[2,3]] in K
            Traceback (most recent call last):
            ...
            TypeError: the given point is not a cvxopt.base.matrix

            >>> K = SymmetricPSD(3)
            >>> matrix([[1,2],[3,4]]) in K
            Traceback (most recent call last):
            ...
            TypeError: the given point has the wrong dimensions

        """
        if not isinstance(point, matrix):
            raise TypeError('the given point is not a cvxopt.base.matrix')
        if not point.size == (self.dimension(), self.dimension()):
            raise TypeError('the given point has the wrong dimensions')
        if not point.typecode == 'd':
            point = matrix(point, (self.dimension(), self.dimension()), 'd')
        if not norm(point - point.trans()) < options.ABS_TOL:
            # It's not symmetric.
            return False
        return all([e > -options.ABS_TOL for e in eigenvalues(point)])



class CartesianProduct(SymmetricCone):
    """
    A cartesian product of symmetric cones, which is itself a symmetric
    cone.

    Examples
    --------

        >>> K = CartesianProduct(NonnegativeOrthant(3), IceCream(2))
        >>> print(K)
        Cartesian product of dimension 5 with 2 factors:
          * Nonnegative orthant in the real 3-space
          * Lorentz "ice cream" cone in the real 2-space

    """
    def __init__(self, *factors):
        my_dimension = sum([f.dimension() for f in factors])
        super().__init__(my_dimension)
        self._factors = factors


    def __str__(self):
        """
        Output a human-readable description of myself.
        """
        tpl = 'Cartesian product of dimension {:d} with {:d} factors:'
        tpl += '\n  * {!s}' * len(self.factors())
        format_args = [self.dimension(), len(self.factors())]
        format_args += list(self.factors())
        return tpl.format(*format_args)


    def __contains__(self, point):
        """
        Return whether or not ``point`` belongs to this cone.

        The ``point`` is expected to be a tuple of points which will be
        tested for membership in this cone's factors. If each point in
        the tuple belongs to its corresponding factor, then the whole
        point belongs to this cone. Otherwise, it doesn't.

        Parameters
        ----------

        point : tuple of matrix
            A tuple of :class:`cvxopt.base.matrix` corresponding to the
            :meth:`factors` of this cartesian product.

        Returns
        -------

        bool

           ``True`` if ``point`` belongs to this cone, ``False`` otherwise.

        Raises
        ------

        TypeError
            If ``point`` is not a tuple of :class:`cvxopt.base.matrix`.

        TypeError
            If any element of ``point`` has the wrong dimensions.

        Examples
        --------

        The result depends on how containment is defined for our factors:

            >>> K = CartesianProduct(NonnegativeOrthant(3), IceCream(3))
            >>> (matrix([1,2,3]), matrix([1,0.5,0.5])) in K
            True

            >>> K = CartesianProduct(NonnegativeOrthant(3), IceCream(3))
            >>> (matrix([0,0,0]), matrix([1,0,1])) in K
            True

            >>> K = CartesianProduct(NonnegativeOrthant(3), IceCream(3))
            >>> (matrix([1,1,1]), matrix([1,1,1])) in K
            False

            >>> K = CartesianProduct(NonnegativeOrthant(3), IceCream(3))
            >>> (matrix([1,-1,1]), matrix([1,0,1])) in K
            False

        Junk arguments don't work:

            >>> K = CartesianProduct(NonnegativeOrthant(3), IceCream(3))
            >>> [[1,2,3],[4,5,6]] in K
            Traceback (most recent call last):
            ...
            TypeError: the given point is not a cvxopt.base.matrix

            >>> K = CartesianProduct(NonnegativeOrthant(3), IceCream(3))
            >>> (matrix([1,2]), matrix([3,4,5,6])) in K
            Traceback (most recent call last):
            ...
            TypeError: the given point has the wrong dimensions

        """
        return all([p in f for (p, f) in zip(point, self.factors())])



    def factors(self):
        """
        Return a tuple containing the factors (in order) of this
        cartesian product.

        Returns
        -------

        tuple of SymmetricCone.
            The factors of this cartesian product.

        Examples
        --------

            >>> K = CartesianProduct(NonnegativeOrthant(3), IceCream(2))
            >>> len(K.factors())
            2

        """
        return self._factors


    def cvxopt_dims(self):
        """
        Return a dictionary of dimensions corresponding to the
        factors of this cartesian product. The format of this dictionary
        is described in the `CVXOPT user's guide
        <http://cvxopt.org/userguide/coneprog.html#linear-cone-programs>`_.

        Returns
        -------

        dict
            A dimension dictionary suitable to feed to CVXOPT.

        Examples
        --------

            >>> K = CartesianProduct(NonnegativeOrthant(3),
            ...                      IceCream(2),
            ...                      IceCream(3))
            >>> d = K.cvxopt_dims()
            >>> (d['l'], d['q'], d['s'])
            (3, [2, 3], [])

        """
        dims = {'l':0, 'q':[], 's':[]}
        dims['l'] += sum([K.dimension()
                          for K in self.factors()
                          if isinstance(K, NonnegativeOrthant)])
        dims['q'] = [K.dimension()
                     for K in self.factors()
                     if isinstance(K, IceCream)]
        dims['s'] = [K.dimension()
                     for K in self.factors()
                     if isinstance(K, SymmetricPSD)]
        return dims


