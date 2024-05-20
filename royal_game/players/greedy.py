"""A greedy player that always ascends, then rosettes, then captures."""

from random import randint
from typing import Iterable

from royal_game.modules.board import Board
from royal_game.modules.move import Move
from royal_game.modules.player import Player


class Greedy(Player):
    """You must implement the select_move method!"""  # noqa: D400

    def __init__(self):
        """Choose a name for your player."""
        name = "Greedy player"
        super().__init__(name)

    def select_move(
        self, board: Board, available_moves: Iterable[Move], white_turn: bool
    ) -> Move:
        """
        Select a move based on some heuristic.

        The complete board state can be accessed through board.board by indexing
        with the name of the grids. The grid representation is reproduced below:

        white (W):  W4 W3 W2 W1 WS WE  W14  W13
        public:      5  6  7  8  9 10   11   12
        black (B):  B4 B3 B2 B1 BS BE  B14  B13

        You can determine the side you are playing for via the white_turn argument.

        The dummy always return the first available move.
        """
        # Takes an ascension whenever it is available
        for move in available_moves:
            if move.is_ascension:
                return move
        # Then tries to claim a rosette
        for move in available_moves:
            if move.is_rosette:
                return move
        # Then tries to capture enemy pieces
        for move in available_moves:
            if move.is_capture:
                return move
        # If none of these options are available, select a move randomly
        return available_moves[randint(0, len(available_moves) - 1)]
