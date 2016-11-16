"""
Errors that can occur when solving a linear game.
"""

from cvxopt import matrix


def _pretty_format_dict(dictionary):
    """
    Return a pretty-formatted string representation of a dictionary
    containing CVXOPT matrices.

    The dictionary is also sorted so that it can be tested repeatably.

    Examples
    --------

        >>> d = {'foo': 1.234, 'bar': matrix([1,2,3])}
        >>> print(_pretty_format_dict(d))
        bar:
          [ 1]
          [ 2]
          [ 3]
        foo: 1.234

    """
    result = ''
    for (key, value) in sorted(dictionary.items()):
        if isinstance(value, matrix):
            # Display matrices on their own lines, indented.
            result += '{:s}:'.format(key)
            colvec = '\n{!s}'.format(value)
            result += '\n  '.join(colvec.splitlines())
            result += '\n'
        else:
            result += '{:s}: {!s}\n'.format(key, value)

    return result.rstrip('\n') # Kills trailing newlines on matrices.


class GameUnsolvableException(Exception):
    """
    An exception raised when a game cannot be solved.

    Every linear game has a solution. If we can't solve the conic
    program associated with a linear game, then something is wrong with
    either the model or the input, and this exception should be raised.

    Parameters
    ----------

    game : SymmetricLinearGame
        A copy of the game whose solution failed.

    solution_dict : dict
        The solution dictionary returned from the failed cone program.

    Examples
    --------

       >>> from dunshire import *
       >>> K = IceCream(2)
       >>> L = [[1,2],[3,4]]
       >>> e1 = [1, 0.1]
       >>> e2 = [3, 0.1]
       >>> G = SymmetricLinearGame(L,K,e1,e2)
       >>> d = {'residual as dual infeasibility certificate': None,
       ...      'y': matrix([1,1]),
       ...      'dual slack': 8.779496368228267e-10,
       ...      'z': matrix([1,1,0,0]),
       ...      's': None,
       ...      'primal infeasibility': None,
       ...      'status': 'primal infeasible',
       ...      'dual infeasibility': None,
       ...      'relative gap': None,
       ...      'iterations': 5,
       ...      'primal slack': None,
       ...      'x': None,
       ...      'dual objective': 1.0,
       ...      'primal objective': None,
       ...      'gap': None,
       ...      'residual as primal infeasibility certificate':
       ...          3.986246886102996e-09}
       >>> print(GameUnsolvableException(G,d))
       Solution failed with result "primal infeasible."
       The linear game (L, K, e1, e2) where
         L = [ 1  2]
             [ 3  4],
         K = Lorentz "ice cream" cone in the real 2-space,
         e1 = [1.0000000]
              [0.1000000],
         e2 = [3.0000000]
              [0.1000000]
       CVXOPT returned:
         dual infeasibility: None
         dual objective: 1.0
         dual slack: 8.779496368228267e-10
         gap: None
         iterations: 5
         primal infeasibility: None
         primal objective: None
         primal slack: None
         relative gap: None
         residual as dual infeasibility certificate: None
         residual as primal infeasibility certificate: 3.986246886102996e-09
         s: None
         status: primal infeasible
         x: None
         y:
           [ 1]
           [ 1]
         z:
           [ 1]
           [ 1]
           [ 0]
           [ 0]
    """
    def __init__(self, game, solution_dict):
        """
        Create a new :class:`GameUnsolvableException` object.
        """
        super().__init__()
        self._game = game
        self._solution_dict = solution_dict


    def __str__(self):
        """
        Return a string representation of this exception.

        The returned representation highlights the "status" field of the
        CVXOPT dictionary, since that should explain what went
        wrong. The game details and full CVXOPT solution dictionary are
        included after the status.
        """
        tpl = 'Solution failed with result "{:s}."\n' \
              '{!s}\n' \
              'CVXOPT returned:\n  {!s}'
        cvx_lines = _pretty_format_dict(self._solution_dict).splitlines()
        # Indent the whole dict by two spaces.
        cvx_str = '\n  '.join(cvx_lines)
        return tpl.format(self._solution_dict['status'], self._game, cvx_str)


class PoorScalingException(Exception):
    """
    An exception raised when poor scaling leads to solution errors.

    Under certain circumstances, a problem that should be solvable can
    trigger errors in CVXOPT. The end result is the following
    :class:`ValueError`::

        Traceback (most recent call last):
        ...
          return math.sqrt(x[offset] - a) * math.sqrt(x[offset] + a)
        ValueError: math domain error

    This happens when one of the arguments to :func:`math.sqrt` is
    negative, but the underlying cause is elusive. We're blaming it on
    "poor scaling," whatever that means.

    Similar issues have been discussed a few times on the CVXOPT mailing
    list; for example,

    1. https://groups.google.com/forum/#!msg/cvxopt/TeQGdc2b4Xc/j5_mQME_rvUJ
    2. https://groups.google.com/forum/#!topic/cvxopt/HZrRfaoM0pk
    3. https://groups.google.com/forum/#!topic/cvxopt/riFSxB31zU4

    Parameters
    ----------

    game : SymmetricLinearGame
        A copy of the game whose solution failed.

    Examples
    --------

       >>> from dunshire import *
       >>> K = IceCream(2)
       >>> L = [[1,2],[3,4]]
       >>> e1 = [1, 0.1]
       >>> e2 = [3, 0.1]
       >>> G = SymmetricLinearGame(L,K,e1,e2)
       >>> print(PoorScalingException(G))
       Solution failed due to poor scaling.
       The linear game (L, K, e1, e2) where
         L = [ 1  2]
             [ 3  4],
         K = Lorentz "ice cream" cone in the real 2-space,
         e1 = [1.0000000]
              [0.1000000],
         e2 = [3.0000000]
              [0.1000000]
       <BLANKLINE>
    """
    def __init__(self, game):
        """
        Create a new :class:`PoorScalingException` object.
        """
        super().__init__()
        self._game = game


    def __str__(self):
        """
        Return a string representation of this exception.

        Pretty much all we can say is that there was poor scaling; that
        is, that CVXOPT failed. The game details are included after
        that.
        """
        tpl = 'Solution failed due to poor scaling.\n' \
              '{!s}\n'
        return tpl.format(self._game)
