"""
Advent of Code
Day 21
Step Counter
jramaswami
"""


import collections


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


def solve_b(grid, ticks):
    visited = dict()
    queue = collections.deque()
    start = find_start(grid)
    visited[start] = 0
    queue.append(start)
    min_row, max_row = -(7 * len(grid)), (7 * len(grid))
    min_col, max_col = - (7 * len(grid[0])), (7 * len(grid[0]))

    print(min_row, max_row)
    print(min_col, max_col)
    print(start)
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
    gog = []
    dog = []
    for r_ in range(-5, 5+1):
        curr_gog = []
        curr_dog = []
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
            # print(curr_grid)
            if curr_grid not in grids_seen:
                grids_seen[curr_grid] = len(grids_seen)
            curr_gog.append(grids_seen[curr_grid])
            curr_dog.append(visited[Vector(dr+start.row, dc+start.col)])
        gog.append(curr_gog)
        dog.append(curr_dog)

    for row in gog:
        print(row)

    for row in dog:
        print(row)

    # for r in range(min_row+start.row, max_row, len(grid)):
    #     for d in (0,):
    #         for c in range(min_col+start.col, max_col, len(grid[0])):

    #                 p = Vector(r+d,c)
    #                 if p in visited:
    #                     print(p, visited[p], end=', ')
    #                 else:
    #                     print(p, '#', end=', ')
    #         print()




def main():
    "Main program"
    import pyperclip
    grid = read_input('../../data/21/input21.txt')
    soln_a = solve_a(grid, 64)
    print('The elf can reach', soln_a, 'garden plots in 64 steps')
    assert soln_a == 3649
    pyperclip.copy(str(soln_a))

    grid = read_input('../../data/21/test21a.txt')
    soln_b = solve_b(grid, 10000)

if __name__ == '__main__':
    main()