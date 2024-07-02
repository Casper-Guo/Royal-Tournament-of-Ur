"""
Translate Rust board seed to Python board seed.

Note the following assumption is not valid:

    python_to_rust(rust_to_python(rust_seed)) == rust_seed

This property is only guaranteed for the first 62 bits.

However, this assumption is valid:

    rust_to_python(python_to_rust(py_seed)) == py_seed
"""

import logging
from pathlib import Path

import click

from royal_game._constants import black_order_iter, white_order_iter
from royal_game._exceptions import BoardError
from royal_game.modules.board import Board

logging.basicConfig(format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def rust_to_python(rust_seed: int, verify: bool = True) -> int:
    """
    Rust board encoding schema copied below.

    Two bits each for board grids to achieve consistency in the order of
    W1...W4, 5...12, W13, W14, B1...B4, 5...12, B13, B14 (from least to most significant).
    Note the more significant bit of private grids are unused (56 total)

    Three bits each for WS and BS from the least to the most significant (6 total)

    Bits 62-63 indicate the endgame state.
    This is useful for stopping search and assigning rewards.
        00: not set/calculated
        01: white win
        10: black win
        11: in progress
    """
    if verify:
        assert (rust_seed & (0xFFFF << 8)) >> 8 == (
            rust_seed & (0xFFFF << 36)
        ) >> 36, f"{rust_seed}"

    py_seed = 0
    white_total, black_total = 0, 0

    for py_offset, rust_offset in enumerate((0, 2, 4, 6, 24, 26)):
        if ((rust_seed & (0b11 << rust_offset)) >> rust_offset) == 0b01:
            white_total += 1
            py_seed += 1 << py_offset

    for py_offset, rust_offset in enumerate((28, 30, 32, 34, 52, 54)):
        if ((rust_seed & (0b11 << rust_offset)) >> rust_offset) == 0b10:
            black_total += 1
            py_seed += 1 << (py_offset + 6)

    for py_offset, rust_offset in zip(range(12, 28, 2), range(8, 24, 2)):
        grid_status = (rust_seed & (0b11 << rust_offset)) >> rust_offset
        py_seed += grid_status << py_offset

        if grid_status == 0b01:
            white_total += 1
        elif grid_status == 0b10:
            black_total += 1

    num_ws = (rust_seed & (0b111 << 56)) >> 56
    py_seed += num_ws << 28
    num_bs = (rust_seed & (0b111 << 59)) >> 59
    py_seed += num_bs << 34

    # WE
    py_seed += (7 - white_total - num_ws) << 31
    # BE
    py_seed += (7 - black_total - num_bs) << 37

    if verify:
        try:
            _ = Board(py_seed)
        except BoardError as e:
            logger.warning("Provided rust seed %d is invalid.", rust_seed)
            raise e

    return py_seed


def python_to_rust(py_seed: int, verify: bool = True) -> int:
    """
    Python board encoding schema copied below.

    bit 0-5: one bit each for W1...W14 indicating
    whether the grid is occupied
    bit 6-11: one bit each for B1...B14 indicating
    whether the grid is occupied
    bit 12-27: two bit each for 5...12 indicating
    whether the grid is empty, white, or black
    bit 28-39: three bit each for WS, WE, BS, BE
    indicating number of pieces at start/end

    The endgame state bits will always be set. Thus the following assumption
    is not valid:

        python_to_rust(rust_to_python(rust_seed)) == rust_seed

    Only compare the lower 62 bits if needed.
    """
    if verify:
        try:
            _ = Board(py_seed)
        except BoardError as e:
            logger.warning("Provided python seed %d is invalid.", py_seed)
            raise e

    board = Board(py_seed, no_verify=True)
    rust_seed = 0

    if board.board["WE"].num_pieces == 7:
        rust_seed += 0b01 << 62
    elif board.board["BE"].num_pieces == 7:
        rust_seed += 0b10 << 62
    else:
        rust_seed += 0b11 << 62

    rust_seed += int(board.board["WS"]) << 56
    rust_seed += int(board.board["BS"]) << 59

    for grid, offset in zip(list(white_order_iter()), range(0, 28, 2)):
        # we can take this shortcut because GridStatus(1) indicates white
        # which match the status bit for an occupied white private grid
        rust_seed += int(board.board[grid]) << offset

    for grid, offset in zip(list(black_order_iter()), range(28, 56, 2)):
        rust_seed += int(board.board[grid]) << offset

    return rust_seed


@click.command()
@click.option("--python-seeds/--rust-seeds", "-p/-r", required=True)
@click.option("--binary-output", "-b", is_flag=True, default=False)
@click.option("--verify/--no-verify", default=True)
@click.argument("in_file", type=click.Path(exists=True, path_type=Path))
@click.argument("out_file", type=click.Path(path_type=Path))
def main(python_seeds: bool, binary_output: bool, verify: bool, in_file: Path, out_file: Path):
    """
    Implement batch translation of seeds.

    Input file should contain seeds in decimal encoding with one on each line.
    """
    translator = python_to_rust if python_seeds else rust_to_python

    with open(in_file, mode="r") as fin, open(out_file, mode="w+") as fout:
        for line in fin:
            seed = int(line.strip())
            translated = translator(seed, verify=verify)

            if binary_output:
                translated = f"{translated:0>64b}" if python_seeds else f"{translated:0>40b}"

            fout.write(f"{translated}\n")


if __name__ == "__main__":
    main()
