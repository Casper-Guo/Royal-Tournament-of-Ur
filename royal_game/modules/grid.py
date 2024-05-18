"""Implements individual grids on the game board."""

from royal_game._constants import black_piece, rosette, white_piece
from royal_game._exceptions import InvalidNumPieces
from royal_game.modules.grid_status import GridStatus


class Grid:
    """Base class that represents non-start/end grids."""

    def __init__(
        self, name: str, is_rosette: bool, status: GridStatus = GridStatus.empty
    ) -> None:
        self.status = status
        self.name = name
        self.is_rosette = is_rosette

    def __str__(self) -> str:
        symbol = " "
        if self.status is GridStatus.empty:
            if self.is_rosette:
                symbol = rosette
        else:
            symbol = white_piece if self.status is GridStatus.white else black_piece

        return f"---\n|{symbol}|\n---\n"

    def __repr__(self) -> str:
        return f"Grid({self.name}, {self.is_rosette}, {self.status})"

    def __int__(self) -> int:
        return self.status.value


class StartEndGrid(Grid):
    """Starting grid."""

    def __init__(self, num_pieces: int, name: str) -> None:
        super().__init__(name, is_rosette=False)
        if num_pieces < 0 or num_pieces > 7:
            raise InvalidNumPieces(num_pieces)
        self.num_pieces = num_pieces

    def __str__(self) -> str:
        return f"   \n {self.num_pieces} \n   \n"

    def __repr__(self) -> str:
        return f"StartEndGrid({self.num_pieces}, {self.name})"

    def __int__(self) -> int:
        return self.num_pieces
