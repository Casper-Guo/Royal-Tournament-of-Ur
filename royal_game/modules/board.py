"""
Implements the game logic via Board class.

Grids denoted as follows:

white (W):  W4 W3 W2 W1 WS WE  W14  W13
public:      5  6  7  8  9 10   11   12
black (B):  B4 B3 B2 B1 BS BE  B14  B13
"""

from itertools import chain

from royal_game._constants import (
    black_iter,
    board_order_iter,
    public_iter,
    start_end_iter,
    white_iter,
)
from royal_game._exceptions import InvalidNumberofPieces
from royal_game.modules.grid import Grid, StartEndGrid
from royal_game.modules.grid_status import GridStatus


class Board:
    """
    Stores game state and implements game logic.

    Each board can be uniquely represented in 40 bits
    via the following mapping.

    bit 0-5: one bit each for W1...W14 indicating
    whether the grid is occupied
    bit 6-11: one bit each for B1...B14 indicating
    whether the grid is occupied
    bit 12-27: two bit each for 5...12 indicating
    whether the grid is empty, white, or black
    bit 28-39: three bit each for WS, WE, BS, BE
    indicating number of pieces at start/end

    122138132480 = (7 << 28) + (7 << 34)
    """

    def __init__(self, seed: int = 122138132480) -> None:
        self.board: dict[str, Grid] = {}

        # initialize the white row
        offset = 0
        for name, is_rosette in white_iter():
            status_bit = (seed & (0b1 << offset)) >> offset
            offset += 1

            # simplified expression since GridStatus(1) indicates white
            self.board[name] = Grid(name, is_rosette, GridStatus(status_bit))

        # initialize the black row
        for name, is_rosette in black_iter():
            status_bit = (seed & (0b1 << offset)) >> offset
            offset += 1
            self.board[name] = Grid(
                name, is_rosette, GridStatus(2) if status_bit else GridStatus(0)
            )

        # initialize public row
        for name, is_rosette in public_iter():
            status_bit = (seed & (0b11 << offset)) >> offset
            offset += 2
            self.board[name] = Grid(name, is_rosette, GridStatus(status_bit))

        # offset = 28 now
        for name in start_end_iter():
            num_pieces = (seed & (0b111 << offset)) >> offset
            offset += 3
            self.board[name] = StartEndGrid(num_pieces, name)

        self.verify_board()

    def __repr__(self):
        fmt = ""
        unformatted = ""

        for i, name in enumerate(board_order_iter()):
            unformatted += str(self.board[name])
            if i % 8 == 7:
                # take every third row in unformatted, remove newline character,
                # and put into a list
                format_row = [
                    [row.replace("\n", "") for row in unformatted.split("\n")][start::3]
                    for start in range(3)
                ]

                # join the three separate lists into single rows, and then join these rows
                format_row = "\n".join(list(map(lambda x: " ".join(x), format_row)))
                fmt += format_row + "\n"
                unformatted = ""

        return fmt

    def __int__(self) -> int:
        board_int = 0
        offset = 0

        for name, _ in chain(white_iter(), black_iter()):
            board_int += (int(self.board[name])) << offset
            offset += 1

        for name, _ in public_iter():
            board_int += (int(self.board[name])) << offset
            offset += 2

        for name in start_end_iter():
            board_int += (int(self.board[name])) << offset
            offset += 3

        return board_int

    def verify_board(self) -> bool:
        """Check if the board has the correct number of total pieces."""
        white_total = 0
        black_total = 0

        for name, _ in chain(white_iter(), public_iter()):
            if self.board[name].status is GridStatus.white:
                white_total += 1

        white_total += self.board["WS"].num_pieces + self.board["WE"].num_pieces

        if white_total != 7:
            raise InvalidNumberofPieces("white", white_total)

        for name, _ in chain(black_iter(), public_iter()):
            if self.board[name].status is GridStatus.black:
                black_total += 1

        black_total += self.board["BS"].num_pieces + self.board["BE"].num_pieces

        if black_total != 7:
            raise InvalidNumberofPieces("black", black_total)

    def is_end_state(self):
        """
        Check if the board is at an end state.

        An end state is a state where at least one of the players has moved
        all 7 pieces to the end grid.
        """
        return self.board["BE"].num_pieces == 7 or self.board["WE"].num_pieces == 7
