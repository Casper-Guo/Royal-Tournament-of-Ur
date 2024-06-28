"""
CLI for benchmarking player agents against each other.

Accepts player implementations as arguments and play them
against each other pairwise.
"""

import logging
import random
from collections import defaultdict
from itertools import combinations, combinations_with_replacement
from pathlib import Path
from typing import Iterable

import click

from royal_game.modules.game import Game

logging.basicConfig(format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def filename_to_class_name(filename: str) -> str:
    """Convert snake class filename to capitalized camel case class name."""
    return "".join([word.capitalize() for word in filename.split("_")])


def output_results(num_wins: defaultdict, num_games: int, self_play: bool) -> None:
    """Format tournament results nicely."""
    print(f"{'TOURNAMENT RESULTS':_^120}")
    player_names = list(num_wins.keys())

    # list player names in the top row of the table
    print("".join([f"{name:^20}" for name in ([""] + player_names)]))

    for name1 in player_names:
        # list player names in the first column of the table
        # for a scoring matrix look
        table_row = f"{name1:^20}"
        for name2 in player_names:
            if name1 == name2 and not self_play:
                table_row += f"{'/':^20}"
            else:
                win_percentage = f"{num_wins[name1][name2]}/{num_games}"
                table_row += f"{win_percentage:^20}"
        print(table_row)


@click.command()
@click.argument("players", nargs=-1, type=click.Path(exists=True, path_type=Path))
@click.option(
    "-n",
    "--num-games",
    default=1000,
    type=int,
    help="Number of games to simulate between each pair of players.",
)
@click.option(
    "-s",
    "--board-seed",
    default=122138132480,
    type=int,
    help=(
        "Use a non-default initial board. "
        "Board representation layout is documented in royal_game.modules.board."
    ),
)
@click.option("-b", "--binary-seed", is_flag=True, help="Interpret the seed argument as binary")
@click.option(
    "-r",
    "--random-seed",
    default=None,
    type=int,
    help="Optionally set a random seed for reproducibility.",
)
@click.option("-p", "--self-play", is_flag=True)
@click.option(
    "-f",
    "--full-output",
    is_flag=True,
    help="Enable saving full debug output to games.log in addition to summary statistics",
)
def main(
    players: Iterable[Path],
    num_games: int,
    board_seed: int,
    binary_seed: bool,
    random_seed: int,
    self_play: bool,
    full_output: bool,
):
    """Implement tournament runner."""
    if not full_output:
        logging.getLogger("royal_game.modules.game").setLevel(logging.INFO)
    if binary_seed:
        board_seed = int(str(board_seed), 2)
    if random_seed is not None:
        random.seed(random_seed)

    player_classes = []
    for player in players:
        try:
            exec(
                (
                    f"from royal_game.players.{player.stem} import "
                    f"{filename_to_class_name(player.stem)}"
                )
            )
            player_classes.append(eval(filename_to_class_name(player.stem)))
        except ImportError:
            logger.critical("Unable to import from %s.", player.stem)
            logger.info(
                "Your player subclass should be named %s.", filename_to_class_name(player.stem)
            )

    num_wins = defaultdict(lambda: defaultdict(int))
    iterator = (
        combinations(player_classes, 2)
        if not self_play
        else combinations_with_replacement(player_classes, 2)
    )
    for player1, player2 in iterator:
        for _ in range(num_games):
            game = Game(player1(), player2(), board_seed)
            if game.play():
                # player1 wins
                num_wins[str(game.player1)][str(game.player2)] += 1
            else:
                if player1 != player2:
                    # only log white wins in self-play
                    # black wins are implied
                    num_wins[str(game.player2)][str(game.player1)] += 1

    output_results(num_wins, num_games, self_play)


if __name__ == "__main__":
    main()
