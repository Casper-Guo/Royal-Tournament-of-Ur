"""Enum class for representing grid status."""

from enum import Enum


class GridStatus(Enum):
    """
    Grid status definitions.

    Although (-1, 0, 1) might be a more natural representation
    of the three different states, it presents problem when Grids
    are converted to two-bit ints.
    """

    empty = 0
    white = 1
    black = 2
