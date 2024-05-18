import pytest

from royal_game.modules.game import Game
from royal_game.modules.board import Board
from royal_game.players.dummy import DummyPlayer

def test_end_game():
    white_win = Game(DummyPlayer(), DummyPlayer(), Board(599282155520))
    assert white_win.play()

    black_win = Game(DummyPlayer(), DummyPlayer(), Board(966988398624))
    assert not black_win.play()