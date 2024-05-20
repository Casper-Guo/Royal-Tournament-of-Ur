"""Implements player interface."""

from typing import Iterable

from royal_game.modules.board import Board
from royal_game.modules.move import Move


class Player:
    """Player evaluates board state and selects from available actions."""

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def select_move(
        self, board: Board, available_moves: Iterable[Move], white_turn: bool
    ) -> Move:
        """All subclasses must implement this method."""
        pass
