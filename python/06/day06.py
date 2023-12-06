"""
Advent of Code
Day 6
Wait For It
jramaswami
"""


import collections
import functools
import operator
import tqdm


Race = collections.namedtuple('Race', ['time', 'dist'])


def parse_input_a(lines):
    _, time_tokens = (t.strip() for t in lines[0].split(':'))
    times = [int (t) for t in time_tokens.split()]
    _, dist_tokens = (t.strip() for t in lines[1].split(':'))
    dists = [int (t) for t in dist_tokens.split()]
    return [Race(t, d) for t, d in zip(times, dists)]


def parse_input_b(lines):
    _, time_tokens = (t.strip() for t in lines[0].split(':'))
    time = int(''.join(t.strip() for t in time_tokens))
    _, dist_tokens = (t.strip() for t in lines[1].split(':'))
    dist = int(''.join(t.strip() for t in dist_tokens))
    return Race(time, dist)


def get_time_to_complete_race(time_to_hold, record_distance):
    time_to_cover_record_distance = record_distance / time_to_hold
    return time_to_hold + time_to_cover_record_distance


def compute_race_extrema(race):
    min_hold = race.time
    max_hold = 0
    for t in tqdm.trange(1, race.time):
        if t + (race.dist / t) < race.time:
            min_hold = min(min_hold, t)
            max_hold = max(max_hold, t)
    return min_hold,max_hold


def solve_a(races):
    result = []
    for race in races:
        min_hold, max_hold = compute_race_extrema(race)
        result.append((min_hold, max_hold))
    return functools.reduce(operator.mul, (y - x + 1 for x, y in result), 1)


def solve_b(race):
    min_hold, max_hold = compute_race_extrema(race)
    return max_hold - min_hold + 1


def main():
    "Main program."
    import sys
    import pyperclip
    lines = sys.stdin.readlines()
    races = parse_input_a(lines)
    soln_a = solve_a(races)
    assert soln_a == 625968
    print('The solution to the first part of day 6 is', soln_a)
    race = parse_input_b(lines)
    soln_b = solve_b(race)
    assert soln_b == 43663323
    print('The solution to the first part of day 6 is', soln_b)
    pyperclip.copy(str(soln_b))


if __name__ == '__main__':
    main()