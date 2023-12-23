"""
Advent of Code
Day 23
A Long Walk
jramaswami
"""


import collections
import sys


sys.setrecursionlimit(pow(10,5))


Vector = collections.namedtuple('Vector', ['row', 'col'])
Vector.__add__ = lambda a, b: Vector(a.row + b.row, a.col + b.col)


OFFSETS = (Vector(1, 0), Vector(-1, 0), Vector(0, 1), Vector(0, -1))


def inbounds(p, grid):
    return (
        p.row >= 0 and p.col >= 0 and
        p.row < len(grid) and p.col < len(grid[p.row])
    )


def neighbors(p, grid):
    if grid[p.row][p.col] in 'v^><':
        q = p + OFFSETS['v^><'.index(grid[p.row][p.col])]
        if inbounds(q, grid) and grid[q.row][q.col] != '#':
            yield q
    else:
        for d in OFFSETS:
            q = p + d
            if inbounds(q, grid) and grid[q.row][q.col] != '#':
                yield q


def read_input(path):
    with open(path, 'r') as infile:
        grid = [line.strip() for line in infile]
    return grid


def solve_a(grid):
    start = Vector(0, grid[0].index('.'))
    finish = Vector(len(grid)-1, grid[-1].index('.'))
    visited = set()

    def dfs(p, d):
        visited.add(p)
        if p == finish:
            result = d
        else:
            result = 0
            for q in neighbors(p, grid):
                if q not in visited:
                    result = max(result, dfs(q, d+1))
        visited.remove(p)
        return result

    return dfs(start, 0)


def test_solve_a():
    grid = read_input('../../data/23/test23a.txt')
    assert solve_a(grid) == 94


def solve_b(grid):
    start = Vector(0, grid[0].index('.'))
    finish = Vector(len(grid)-1, grid[-1].index('.'))
    critical_points = [start, finish]

    # Find any points that branch and add them to critical points
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell != '#':
                ns = 0
                p = Vector(r, c)
                for d in OFFSETS:
                    q = p + d
                    if inbounds(q, grid) and grid[q.row][q.col] != '#':
                        ns += 1
                if ns > 2:
                    critical_points.append(p)

    # Graph critical points
    graph = collections.defaultdict(list)
    for cp in critical_points:
        queue = collections.deque()
        queue.append((cp, 0))
        visited = set()
        visited.add(cp)
        while queue:
            p, d = queue.popleft()
            if p != cp and p in critical_points:
                # Do not go through another critical point
                graph[cp].append((p, d))
            else:
                for o in OFFSETS:
                    q = p + o
                    if inbounds(q, grid) and grid[q.row][q.col] != '#' and q not in visited:
                        visited.add(q)
                        queue.append((q, d+1))

    # Make sure there are no duplicates in any critical point edges
    for cp in critical_points:
        vs = [t[0] for t in graph[cp]]
        assert len(vs) == len(set(vs))

    # Find longest path using critical points
    visited = set()
    def dfs(p, d):
        visited.add(p)
        if p == finish:
            result = d
        else:
            result = 0
            for q, d_ in graph[p]:
                if q not in visited:
                    result = max(result, dfs(q, d+d_))
        visited.remove(p)
        return result

    soln_b = dfs(start, 0)
    return soln_b


def test_solve_b():
    grid = read_input('../../data/23/test23a.txt')
    assert solve_b(grid) == 154


def main():
    "Main program"
    import pyperclip
    grid = read_input('../../data/23/input23.txt')
    soln_a = solve_a(grid)
    print('The longest hike with slippery slopes is', soln_a, 'steps')
    assert soln_a == 2074
    soln_b = solve_b(grid)
    print('The longest hike without slippery slopes is', soln_b, 'steps')
    pyperclip.copy(str(soln_b))
    assert soln_b == 6494


if __name__ == '__main__':
    main()