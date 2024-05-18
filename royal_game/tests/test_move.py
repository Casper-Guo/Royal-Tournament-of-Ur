import pytest

from royal_game.modules.move import Move
from royal_game._exceptions import ImpossibleMove

def test_reject_invalid():
    with pytest.raises(ImpossibleMove):
        _ = Move("W4", "B4")
    with pytest.raises(ImpossibleMove):
        _ = Move("B13", "W14")
    with pytest.raises(ImpossibleMove):
        _ = Move("8", "8")
    with pytest.raises(ImpossibleMove):
        _ = Move("5", "8", is_rosette=True, is_capture=True)
    with pytest.raises(ImpossibleMove):
        _ = Move("12", "BE", is_rosette=True, is_ascension=True)