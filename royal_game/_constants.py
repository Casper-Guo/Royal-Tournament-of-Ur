"""String constants."""

from itertools import chain
from typing import Iterator

rosette = "\U0001f3f5"
white_piece = "\U000025cb"
black_piece = "\U000025cf"
capture = "\U00002694"
ascension = "\U0001f680"

"""
The grid_iter objects contain all information needed for
creating Grid objects.

The other iterators yield names only.
"""


def white_grid_iter() -> Iterator[tuple[str, bool]]:
    yield from [
        ("W1", False),
        ("W2", False),
        ("W3", False),
        ("W4", True),
        ("W13", False),
        ("W14", True),
    ]


def black_grid_iter() -> Iterator[tuple[str, bool]]:
    yield from [
        ("B1", False),
        ("B2", False),
        ("B3", False),
        ("B4", True),
        ("B13", False),
        ("B14", True),
    ]


def public_grid_iter() -> Iterator[tuple[str, bool]]:
    yield from [
        ("5", False),
        ("6", False),
        ("7", False),
        ("8", True),
        ("9", False),
        ("10", False),
        ("11", False),
        ("12", False),
    ]


def start_end_grid_iter() -> Iterator[str]:
    yield from ["WS", "WE", "BS", "BE"]


def white_order_iter() -> Iterator[str]:
    yield from chain.from_iterable(
        [["W1", "W2", "W3", "W4"], [name for name, _ in public_grid_iter()], ["W13", "W14"]]
    )


def black_order_iter() -> Iterator[str]:
    yield from chain.from_iterable(
        [["B1", "B2", "B3", "B4"], [name for name, _ in public_grid_iter()], ["B13", "B14"]]
    )


def board_order_iter() -> Iterator[str]:
    yield from [
        "W4",
        "W3",
        "W2",
        "W1",
        "WS",
        "WE",
        "W14",
        "W13",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "B4",
        "B3",
        "B2",
        "B1",
        "BS",
        "BE",
        "B14",
        "B13",
    ]
