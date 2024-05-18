"""An example player implementation."""

from royal_game.modules.player import Player
from typing import Iterable
from royal_game.modules.board import Board
from royal_game.modules.move import Move

class SamplePlayer(Player):
    """You must implement the select_move method!"""
    def __init__(self):
        """choose a name for your player"""
        super().__init__("{name goes here}")
    def select_move(self, board: Board, available_moves: Iterable[Move]) -> Move:
        """
        Select a move based on some heuristic.
        
        The complete board state can be accessed through board.board by indexing
        with the name of the grids. The grid representation is reproduced below:
        
        white (W):  W4 W3 W2 W1 WS WE  W14  W13
        public:      5  6  7  8  9 10   11   12
        black (B):  B4 B3 B2 B1 BS BE  B14  B13
        """
        pass
