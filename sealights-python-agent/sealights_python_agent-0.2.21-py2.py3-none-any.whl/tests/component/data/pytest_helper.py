
class TestSanity(object):

    def test_3plus3(self):
        assert 3 + 3 == 6

    def test_1plus1(self):
        assert 1 + 1 == 2


class TestPassSkip(object):
    import pytest

    def test_3plus3(self):
        assert 3+3 == 6

    @pytest.mark.skip()
    def test_1plus1(self):
        assert 1+1 == 2


class TestAllSkipped(object):
    import pytest

    @pytest.mark.skip()
    def test_3plus3(self):
        assert 3+3 == 6

    @pytest.mark.skip()
    def test_1plus1(self):
        assert 1+1 == 2


class TestSkipError(object):
    import pytest

    @pytest.mark.skip()
    def test_3plus3(self):
        assert 3+3 == 6

    def test_1plus1(self):
        a[1]
        assert 1+1 == 2


class TestPassError(object):

    def test_3plus3(self):
        assert 3+3 == 6

    def test_1plus1(self):
        a[1]
        assert 1+1 == 2