"""Implements game loop."""

import logging
from random import choices

from royal_game._exceptions import InvalidMove, InvalidPlayer
from royal_game.modules.board import Board
from royal_game.modules.player import Player

logging.basicConfig(filename="games.log", filemode="w", format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


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
        self.white_turn = True

    def play(self) -> bool:
        """
        Implement the game loop.

        1, roll dices. If 0, skip to 5
        2, send available moves to player
        3, player returns selected move
        4, update board
        5, determine who has the next turn

        Return true if white wins, and vice versa
        """
        # pre-game output, player names etc.

        while not self.board.is_end_state():
            dice_roll = choices(
                [0, 1, 2, 3, 4], weights=[1 / 16, 1 / 4, 3 / 8, 1 / 4, 1 / 16], k=1
            )

            if dice_roll == 0:
                logger.info(
                    "%s rolled a zero. The turn is automatically passed",
                    self.player1 if self.white_turn else self.player2,
                )
                self.white_turn = not self.white_turn
                continue

            available_moves = self.board.get_available_moves(self.white_turn, dice_roll)
            move_selected = (
                self.player1.select_move(self.board, available_moves)
                if self.white_turn
                else self.player2(self.board, available_moves)
            )

            try:
                logger.info(move_selected)
                self.board.make_move(move_selected)
            except InvalidMove as e:
                logger.critical(move_selected)
                raise e

            if not move_selected.is_rosette:
                self.white_turn = not self.white_turn

        # end of game output, results + any metadata
