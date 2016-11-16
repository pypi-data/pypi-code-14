"""
Unit tests for the :class:`SymmetricLinearGame` class.
"""

from unittest import TestCase

from dunshire.games import SymmetricLinearGame
from dunshire.matrices import eigenvalues_re, inner_product, norm
from dunshire import options
from .randomgen import (random_icecream_game, random_ll_icecream_game,
                        random_ll_orthant_game, random_nn_scaling,
                        random_orthant_game, random_positive_orthant_game,
                        random_translation)


# Tell pylint to shut up about the large number of methods.
class SymmetricLinearGameTest(TestCase): # pylint: disable=R0904
    """
    Tests for the SymmetricLinearGame and Solution classes.
    """
    def assert_within_tol(self, first, second, modifier=1):
        """
        Test that ``first`` and ``second`` are equal within a multiple of
        our default tolerances.

        Parameters
        ----------

        first : float
            The first number to compare.

        second : float
            The second number to compare.

        modifier : float
            A scaling factor (default: 1) applied to the default
            tolerance for this comparison. If you have a poorly-
            conditioned matrix, for example, you may want to set this
            greater than one.

        """
        self.assertTrue(abs(first - second) < options.ABS_TOL*modifier)


    def test_solutions_dont_change_orthant(self):
        """
        If we solve the same game twice over the nonnegative orthant,
        then we should get the same solution both times. The solution to
        a game is not unique, but the process we use is (as far as we
        know) deterministic.
        """
        G = random_orthant_game()
        self.assert_solutions_dont_change(G)

    def test_solutions_dont_change_icecream(self):
        """
        If we solve the same game twice over the ice-cream cone, then we
        should get the same solution both times. The solution to a game
        is not unique, but the process we use is (as far as we know)
        deterministic.
        """
        G = random_icecream_game()
        self.assert_solutions_dont_change(G)

    def assert_solutions_dont_change(self, G):
        """
        Solve ``G`` twice and check that the solutions agree.
        """
        soln1 = G.solution()
        soln2 = G.solution()
        p1_diff = norm(soln1.player1_optimal() - soln2.player1_optimal())
        p2_diff = norm(soln1.player2_optimal() - soln2.player2_optimal())
        gv_diff = abs(soln1.game_value() - soln2.game_value())

        p1_close = p1_diff < options.ABS_TOL
        p2_close = p2_diff < options.ABS_TOL
        gv_close = gv_diff < options.ABS_TOL

        self.assertTrue(p1_close and p2_close and gv_close)


    def assert_player1_start_valid(self, G):
        """
        Ensure that player one's starting point satisfies both the
        equality and cone inequality in the CVXOPT primal problem.
        """
        x = G.player1_start()['x']
        s = G.player1_start()['s']
        s1 = s[0:G.dimension()]
        s2 = s[G.dimension():]
        self.assert_within_tol(norm(G.A()*x - G.b()), 0)
        self.assertTrue((s1, s2) in G.C())


    def test_player1_start_valid_orthant(self):
        """
        Ensure that player one's starting point is feasible over the
        nonnegative orthant.
        """
        G = random_orthant_game()
        self.assert_player1_start_valid(G)


    def test_player1_start_valid_icecream(self):
        """
        Ensure that player one's starting point is feasible over the
        ice-cream cone.
        """
        G = random_icecream_game()
        self.assert_player1_start_valid(G)


    def assert_player2_start_valid(self, G):
        """
        Check that player two's starting point satisfies both the
        cone inequality in the CVXOPT dual problem.
        """
        z = G.player2_start()['z']
        z1 = z[0:G.dimension()]
        z2 = z[G.dimension():]
        self.assertTrue((z1, z2) in G.C())


    def test_player2_start_valid_orthant(self):
        """
        Ensure that player two's starting point is feasible over the
        nonnegative orthant.
        """
        G = random_orthant_game()
        self.assert_player2_start_valid(G)


    def test_player2_start_valid_icecream(self):
        """
        Ensure that player two's starting point is feasible over the
        ice-cream cone.
        """
        G = random_icecream_game()
        self.assert_player2_start_valid(G)


    def test_condition_lower_bound(self):
        """
        Ensure that the condition number of a game is greater than or
        equal to one.

        It should be safe to compare these floats directly: we compute
        the condition number as the ratio of one nonnegative real number
        to a smaller nonnegative real number.
        """
        G = random_orthant_game()
        self.assertTrue(G.condition() >= 1.0)
        G = random_icecream_game()
        self.assertTrue(G.condition() >= 1.0)


    def assert_scaling_works(self, G):
        """
        Test that scaling ``L`` by a nonnegative number scales the value
        of the game by the same number.
        """
        (alpha, H) = random_nn_scaling(G)
        soln1 = G.solution()
        soln2 = H.solution()
        value1 = soln1.game_value()
        value2 = soln2.game_value()
        modifier1 = G.tolerance_scale(soln1)
        modifier2 = H.tolerance_scale(soln2)
        modifier = max(modifier1, modifier2)
        self.assert_within_tol(alpha*value1, value2, modifier)


    def test_scaling_orthant(self):
        """
        Test that scaling ``L`` by a nonnegative number scales the value
        of the game by the same number over the nonnegative orthant.
        """
        G = random_orthant_game()
        self.assert_scaling_works(G)


    def test_scaling_icecream(self):
        """
        The same test as :meth:`test_nonnegative_scaling_orthant`,
        except over the ice cream cone.
        """
        G = random_icecream_game()
        self.assert_scaling_works(G)


    def assert_translation_works(self, G):
        """
        Check that translating ``L`` by alpha*(e1*e2.trans()) increases
        the value of the associated game by alpha.
        """
        # We need to use ``L`` later, so make sure we transpose it
        # before passing it in as a column-indexed matrix.
        soln1 = G.solution()
        value1 = soln1.game_value()
        x_bar = soln1.player1_optimal()
        y_bar = soln1.player2_optimal()

        # This is the "correct" representation of ``M``, but COLUMN
        # indexed...
        (alpha, H) = random_translation(G)
        value2 = H.solution().game_value()

        modifier = G.tolerance_scale(soln1)
        self.assert_within_tol(value1 + alpha, value2, modifier)

        # Make sure the same optimal pair works.
        self.assert_within_tol(value2, H.payoff(x_bar, y_bar), modifier)


    def test_translation_orthant(self):
        """
        Test that translation works over the nonnegative orthant.
        """
        G = random_orthant_game()
        self.assert_translation_works(G)


    def test_translation_icecream(self):
        """
        The same as :meth:`test_translation_orthant`, except over the
        ice cream cone.
        """
        G = random_icecream_game()
        self.assert_translation_works(G)


    def assert_opposite_game_works(self, G):
        """
        Check the value of the "opposite" game that gives rise to a
        value that is the negation of the original game. Comes from
        some corollary.
        """
        # This is the "correct" representation of ``M``, but
        # COLUMN indexed...
        M = -G.L().trans()

        # so we have to transpose it when we feed it to the constructor.
        # Note: the condition number of ``H`` should be comparable to ``G``.
        H = SymmetricLinearGame(M.trans(), G.K(), G.e2(), G.e1())

        soln1 = G.solution()
        x_bar = soln1.player1_optimal()
        y_bar = soln1.player2_optimal()
        soln2 = H.solution()

        modifier = G.tolerance_scale(soln1)
        self.assert_within_tol(-soln1.game_value(),
                               soln2.game_value(),
                               modifier)

        # Make sure the switched optimal pair works. Since x_bar and
        # y_bar come from G, we use the same modifier.
        self.assert_within_tol(soln2.game_value(),
                               H.payoff(y_bar, x_bar),
                               modifier)



    def test_opposite_game_orthant(self):
        """
        Test the value of the "opposite" game over the nonnegative
        orthant.
        """
        G = random_orthant_game()
        self.assert_opposite_game_works(G)


    def test_opposite_game_icecream(self):
        """
        Like :meth:`test_opposite_game_orthant`, except over the
        ice-cream cone.
        """
        G = random_icecream_game()
        self.assert_opposite_game_works(G)


    def assert_orthogonality(self, G):
        """
        Two orthogonality relations hold at an optimal solution, and we
        check them here.
        """
        soln = G.solution()
        x_bar = soln.player1_optimal()
        y_bar = soln.player2_optimal()
        value = soln.game_value()

        ip1 = inner_product(y_bar, G.L()*x_bar - value*G.e1())
        ip2 = inner_product(value*G.e2() - G.L().trans()*y_bar, x_bar)

        modifier = G.tolerance_scale(soln)
        self.assert_within_tol(ip1, 0, modifier)
        self.assert_within_tol(ip2, 0, modifier)


    def test_orthogonality_orthant(self):
        """
        Check the orthgonality relationships that hold for a solution
        over the nonnegative orthant.
        """
        G = random_orthant_game()
        self.assert_orthogonality(G)


    def test_orthogonality_icecream(self):
        """
        Check the orthgonality relationships that hold for a solution
        over the ice-cream cone.
        """
        G = random_icecream_game()
        self.assert_orthogonality(G)


    def test_positive_operator_value(self):
        """
        Test that a positive operator on the nonnegative orthant gives
        rise to a a game with a nonnegative value.

        This test theoretically applies to the ice-cream cone as well,
        but we don't know how to make positive operators on that cone.
        """
        G = random_positive_orthant_game()
        self.assertTrue(G.solution().game_value() >= -options.ABS_TOL)


    def assert_lyapunov_works(self, G):
        """
        Check that Lyapunov games act the way we expect.
        """
        soln = G.solution()

        # We only check for positive/negative stability if the game
        # value is not basically zero. If the value is that close to
        # zero, we just won't check any assertions.
        #
        # See :meth:`assert_within_tol` for an explanation of the
        # fudge factors.
        eigs = eigenvalues_re(G.L())

        if soln.game_value() > options.ABS_TOL:
            # L should be positive stable
            positive_stable = all([eig > -options.ABS_TOL for eig in eigs])
            self.assertTrue(positive_stable)
        elif soln.game_value() < -options.ABS_TOL:
            # L should be negative stable
            negative_stable = all([eig < options.ABS_TOL for eig in eigs])
            self.assertTrue(negative_stable)

        dualsoln = G.dual().solution()
        mod = G.tolerance_scale(soln)
        self.assert_within_tol(dualsoln.game_value(), soln.game_value(), mod)


    def test_lyapunov_orthant(self):
        """
        Test that a Lyapunov game on the nonnegative orthant works.
        """
        G = random_ll_orthant_game()
        self.assert_lyapunov_works(G)


    def test_lyapunov_icecream(self):
        """
        Test that a Lyapunov game on the ice-cream cone works.
        """
        G = random_ll_icecream_game()
        self.assert_lyapunov_works(G)
