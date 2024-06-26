import pytest

from royal_game._constants import black_piece, rosette, white_piece
from royal_game._exceptions import InvalidNumPieces
from royal_game.modules.grid import Grid, StartEndGrid
from royal_game.modules.grid_status import GridStatus


def test_reject_invalid_grid():
    with pytest.raises(InvalidNumPieces):
        _ = StartEndGrid(name="", num_pieces=-1)

    with pytest.raises(InvalidNumPieces):
        _ = StartEndGrid(name="", num_pieces=10)


def test_int_conversion():
    assert int(Grid("W3", False, GridStatus.empty)) == 0
    assert int(Grid("8", True, GridStatus.white)) == 1
    assert int(Grid("B14", False, GridStatus.black)) == 2
    assert int(StartEndGrid("WS", 5)) == 5
    assert int(StartEndGrid("BE", 1)) == 1


def test_repr():
    test_end = StartEndGrid("end", 3)
    assert str(test_end) == "   \n 3 \n   \n"

    test_grid = Grid("test", False, GridStatus.empty)
    assert str(test_grid) == "---\n| |\n---\n"

    test_grid.is_rosette = True
    assert str(test_grid) == f"---\n|{rosette}|\n---\n"

    test_grid.status = GridStatus.white
    assert str(test_grid) == f"---\n|{white_piece}|\n---\n"

    test_grid.status = GridStatus.black
    assert str(test_grid) == f"---\n|{black_piece}|\n---\n"
