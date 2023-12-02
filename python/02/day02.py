"""
Advent of Code
Day 2
Cube Conundrum
jramaswami
"""


import functools
import operator


def parse_input(input):
    "Parse input into a list of lists of ..."
    games = []
    for line in input:
        games.append([])
        # Parse game number and game rounds
        game_clause, line = (t.strip() for t in line.split(':'))
        game_number = game_clause.split()[-1][:-1]
        # Parse game rounds
        game_rounds = (t.strip() for t in line.split(';'))
        for round in game_rounds:
            games[-1].append([])
            for draw in (t.strip() for t in round.split(',')):
                number_drawn, color_drawn = draw.split()
                number_drawn = int(number_drawn)
                games[-1][-1].append((number_drawn, color_drawn))
    return games


def is_game_possible(game):
    "Return True if the game is possible with the cubes available."
    cubes={'red': 12, 'green': 13, 'blue': 14}
    for round in game:
        for number_drawn, color_drawn in round:
            if number_drawn > cubes[color_drawn]:
                return False
    return True


def max_cubes_needed(game):
    "Return the maximum number of cubes needed to play the game."
    cubes = {'red': 0, 'green': 0, 'blue': 0}
    for round in game:
        for number_drawn, color_drawn in round:
            cubes[color_drawn] = max(cubes[color_drawn], number_drawn)
    return cubes


def main():
    "Main program"
    import sys
    import pyperclip
    games = parse_input(sys.stdin)
    soln_a = sum([i for i, g in enumerate(games, start=1) if is_game_possible(g)])
    print('The sum of IDs of possible games is', soln_a)
    assert soln_a == 2486
    soln_b = sum(functools.reduce(operator.mul, max_cubes_needed(g).values(), 1) for g in games)
    print('The sum of the power of the games is', soln_b)
    assert soln_b == 87984
    pyperclip.copy(str(soln_b))


if __name__ == '__main__':
    main()