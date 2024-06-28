import pytest

from royal_game._exceptions import BoardError
from translate import rust_to_python, python_to_rust


def test_rust_to_python():
    assert (
        rust_to_python(0b0010111000000000000010000100000000100000000000001000010000000000)
        == 87510499392
    )

    assert (
        rust_to_python(0b0110000000000000000000000010100000100000000000000000001000000000)
        == 83751871040
    )

    with pytest.raises(BoardError):
        # too many black pieces
        rust_to_python(0b0000000000001010101010101010000000000000101010101010101000000000)


def test_python_to_rust():
    assert (
        python_to_rust(87510499392)
        == 0b1110111000000000000010000100000000100000000000001000010000000000
    )

    assert (
        python_to_rust(83751871040)
        == 0b0110000000000000000000000010100000100000000000000000001000000000
    )

    assert (
        python_to_rust(966988398624)
        == 0b1000001000000101000000000000000000000100010100000000000000000000
    )

    with pytest.raises(BoardError):
        python_to_rust(155055118456)
