"""Enum class for representing grid status."""

from enum import Enum


class GridStatus(Enum):
    """Grid status definitions."""

    empty = 0
    white = 1
    black = -1
