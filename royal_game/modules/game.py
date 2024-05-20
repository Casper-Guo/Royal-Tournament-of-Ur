"""Implements game loop."""

import logging
from random import choices
from typing import Optional

from royal_game._exceptions import InvalidPlayer
from royal_game.modules.board import Board
from royal_game.modules.player import Player

logging.basicConfig(
    filename="games.log", filemode="w", level=logging.INFO, format="%(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)


class Game:
    """
    Simulates a game between two players.

    Each player should inherit from the Player class and
    implements select_move.
    """

    def __init__(self, player1: Player, player2: Player, board: Optional[Board] = None):
        if "select_move" not in dir(player1):
            raise InvalidPlayer(player1)

        if "select_move" not in dir(player2):
            raise InvalidPlayer(player2)

        self.player1 = player1
        self.player2 = player2

        if board is None:
            self.board = Board()
        else:
            self.board = board
        self.white_turn = True

    def __repr__(self):
        return (
            f"{self.player1} vs {self.player2}\n"
            f"It's {self.player1 if self.white_turn else self.player_2}'s turn.\n"
            f"{self.board}"
        )

    def play(self) -> bool:
        """Return true if white wins, and vice versa."""
        logger.info("%s is white.\n%s is black.", self.player1, self.player2)

        while not self.board.is_end_state():
            current_player = self.player1 if self.white_turn else self.player2
            dice_roll = choices(
                [0, 1, 2, 3, 4], weights=[1 / 16, 1 / 4, 3 / 8, 1 / 4, 1 / 16], k=1
            )[0]

            if dice_roll == 0:
                logger.info(
                    "%s rolled a zero. The turn is automatically passed", current_player
                )
                self.white_turn = not self.white_turn
                continue
            logger.info("%s rolled a %d.", current_player, dice_roll)

            available_moves = self.board.get_available_moves(self.white_turn, dice_roll)

            if not available_moves:
                logger.info(
                    "%s has no available moves. The turn is automatically passed",
                    current_player,
                )
                self.white_turn = not self.white_turn
                continue

            move_selected = current_player.select_move(self.board, available_moves)

            self.board.make_move(move_selected)
            logger.info("%s %s", current_player, move_selected)
            logger.info("\n%s", self.board)

            if not move_selected.is_rosette:
                self.white_turn = not self.white_turn

        # no other return statement needed since it is guaranteed that
        # one of the following two conditions is True
        if self.board.board["WE"].num_pieces == 7:
            logger.info("%s wins!", self.player1)
            return True
        if self.board.board["BE"].num_pieces == 7:  # noqa: RET503
            logger.info("%s wins!", self.player2)
            return False
