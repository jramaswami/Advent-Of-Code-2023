"""
Advent of Code
Day 5
If You Give A Seed A Fertilizer
jramaswami
"""


import collections


Entry = collections.namedtuple('Entry', ['next', 'curr', 'range'])


def parse_input(lines):
    "Parse input and return seeds and almanac"
    # Read seeds line.
    seeds_line = lines[0]
    # Parse seeds line.
    _, tokens = seeds_line.split(': ')
    seeds = tuple(int(t) for t in tokens.split())
    i = 2
    almanac = []
    while i < len(lines):
        # Header line.
        assert lines[i]
        # Create a new map for it.
        almanac.append([])
        i += 1
        while i < len(lines) and lines[i]:
            almanac[-1].append(Entry(*(int(t) for t in lines[i].split())))
            i += 1
        # Skip blank line
        i += 1
    return seeds, almanac


def transform_seed(seed, almanac):
    for t, transformation in enumerate(almanac):
        for entry in transformation:
            seed0 = seed
            if entry.curr <= seed < (entry.curr + entry.range):
                delta = seed - entry.curr
                seed = entry.next + delta
                break
    return seed


def solve_a(seeds, almanac):
    return min(transform_seed(seed, almanac) for seed in seeds)


def main():
    "Main program"
    import sys
    import pyperclip
    with open(sys.argv[1]) as infile:
        lines = [t.strip() for t in infile.readlines()]
    seeds, almanac = parse_input(lines)
    soln_a = solve_a(seeds, almanac)
    print('The lowest location number is', soln_a)
    assert soln_a == 261668924


if __name__ == '__main__':
    main()