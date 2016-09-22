from words import is_clean


def test_clean():
    assert is_clean("snowdrift") is True

    assert is_clean("snowdrift's") is False
    assert is_clean("Englishes") is False
    assert is_clean("steve") is False
    assert is_clean("conglomerated") is False
