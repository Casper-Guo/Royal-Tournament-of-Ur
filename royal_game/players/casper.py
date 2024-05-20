"""Casper's heuristics."""

from random import randint
from typing import Iterable

from royal_game.modules.board import Board
from royal_game.modules.grid_status import GridStatus
from royal_game.modules.move import Move
from royal_game.modules.player import Player


class Casper(Player):
    """You must implement the select_move method!"""  # noqa: D400

    def __init__(self):
        """Choose a name for your player."""
        name = "Casper's heuristics"
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
        # convert to list so moves can be eliminated from consideration
        available_moves = list(available_moves)

        # always claim center rosette when possible
        for move in available_moves:
            if move.grid2 == "8":
                return move

        # filter out all moves away from the center rosette unless
        # there are no other options
        if len(available_moves) > 1:
            available_moves = [move for move in available_moves if move.grid1 != "8"]
        else:
            return available_moves[0]

        # otherwise always rosette when possible
        for move in available_moves:
            if move.is_rosette:
                return move

        white_at_back, black_at_back = 0, 0

        for name in ["W1", "W2", "W3", "W4"]:
            if board.board[name].status is GridStatus.white:
                white_at_back += 1
        for name in ["B1", "B2", "B3", "B4"]:
            if board.board[name].status is GridStatus.black:
                black_at_back += 1

        # if the opponent has more pieces on private tiles
        # then prioritize moving pieces onto the board
        if (white_turn and black_at_back > white_at_back) or (
            not white_turn and white_at_back > black_at_back
        ):
            for move in available_moves:
                if move.is_onboard:
                    return move

        # if no better moves are available, then captures whenever possible
        for move in available_moves:
            if move.is_capture:
                return move

        # fall back to moving randomly
        return available_moves[randint(0, len(available_moves) - 1)]
