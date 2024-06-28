"""Display board from input seeds."""

import logging
from pathlib import Path
from typing import Optional

import click

from royal_game._exceptions import BoardError
from royal_game.modules.board import Board

logging.basicConfig(format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def process_input(seed: str, decimal: bool) -> Board | None:
    """Produce board from input seed string."""
    try:
        seed = int(seed, 10 if decimal else 2)
    except ValueError as e:
        logger.warning(e)
        return None

    try:
        board = Board(seed)
    except BoardError as e:
        logger.warning(e)
        board = Board(seed, no_verify=True)
    finally:
        return board


@click.command()
@click.option("--decimal/--binary", "-d/-b", default=True)
@click.argument("in_file", required=False, type=click.Path(exists=True, path_type=Path))
def main(decimal: bool, in_file: Optional[Path]):
    """
    Accept seed input from user or file and display the corresponding boards.

    If an input file is provided, decimal encoding is assumed. The file should
    contain one seed per line.

    Warnings are shown for invalid boards but the program will not terminate.
    """
    if in_file is not None:
        decimal = True
        with open(in_file, "r") as fin:
            seeds = [line.strip() for line in fin.readlines()]

        for seed in seeds:
            board = process_input(seed, decimal)
            if board is not None:
                print(f"{seed}:\n{board}")

    else:
        user_input = ""
        while user_input != "quit":
            user_input = input("Enter a board seed in the chosen encoding: ")
            board = process_input(user_input, decimal)
            if board is not None:
                print(board)


if __name__ == "__main__":
    main()
