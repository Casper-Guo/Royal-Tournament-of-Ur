# royal-tournament-of-ur
Interface for benchmarking agents and heuristics for the royal game of Ur tournament-style

## Setup
Install with `pip install -e .`

## Add Your Own Player
See `/royal_game/players/dummy.py` for a template to implement your own player/heuristics. Place it in the same directory. File name should use snake case and your player class name should be identical except in camel case with the first letter capitalized.

## Tournament Interface
Running with all default options:

`python3 tournament.py royal_game/players/greedy.py royal_game/players/rng.py `

Output:

```
___________________________________________________TOURNAMENT RESULTS___________________________________________________
                       Greedy player       Random player    
   Greedy player             /                963/1000      
   Random player          37/1000                /    
```

Run `python3 tournament.py --help` to see all available options.

## Todo
Create workflow to automatically benchmark players submitted via PR of a certain label against all existing players.