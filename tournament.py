"""CLI for benchmarking player agents against each other."""

from royal_game.modules.game import Game
from royal_game.players.dummy import Dummy

game = Game(Dummy(), Dummy())
game.play()
