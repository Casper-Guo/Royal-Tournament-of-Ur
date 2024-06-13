import pytest

from royal_game._exceptions import BoardError
from rust_translate import translate


def test_translate():
    assert (
        translate(0b0010111000000000000010000100000000100000000000001000010000000000)
        == 87510499392
    )

    assert (
        translate(0b0110000000000000000000000010100000100000000000000000001000000000)
        == 83751871040
    )

    with pytest.raises(BoardError):
        # too many black pieces
        translate(0b0000000000001010101010101010000000000000101010101010101000000000)
