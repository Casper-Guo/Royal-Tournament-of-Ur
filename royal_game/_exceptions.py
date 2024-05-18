"""Custom exception types."""

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
    def __init__(self, player) -> None:
        """
        player is a Player class object.
        
        Annotating this type is impossible due to circular imports.
        """

        message = f"Player {player.name} has not implemented select_move."
        super().__init__(message)

class MoveError(Exception):
    pass

# ImpossibleMove denotes a move that is invalid in any circumstances
# InvalidMove denotes a move that is invalid on a specific board
class ImpossibleMove(MoveError):
    def __init__(self) -> None:
        super().__init__("The requested move is impossible.")

class InvalidMove(MoveError):
    def __init__(self) -> None:
        super().__init__("This move is invalid.")