"""Test board logic and representation."""

import pytest

from royal_game._exceptions import InvalidNumberofPieces
from royal_game.modules.board import Board
from royal_game.modules.grid_status import GridStatus


def test_reject_invalid_board():
    with pytest.raises(InvalidNumberofPieces, match=r"(white|black).*0"):
        _ = Board(0)
    with pytest.raises(InvalidNumberofPieces, match=r"white.*8"):
        _ = Board(481040535615)
    with pytest.raises(InvalidNumberofPieces, match=r"black.*6"):
        _ = Board(155055118456)
    with pytest.raises(InvalidNumberofPieces, match=r"black.*8"):
        _ = Board(292865706639)


def test_init():
    board = Board(174518804524)
    assert board.board["W4"].status == GridStatus.white
    assert board.board["8"].status == GridStatus.empty
    assert board.board["B14"].status == GridStatus.empty
    assert int(board.board["WS"]) == 2
    assert int(board.board["BE"]) == 1
    assert int(board) == 174518804524


def test_check_endstate():
    assert Board(966988398624).is_end_state()
    assert Board(599282155520).is_end_state()
    assert not Board(829549445216).is_end_state()
    assert not Board(597403107328).is_end_state()
