"""Test grid logic and representation."""

import pytest

from royal_game._constants import black_piece, rosette, white_piece
from royal_game._exceptions import InvalidNumPieces
from royal_game.modules.grid import Grid, StartEndGrid
from royal_game.modules.grid_status import GridStatus


def test_reject_invalid_grid():
    with pytest.raises(InvalidNumPieces) as e:
        _ = StartEndGrid(num_pieces=-1, name="")

    with pytest.raises(InvalidNumPieces) as e:
        _ = StartEndGrid(num_pieces=10, name="")


def test_int_conversion():
    assert int(Grid("", False, GridStatus.empty)) == 0
    assert int(StartEndGrid(5, "")) == 5


def test_repr():
    test_end = StartEndGrid(3, "end")
    assert str(test_end) == "   \n 3 \n   \n"

    test_grid = Grid("test", False, GridStatus.empty)
    assert str(test_grid) == "---\n| |\n---\n"

    test_grid.is_rosette = True
    assert str(test_grid) == f"---\n|{rosette}|\n---\n"

    test_grid.status = GridStatus.white
    assert str(test_grid) == f"---\n|{white_piece}|\n---\n"

    test_grid.status = GridStatus.black
    assert str(test_grid) == f"---\n|{black_piece}|\n---\n"