import pytest

from firesat.hello import hello_world


def test_true_hello():
    assert hello_world() == "Hello, World!"


def test_false_hello():
    with pytest.raises(AssertionError):
        assert hello_world() == 1
