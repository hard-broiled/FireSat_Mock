import pytest


def test_sanity_true():
    assert 1 + 2 == 3


def test_sanity_false():
    with pytest.raises(AssertionError):
        assert 1 + 2 == 4
