"""
Advent of Code
Day 14
Parabolic Reflector Dish
jramaswami
"""


def read_input(path):
    with open(path, 'r') as infile:
        grid = [line.strip() for line in infile]
    return grid


def S(n):
    if n < 0:
        return 0
    return (n * (n + 1)) // 2


def compute_load(rocks, row):
    return (row * rocks) - S(rocks-1)


def solve_a(grid):
    # Compute number of rocks that roll to the north.
    soln = 0
    curr_rocks = [0 for _ in grid[0]]
    N = len(grid)
    for r, row in enumerate(reversed(grid)):
        for c, cell in enumerate(row):
            if cell == '#':
                # Add the load of these rocks to solution
                soln += compute_load(curr_rocks[c], r)
                curr_rocks[c] = 0
            elif cell == 'O':
                curr_rocks[c] += 1
    # Add the load for all the rocks that stopped at the top of the grid
    soln += sum(compute_load(cr, N) for cr in curr_rocks)
    return soln


def test_soln_a():
    grid = read_input('../../data/14/test14a.txt')
    assert solve_a(grid) == 136


def main():
    "Main program"
    import pyperclip
    grid = read_input('../../data/14/input14.txt')
    soln_a = solve_a(grid)
    print('The total load is', soln_a)
    assert soln_a == 111979
    pyperclip.copy(str(soln_a))



if __name__ == '__main__':
    main()