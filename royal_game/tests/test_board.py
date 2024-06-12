import pytest

from royal_game._exceptions import InvalidNumberofPieces
from royal_game.modules.board import Board
from royal_game.modules.grid_status import GridStatus
from royal_game.modules.move import Move


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
    assert board.board["W4"].status is GridStatus.white
    assert board.board["8"].status is GridStatus.empty
    assert board.board["B14"].status is GridStatus.empty
    assert int(board.board["WS"]) == 2
    assert int(board.board["BE"]) == 1
    assert int(board) == 174518804524

    board = Board(104689829892)
    assert board.board["W3"].status is GridStatus.white
    assert board.board["B4"].status is GridStatus.empty
    assert board.board["W14"].status is GridStatus.empty
    assert board.board["B14"].status is GridStatus.black
    assert int(board.board["BS"]) == 6
    assert int(board) == 104689829892


def test_check_end_state():
    assert Board(966988398624).is_end_state()
    assert Board(599282155520).is_end_state()
    assert not Board(829549445216).is_end_state()
    assert not Board(597403107328).is_end_state()


def test_get_available_moves():
    board = Board(86973360148)
    black_4_expected = set((Move("BS", "B4", is_rosette=True, is_onboard=True), Move("5", "9")))
    assert black_4_expected == set(board.get_available_moves(False, 4))
    white_2_expected = set(
        (
            Move("WS", "W2", is_onboard=True),
            Move("W3", "5", is_capture=True),
            Move("8", "10"),
            Move("W13", "WE", is_ascension=True),
        )
    )
    assert white_2_expected == set(board.get_available_moves(True, 2))

    board = Board(88852430985)
    black_2_expected = set((Move("B2", "B4", is_rosette=True), Move("6", "9")))
    assert black_2_expected == set(board.get_available_moves(False, 2))

    # no piece remaining off the board special case
    board = Board(837518624784)
    assert set([Move("W13", "WE", is_ascension=True)]) == set(
        board.get_available_moves(True, 2)
    )
    assert set([Move("B14", "BE", is_ascension=True)]) == set(
        board.get_available_moves(False, 1)
    )

    # end game boards
    board = Board(966988398624)
    assert board.get_available_moves(True, 1) == ()
    board = Board(599282155520)
    assert board.get_available_moves(False, 4) == ()


def test_move():
    board = Board()
    board.make_move(Move("WS", "W3", False, False, False, True))
    assert int(board) == 121869697028
    board.make_move(Move("BS", "B2", False, False, False, True))
    assert int(board) == 104689827972
    board.make_move(Move("WS", "W4", True, False, False, True))
    assert int(board) == 104421392524
    board.make_move(Move("W4", "6", False, False, False, False))
    board.make_move(Move("B2", "6", False, True, False, False))
    assert int(board) == 104689860612
    board.make_move(Move("6", "10", False, False, False, False))
    assert int(board) == 104698216452
    board.make_move(Move("10", "B14", True, False, False, False))
    assert int(board) == 104689829892
    board.make_move(Move("B14", "BE", False, False, True, False))
    assert int(board) == 242128781316
