"""
Unit tests for the functions in the :mod:`dunshire.matrices` module.
"""

from copy import deepcopy
from unittest import TestCase

from dunshire.matrices import (append_col, append_row, condition_number,
                               eigenvalues, eigenvalues_re, identity,
                               inner_product, norm)
from dunshire.options import ABS_TOL
from .randomgen import random_matrix, random_natural


class AppendColTest(TestCase):
    """
    Tests for the :func:`append_col` function.
    """

    def test_new_dimensions(self):
        """
        If we append one matrix to another side-by-side, then the result
        should have the same number of rows as the two original
        matrices. However, the number of their columns should add up to
        the number of columns in the new combined matrix.
        """
        rows = random_natural()
        cols1 = random_natural()
        cols2 = random_natural()
        mat1 = random_matrix(rows, cols1)
        mat2 = random_matrix(rows, cols2)
        bigmat = append_col(mat1, mat2)
        self.assertTrue(bigmat.size[0] == rows)
        self.assertTrue(bigmat.size[1] == cols1+cols2)


class AppendRowTest(TestCase):
    """
    Tests for the :func:`dunshire.matrices.append_row` function.
    """

    def test_new_dimensions(self):
        """
        If we append one matrix to another top-to-bottom, then
        the result should have the same number of columns as the two
        original matrices. However, the number of their rows should add
        up to the number of rows in the the new combined matrix.
        """
        rows1 = random_natural()
        rows2 = random_natural()
        cols = random_natural()
        mat1 = random_matrix(rows1, cols)
        mat2 = random_matrix(rows2, cols)
        bigmat = append_row(mat1, mat2)
        self.assertTrue(bigmat.size[0] == rows1+rows2)
        self.assertTrue(bigmat.size[1] == cols)


class EigenvaluesTest(TestCase):
    """
    Tests for the :func:`dunshire.matrices.eigenvalues` function.
    """

    def test_eigenvalues_input_not_clobbered(self):
        """
        The eigenvalue functions provided by CVXOPT/LAPACK like to
        overwrite the matrices that you pass into them as
        arguments. This test makes sure that our :func:`eigenvalues`
        function does not do the same.

        We use a ``deepcopy`` here in case the ``copy`` used in the
        :func:`eigenvalues` function is insufficient. If ``copy`` didn't
        work and this test used it too, then this test would pass when
        it shouldn't.
        """
        mat = random_matrix(random_natural())
        symmat = mat + mat.trans()
        symmat_copy = deepcopy(symmat)
        dummy = eigenvalues(symmat)
        self.assertTrue(norm(symmat - symmat_copy) < ABS_TOL)

    def test_eigenvalues_of_symmat_are_real(self):
        """
        A real symmetric matrix has real eigenvalues, so if we start
        with a symmetric matrix, then the two functions
        :func:`dunshire.matrices.eigenvalues` and
        :func:`dunshire.matrices.eigenvalues_re` should agree on it.
        """
        mat = random_matrix(random_natural())
        symmat = mat + mat.trans()
        eigs1 = sorted(eigenvalues(symmat))
        eigs2 = sorted(eigenvalues_re(symmat))
        diffs = [abs(e1 - e2) for (e1, e2) in zip(eigs1, eigs2)]
        self.assertTrue(all([diff < ABS_TOL for diff in diffs]))

    def test_eigenvalues_of_identity(self):
        """
        All eigenvalues of the identity matrix should be one.
        """
        mat = identity(random_natural(), typecode='d')
        eigs = eigenvalues(mat)
        self.assertTrue(all([abs(ev - 1) < ABS_TOL for ev in eigs]))


class EigenvaluesRealPartTest(TestCase):
    """
    Tests for the :func:`dunshire.matrices.eigenvalues_re` function.
    """

    def test_eigenvalues_re_input_not_clobbered(self):
        """
        The eigenvalue functions provided by CVXOPT/LAPACK like
        to overwrite the matrices that you pass into them as
        arguments. This test makes sure that our
        :func:`dunshire.matrices.eigenvalues_re` function does not do
        the same.

        We use a ``deepcopy`` here in case the ``copy`` used in the
        :func:`dunshire.matrices.eigenvalues_re` function is
        insufficient. If ``copy`` didn't work and this test used it too,
        then this test would pass when it shouldn't.
        """
        mat = random_matrix(random_natural())
        mat_copy = deepcopy(mat)
        dummy = eigenvalues_re(mat)
        self.assertTrue(norm(mat - mat_copy) < ABS_TOL)

    def test_eigenvalues_re_of_identity(self):
        """
        All eigenvalues of the identity matrix should be one.
        """
        mat = identity(random_natural(), typecode='d')
        eigs = eigenvalues_re(mat)
        self.assertTrue(all([abs(ev - 1) < ABS_TOL for ev in eigs]))


class InnerProductTest(TestCase):
    """
    Tests for the :func:`dunshire.matrices.inner_product` function.
    """

    def test_inner_product_with_self_is_norm_squared(self):
        """
        Ensure that the func:`dunshire.matrices.inner_product` and
        :func:`dunshire.matrices.norm` functions are compatible by
        checking that the square of the norm of a vector is its inner
        product with itself.
        """
        vec = random_matrix(random_natural(), 1)
        actual = inner_product(vec, vec)
        expected = norm(vec)**2
        self.assertTrue(abs(actual - expected) < ABS_TOL)


class NormTest(TestCase):
    """
    Tests for the :func:`dunshire.matrices.norm` function.
    """

    def test_norm_is_nonnegative(self):
        """
        Test one of the properties of a norm, that it is nonnegative.
        """
        mat = random_matrix(random_natural(), random_natural())
        self.assertTrue(norm(mat) >= 0)


class ConditionNumberTest(TestCase):
    """
    Tests for the :func:`dunshire.matrices.condition_number` function.
    """

    def test_condition_number_ge_one(self):
        """
        From the way that it is defined, the condition number should
        always be greater than or equal to one.
        """
        mat = random_matrix(random_natural(), random_natural())
        self.assertTrue(condition_number(mat) >= 1)
