"""Implements game loop."""

from royal_game._exceptions import InvalidPlayer
from royal_game.modules.board import Board
from royal_game.modules.player import Player


class Game:
    """
    Simulates a game between two players.

    Each player should inherit from the Player class and
    implements select_move.
    """

    def __init__(self, player1: Player, player2: Player):
        if "select_move" not in dir(player1):
            raise InvalidPlayer(player1)

        if "select_move" not in dir(player2):
            raise InvalidPlayer(player2)

        self.player1 = player1
        self.player2 = player2
        self.board = Board()

    """
    Game loop basic design:
    1, roll dices. If 0, skip to 5
    2, send available moves to player
    3, player returns selected move
    4, update board
    5, determine who has the next turn
    """
