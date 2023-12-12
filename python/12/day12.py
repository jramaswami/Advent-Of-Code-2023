"""
Advent of Code
Day 12
Hot Springs
jramaswami
"""


import functools


def read_input(path):
    records = []
    with open(path, 'r') as infile:
        for line in infile:
            line = line.strip()
            grid, rle = (t.strip() for t in line.split())
            rle = tuple(int(t) for t in rle.split(','))
            records.append((grid, rle))
    return records


def count_arrangements_rec(grid, rle):

    @functools.cache
    def can_start_run(g, r):
        # There must be some rle's left
        if r >= len(rle):
            return False
        rl = rle[r]
        # The run must fit inside the grid
        if g+rl > len(grid):
            return False
        # All the chars in the grid must be # or ?
        if any(c == '.' for c in grid[g:g+rl]):
            return False
        return True

    @functools.cache
    def starting(g, r):
        # Base case: done with grid.
        if g >= len(grid):
            # If done with rle too, then we have found an arrangement.
            if r >= len(rle):
                return 1
            return 0

        # Recur.
        if grid[g] == '.':
            # I must move forward.
            return starting(g+1, r)
        elif grid[g] == '?':
            result = 0
            # I can start an rle here
            if can_start_run(g, r):
                result += finishing(g+rle[r], r+1)
            # I can just move forward
            result += starting(g+1, r)
            return result
        elif grid[g] == '#':
            # I must start an rle here
            if can_start_run(g, r):
                return finishing(g+rle[r], r+1)
            return 0

    @functools.cache
    def finishing(g, r):
        # Base case: done with grid.
        if g >= len(grid):
            # If done with rle too, then we have found an arrangement.
            if r >= len(rle):
                return 1
            return 0

        # The next cell cannot be a #
        if grid[g] == '#':
            return 0
        return starting(g+1, r)

    return starting(0, 0)


def test_count_arrangments_rec():
    records = read_input('../../data/12/test12a.txt')
    expected = [1,4,1,1,4,10]
    result = [count_arrangements_rec(*r) for r in records]
    assert result == expected

    records0 = []
    for grid, rle in records:
        grid0 = '?'.join(grid for _ in range(5))
        records0.append((grid0, rle*5))
    expected = [1,16384,1,16,2500,506250]
    result = [count_arrangements_rec(*r) for r in records0]
    assert result == expected


def solve_a(records):
    return sum(count_arrangements_rec(*r) for r in records)


def test_solve_a():
    records = read_input('../../data/12/test12a.txt')
    expected = 21
    result = solve_a(records)
    assert result == expected


def solve_b(records):
    records0 = []
    for grid, rle in records:
        grid0 = '?'.join(grid for _ in range(5))
        records0.append((grid0, rle*5))
    return solve_a(records0)


def test_solve_b():
    records = read_input('../../data/12/test12a.txt')
    expected = 525152
    result = solve_b(records)
    assert result == expected


def main():
    "Main program"
    import pyperclip
    records = read_input('../../data/12/input12.txt')
    soln_a = solve_a(records)
    print('The sum of the counts is', soln_a)
    assert soln_a == 6488
    soln_b = solve_b(records)
    print('The new sum of possible arrangement counts is', soln_b)
    assert soln_b == 815364548481
    pyperclip.copy(soln_b)


if __name__ == '__main__':
    main()