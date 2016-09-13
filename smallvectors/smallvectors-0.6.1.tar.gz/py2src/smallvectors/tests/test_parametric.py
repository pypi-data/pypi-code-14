# -*- coding: utf8 -*-
import pytest
from generic.tests.test_parametric import *
from smallvectors import Vec, VecAny, SmallVectorsBase, SmallVectorsMeta


del A, B


@pytest.fixture
def A():
    return VecAny

@pytest.fixture
def B():
    return Vec


def test_partial_parameters(A, B):
    assert SmallVectorsBase.__parameters__ is None
    assert B.__parameters__ == (int, type)
    assert B[2].__parameters__ == (2, type)


def test_correct_metatypes(A, B):
    assert type(A) == SmallVectorsMeta
    assert type(B) == SmallVectorsMeta
    assert type(B[2, float]) == SmallVectorsMeta


def test_abstract_and_orign_has_ndim(A, B):
    assert A.ndim == 1
    assert B.ndim == 1


def test_concrete_has_ndim(A, B):
    assert B[2, float].ndim == 1


def test_has_size(A, B):
    assert A.size is None
    assert B.size is None
    assert B[2, float].size == 2


def test_concrete_abstract_and_origin_has_shape(A, B):
    assert A.shape == (None,)
    assert B.shape == (None,)
    assert B[2, float].shape == (2,)


def test_has_dtype(A, B):
    assert A.dtype is None
    assert B.dtype is None
    assert B[2, float].dtype == float


if __name__ == '__main__':
    pytest.main('test_parametric.py -q')