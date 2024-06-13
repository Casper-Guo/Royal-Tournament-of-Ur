"""Translate Rust board seed to Python board seed."""

from royal_game._exceptions import BoardError
from royal_game.modules.board import Board


def translate(rust_seed: int, verify: bool = True) -> int:
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
            print(f"Provided rust seed {rust_seed} is invalid.")
            raise e

    return py_seed
