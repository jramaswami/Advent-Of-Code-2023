"""
Advent of Code
Day 21
Step Counter
jramaswami

For part b, inspection of puzzle input shows a repeating pattern of parity grids

[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

Where there are only two kinds of parity grids.

There is also a pattern in the distances to the center of the a grid section:

[1310, 1179, 1048, 917, 786, 655, 786, 917, 1048, 1179, 1310]
[1179, 1048, 917, 786, 655, 524, 655, 786, 917, 1048, 1179]
[1048, 917, 786, 655, 524, 393, 524, 655, 786, 917, 1048]
[917, 786, 655, 524, 393, 262, 393, 524, 655, 786, 917]
[786, 655, 524, 393, 262, 131, 262, 393, 524, 655, 786]
[655, 524, 393, 262, 131, 0, 131, 262, 393, 524, 655]
[786, 655, 524, 393, 262, 131, 262, 393, 524, 655, 786]
[917, 786, 655, 524, 393, 262, 393, 524, 655, 786, 917]
[1048, 917, 786, 655, 524, 393, 524, 655, 786, 917, 1048]
[1179, 1048, 917, 786, 655, 524, 655, 786, 917, 1048, 1179]
[1310, 1179, 1048, 917, 786, 655, 786, 917, 1048, 1179, 1310]

Note that delta is 131.  So the distance to the center of
subgrid[r][c] = delta * (|r| + |c|) and the type of grid
is gridtype[(|r|+|c|) % 2]

This does not work for the test input!


128506022 is too low
10518681788970528282 is too high
"""


import collections
import math


Vector = collections.namedtuple('Vector', ['row', 'col'])
Vector.__add__ = lambda a, b: Vector(a.row + b.row, a.col + b.col)


OFFSETS = (Vector(1,0), Vector(-1,0), Vector(0,1), Vector(0,-1))


def read_input(path):
    with open(path, 'r') as infile:
        grid = [line.strip() for line in infile]
    return grid


def inbounds(p, grid):
    return p.row >= 0 and p.col >=0 and p.row < len(grid) and p.col < len(grid[p.row])


def neighbors(p, grid):
    for off in OFFSETS:
        p0 = p + off
        if inbounds(p0, grid):
            yield p0


def find_start(grid):
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if grid[r][c] == 'S':
                return Vector(r, c)


def solve_a(grid, ticks):
    curr_queue = set()
    curr_queue.add(find_start(grid))
    next_queue = set()
    for _ in range(ticks):
        for p in curr_queue:
            for p0 in neighbors(p, grid):
                if grid[p0.row][p0.col] != '#':
                    next_queue.add(p0)
        curr_queue, next_queue = next_queue, set()
    return len(curr_queue)


def test_solve_a():
    grid = read_input('../../data/21/test21a.txt')
    assert solve_a(grid, 6) == 16


def manhattan_distance(p, q):
    return abs(p.row - q.row) + abs(p.col - q.col)


def solve_b(grid):
    ticks = 26501365

    # Collect grid types
    visited = dict()
    queue = collections.deque()
    start = find_start(grid)
    visited[start] = 0
    queue.append(start)
    min_row, max_row = -(7 * len(grid)), (7 * len(grid))
    min_col, max_col = - (7 * len(grid[0])), (7 * len(grid[0]))
    while queue:
        p = queue.popleft()
        for d in OFFSETS:
            q = p + d
            if q.row < min_row or q.row >= max_row:
                continue
            if q.col < min_col or q.col >= max_col:
                continue

            if q in visited:
                continue
            if grid[q.row % len(grid)][q.col % len(grid[0])] == '#':
                continue

            visited[q] = visited[p] + 1
            queue.append(q)

    grids_seen = dict()
    grid_id = dict()
    for r_ in range(-5, 5+1):
        for c_ in range(-5, 5+1):
            dr = len(grid) * r_
            dc = len(grid) * c_

            curr_grid = []
            for r in range(dr, dr+len(grid)):
                grid_row = []
                for c in range(dc, dc+len(grid[0])):
                    p = Vector(r, c)
                    if p in visited:
                        grid_row.append(str(visited[p] % 2))
                    else:
                        grid_row.append('#')
                curr_grid.append(''.join(grid_row))

            curr_grid = '\n'.join(row for row in curr_grid)
            if curr_grid not in grids_seen:
                grids_seen[curr_grid] = len(grids_seen)
            grid_id[Vector(r_, c_)] = grids_seen[curr_grid]

    assert len(grids_seen) == 2

    print('Distances to center of subgrid')
    for row_offset in range(-5, 6):
        r = start.row + (len(grid) * row_offset)
        for col_offset in range(-5, 6):
            c = start.col + (len(grid[0]) * col_offset)
            p = Vector(r,c)
            if p in visited:
                x = visited[p]
                print(f'{x:04}', end=' ')
            else:
                print('....', end=' ')
        print()

    print('Grid type of subgrid')
    for r in range(-5, 6):
        for c in range(-5, 6):
            p = Vector(r,c)
            print(grid_id[p], end=' ')
        print()

    # What grids can be reached?
    DELTA = 131

    # print(ticks / 131)
    # # How many grids can be reached
    # grid_reachables = [g.count('1') for g in grids_seen]
    # reachable_grids = int(math.ceil(2 * ticks / 131))
    # print('reachable grids', reachable_grids)
    # ones_zeros_row = [1 + ((reachable_grids-1) // 2), ((reachable_grids-1) // 2)]
    # ones_zeros_total = [131 * x for x in ones_zeros_row]
    # print('gr', grid_reachables)
    # print('10r', ones_zeros_row)
    # print('10t', ones_zeros_total)
    # ones_zeros_reachable = [x * y for x, y in zip(ones_zeros_total, grid_reachables)]
    # print(ones_zeros_reachable)
    # return sum(ones_zeros_reachable)

    XS = [g.count('1') for g in grids_seen]
    soln_b = XS[0]
    m = 4
    for t in range(1, ticks):
        soln_b += (m * XS[t%2])
        m += 4
    soln_b += (m * XS[ticks%2] // 2)
    return soln_b



# def test_soln_b():
#     grid = read_input('../../data/21/test21a.txt')
#     assert solve_b(grid, 6) == 16
#     assert solve_b(grid, 10) == 50
#     assert solve_b(grid, 5000) == 16733044


def main():
    "Main program"
    import pyperclip
    grid = read_input('../../data/21/input21.txt')
    # soln_a = solve_a(grid, 64)
    # print('The elf can reach', soln_a, 'garden plots in 64 steps')
    # assert soln_a == 3649
    # pyperclip.copy(str(soln_a))

    # grid = read_input('../../data/21/test21a.txt')
    soln_b = solve_b(grid)
    print('Solution b', soln_b)
    pyperclip.copy(str(soln_b))


if __name__ == '__main__':
    main()