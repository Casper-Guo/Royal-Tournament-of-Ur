"""
Implements the game logic via Board class.

Grids denoted as follows:

white (W):  W4 W3 W2 W1 WS WE  W14  W13
public:      5  6  7  8  9 10   11   12
black (B):  B4 B3 B2 B1 BS BE  B14  B13
"""

from itertools import chain

from royal_game._constants import (
    black_grid_iter,
    black_order_iter,
    board_order_iter,
    public_grid_iter,
    start_end_grid_iter,
    white_grid_iter,
    white_order_iter,
)
from royal_game._exceptions import InvalidNumberofPieces
from royal_game.modules.grid import Grid, StartEndGrid
from royal_game.modules.grid_status import GridStatus
from royal_game.modules.move import Move


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

    white_rosettes = set(["W4", "8", "W14"])
    black_rosettes = set(["B4", "8", "B14"])

    def __init__(self, seed: int = 122138132480, no_verify: bool = False) -> None:
        self.board: dict[str, Grid] = {}
        white_total = 0
        black_total = 0

        # initialize the white row
        offset = 0
        for name, is_rosette in white_grid_iter():
            status_bit = (seed & (0b1 << offset)) >> offset
            offset += 1

            if status_bit:
                white_total += 1

            # simplified expression since GridStatus(1) indicates white
            self.board[name] = Grid(name, is_rosette, GridStatus(status_bit))

        # initialize the black row
        for name, is_rosette in black_grid_iter():
            status_bit = (seed & (0b1 << offset)) >> offset
            offset += 1

            if status_bit:
                black_total += 1

            self.board[name] = Grid(
                name, is_rosette, GridStatus(2) if status_bit else GridStatus(0)
            )

        # initialize public row
        for name, is_rosette in public_grid_iter():
            status_bit = (seed & (0b11 << offset)) >> offset

            if status_bit == 1:
                white_total += 1
            elif status_bit == 2:
                black_total += 1

            offset += 2
            self.board[name] = Grid(name, is_rosette, GridStatus(status_bit))

        # offset = 28 now
        for name in start_end_grid_iter():
            num_pieces = (seed & (0b111 << offset)) >> offset
            offset += 3
            self.board[name] = StartEndGrid(name, num_pieces)

        if not no_verify:
            white_total += self.board["WS"].num_pieces + self.board["WE"].num_pieces
            black_total += self.board["BS"].num_pieces + self.board["BE"].num_pieces

            if white_total != 7:
                raise InvalidNumberofPieces("white", white_total)

            if black_total != 7:
                raise InvalidNumberofPieces("black", black_total)

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
        """
        Recalculate the integer representation since the board may be modified.

        Grid objects are converted to integers based on the value of their status.
        This is the desired behavior for the public grids but not the private grids.
        """
        board_int = 0
        offset = 0

        for name, _ in chain(white_grid_iter(), black_grid_iter()):
            board_int += int(self.board[name].status != GridStatus.empty) << offset
            offset += 1

        for name, _ in public_grid_iter():
            board_int += (int(self.board[name])) << offset
            offset += 2

        for name in start_end_grid_iter():
            board_int += (int(self.board[name])) << offset
            offset += 3

        return board_int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Board):
            return NotImplemented
        return self.__int__() == other.__int__()

    def __hash__(self) -> int:
        return self.__int__()

    def is_end_state(self):
        """
        Check if the board is at an end state.

        An end state is a state where at least one of the players has moved
        all 7 pieces to the end grid.
        """
        return self.board["BE"].num_pieces == 7 or self.board["WE"].num_pieces == 7

    def get_available_moves(self, white_turn: bool, dice_roll: int) -> tuple[Move]:
        """
        Return a tuple of valid moves.

        Requires dice_roll to be non-negative.
        """
        assert dice_roll > 0
        own_status = GridStatus.white if white_turn else GridStatus.black
        other_status = GridStatus.black if white_turn else GridStatus.white
        start_grid = "WS" if white_turn else "BS"
        end_grid = "WE" if white_turn else "BE"
        rosette_grids = Board.white_rosettes if white_turn else Board.black_rosettes
        grid_iterator = white_order_iter if white_turn else black_order_iter
        # convert the iterator to a list so it can be indexed
        grids = list(grid_iterator())

        available_moves = []

        # dice_roll of 1 means moving the piece onto the grid at index 0
        # need to apply a correction of 1
        if (
            self.board[grids[dice_roll - 1]].status is GridStatus.empty
            and self.board[start_grid].num_pieces > 0
        ):
            available_moves.append(
                Move(start_grid, grids[dice_roll - 1], is_onboard=True, no_verify=True)
            )
        if self.board[grids[-dice_roll]].status is own_status:
            available_moves.append(
                Move(grids[-dice_roll], end_grid, is_ascension=True, no_verify=True)
            )

        # the length of grids is always 14
        for i in range(14 - dice_roll):
            # check for valid move from grid1 to grid2
            grid1, grid2 = self.board[grids[i]], self.board[grids[i + dice_roll]]
            if grid1.status is own_status:
                if grid2.status is other_status:
                    # handle middle rosette special case
                    if grid2.name != "8":
                        available_moves.append(
                            Move(grid1.name, grid2.name, is_capture=True, no_verify=True)
                        )
                    elif grid2.name == "8" and self.board["9"].status is GridStatus.empty:
                        available_moves.append(Move(grid1.name, "9", no_verify=True))
                elif grid2.status is GridStatus.empty:
                    if grid2.name in rosette_grids:
                        available_moves.append(
                            Move(grid1.name, grid2.name, is_rosette=True, no_verify=True)
                        )
                    else:
                        available_moves.append(Move(grid1.name, grid2.name, no_verify=True))

        return tuple(available_moves)

    def make_move(self, move: Move) -> None:
        """Modify the board based on the board."""
        if move.is_onboard:
            self.board[move.grid1].num_pieces -= 1
            if move.grid1 == "WS":
                self.board[move.grid2].status = GridStatus.white
            elif move.grid1 == "BS":
                self.board[move.grid2].status = GridStatus.black
        elif move.is_capture:
            if self.board[move.grid2].status is GridStatus.white:
                self.board["WS"].num_pieces += 1
            if self.board[move.grid2].status is GridStatus.black:
                self.board["BS"].num_pieces += 1

            self.board[move.grid2].status = self.board[move.grid1].status
            self.board[move.grid1].status = GridStatus.empty
        elif move.is_ascension:
            self.board[move.grid1].status = GridStatus.empty
            self.board[move.grid2].num_pieces += 1
        else:
            self.board[move.grid2].status = self.board[move.grid1].status
            self.board[move.grid1].status = GridStatus.empty
