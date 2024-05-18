"""Class for representing move options."""

from royal_game._constants import ascension, capture, rosette
from royal_game._exceptions import ImpossibleMove


class Move:
    """Move representation and benchmarking metadata."""

    def __init__(
        self,
        grid1: str,
        grid2: str,
        is_rosette: bool = False,
        is_capture: bool = False,
        is_ascension: bool = False,
        is_onboard: bool = False,
        no_verify: bool = False,
    ) -> None:
        self.grid1 = grid1
        self.grid2 = grid2
        self.is_rosette = is_rosette
        self.is_capture = is_capture
        self.is_ascension = is_ascension
        self.is_onboard = is_onboard

        # set no_verify to avoid repeat validation in game scenarios
        # all moves generated should be assumed valid
        if not no_verify:
            self.verify_move()

    def __str__(self) -> str:
        return (
            f"Move the piece on {self.grid1} to {self.grid2} "
            f"{rosette if self.is_rosette else ''}{capture if self.is_capture else ''}"
            f"{ascension if self.is_ascension else ''}"
        )

    def __repr__(self) -> str:
        return (
            f"{self.grid1} -> {self.grid2} {rosette if self.is_rosette else ''}"
            f"{capture if self.is_capture else ''}{ascension if self.is_ascension else ''}"
        )

    # It would be a nice QoL improvement to implement a full partial order
    # so moves can be reasonably sorted
    # Not urgent due to minimal player interaction and need for nice interface
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Move):
            return NotImplemented
        return self.grid1 == other.grid1 and self.grid2 == other.grid2

    def verify_move(self) -> None:
        """Check move validity."""
        try:
            if int(self.is_rosette) + int(self.is_capture) + int(self.is_ascension) > 1:
                raise ImpossibleMove
            if self.grid1 == self.grid2:
                raise ImpossibleMove
            if (self.grid1[0] == "W" and self.grid2[0] == "B") or (
                self.grid1[0] == "B" and self.grid2[0] == "W"
            ):
                raise ImpossibleMove
            if self.is_onboard and self.grid1 not in ("WS", "BS"):
                raise ImpossibleMove
            if self.is_ascension and self.grid2 not in ("WE", "BE"):
                raise ImpossibleMove
            if self.is_rosette and self.grid2 not in ("W4", "B4", "8", "W14", "B14"):
                raise ImpossibleMove
        except ImpossibleMove as e:
            print(self)
            raise e
