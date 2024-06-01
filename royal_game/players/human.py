"""An example player implementation that also serves as a dummy for testing."""

from typing import Iterable

from royal_game.modules.board import Board
from royal_game.modules.move import Move
from royal_game.modules.player import Player


class Human(Player):
    """You must implement the select_move method!"""  # noqa: D400

    def __init__(self, name: str):
        """Initialize the human player with a name."""
        super().__init__(name)

    def select_move(
        self, board: Board, available_moves: Iterable[Move], white_turn: bool
    ) -> Move:
        """Print available moves and take player input."""
        for i, move in enumerate(available_moves):
            print(f"{i+1}: {move.__repr__()}")

        while True:
            player_selection = input("Please select a move: ")
            try:
                player_selection = int(player_selection)
            except ValueError:
                # catch non-int input strings
                continue

            if 1 <= player_selection <= len(available_moves):
                return available_moves[player_selection - 1]
