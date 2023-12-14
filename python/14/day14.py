"""
Advent of Code
Day 14
Parabolic Reflector Dish
jramaswami
"""


def read_input(path):
    with open(path, 'r') as infile:
        grid = [[c for c in line.strip()] for line in infile]
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


def print_grid(grid):
    for row in grid:
        print(''.join(row))
    print()


def count_items(grid):
    hs, os = 0, 0
    for row in grid:
        for cell in row:
            if cell == '#':
                hs += 1
            if cell == 'O':
                os += 1
    return hs, os


def tilt_north(grid):
    ck = count_items(grid)
    limits = [-1 for _ in grid[0]]
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == '#':
                limits[c] = r
            elif cell == 'O':
                # Roll rock to just under the current limit
                r0 = limits[c]
                if r != r0:
                    grid[r][c] = '.'
                    grid[r0+1][c] = 'O'
                # Move limit down
                limits[c] += 1
    assert count_items(grid) == ck


def tilt_west(grid):
    ck = count_items(grid)
    N, M = len(grid), len(grid[0])
    limits = [-1 for _ in range(N)]
    for c in range(M):
        for r in range(N):
            if grid[r][c] == '#':
                limits[r] = c
            elif grid[r][c] == 'O':
                # Roll rock just to the right of the current limit
                c0 = limits[r] + 1
                if c0 != c:
                    grid[r][c0] = 'O'
                    grid[r][c] = '.'
                limits[r] = c0
    assert count_items(grid) == ck


def tilt_south(grid):
    ck = count_items(grid)
    N, M = len(grid), len(grid[0])
    limits = [N for _ in grid[0]]
    for r in range(N-1, -1, -1):
        for c in range(M):
            cell = grid[r][c]
            if cell == '#':
                limits[c] = r
            elif cell == 'O':
                # Roll rock to just above the current limit
                r0 = limits[c]
                if r != r0:
                    grid[r][c] = '.'
                    grid[r0-1][c] = 'O'
                # Move limit down
                limits[c] -= 1
    assert count_items(grid) == ck


def tilt_east(grid):
    ck = count_items(grid)
    N, M = len(grid), len(grid[0])
    limits = [M for _ in range(N)]
    for c in range(M-1, -1, -1):
        for r in range(N):
            if grid[r][c] == '#':
                limits[r] = c
            elif grid[r][c] == 'O':
                # Roll rock just to the left of the current limit
                c0 = limits[r] - 1
                if c0 != c:
                    grid[r][c0] = 'O'
                    grid[r][c] = '.'
                limits[r] = c0
    assert count_items(grid) == ck


def spin(grid):
    tilt_north(grid)
    tilt_west(grid)
    tilt_south(grid)
    tilt_east(grid)


def test_spin():
    grid = read_input('../../data/14/test14a.txt')
    spin(grid)
    expected = read_input('../../data/14/cycle1.txt')
    assert grid == expected
    spin(grid)
    expected = read_input('../../data/14/cycle2.txt')
    assert grid == expected
    spin(grid)
    expected = read_input('../../data/14/cycle3.txt')
    assert grid == expected


def compute_grid_load(grid):
    load = 0
    N = len(grid)
    for r, row in enumerate(grid):
        for _, cell in enumerate(row):
            if cell == 'O':
                load += N - r
    return load


def test_compute_grid_load():
    grid = read_input('../../data/14/test14a.txt')
    tilt_north(grid)
    assert compute_grid_load(grid) == 136


def solve_b(grid):
    loads = []
    for tick in range(1000):
        spin(grid)
        gl = compute_grid_load(grid)
        loads.append(gl)

    # Floyd's cycle detection, use subarray to avoid the singles that are
    # repeated, like 69 in the sample data
    k = 7
    slow = fast = 0
    cycle_detected = False
    while fast < len(loads):
        slow += 1
        fast += 2
        if loads[slow:slow+k] == loads[fast:fast+k]:
            print('cycle detected')
            cycle_detected = True
            break

    if cycle_detected:
        mu = 0
        while loads[mu:mu+k] != loads[slow:slow+k]:
            slow += 1
            mu += 1

    cycle = loads[mu:slow]
    target = 1000000000 - 1 # Subtract one to make zero based
    target -= mu
    target %= len(cycle)
    return cycle[target]


def test_solve_b():
    grid = read_input('../../data/14/test14a.txt')
    assert solve_b(grid) == 64


def main():
    "Main program"
    import pyperclip
    grid = read_input('../../data/14/input14.txt')
    soln_a = solve_a(grid)
    print('The total load is', soln_a)
    assert soln_a == 111979
    soln_b = solve_b(grid)
    print('After 1000000000 cycles, the total load is', soln_b)
    pyperclip.copy(str(soln_b))


if __name__ == '__main__':
    main()