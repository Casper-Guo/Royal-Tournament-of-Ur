"""Implements player interface."""


class Player:
    """Player evaluates board state and selects from available actions."""

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name
