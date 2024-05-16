"""Custom exception types."""

from royal_game.modules.player import Player

class GridError(Exception):
    pass

class InvalidNumPieces(GridError):
    def __init__(self, num_pieces: int) -> None:
        message = (
            f"{num_pieces} is not a valid number of pieces,"
            " the valid range is [0, 7]."
        )
        super().__init__(message)
        
class BoardError(Exception):
    pass

class InvalidNumberofPieces(BoardError):
    def __init__(self, color: str, num_pieces: int) -> None:
        message = (
            f"Invalid total number of {color} pieces " 
            f"(7 expected, {num_pieces} actual)."
        )
        super().__init__(message)
        
class GameError(Exception):
    pass

class InvalidPlayer(GameError):
    def __init__(self, player: Player) -> None:
        message = f"Player {player.name} has not implemented select_move."
        super().__init__(message)

class MoveError(Exception):
    pass

class ImpossibleMove(MoveError):
    def __init__(self) -> None:
        super().__init__(f"The requested move is impossible.")