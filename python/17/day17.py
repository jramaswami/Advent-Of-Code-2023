"""
Advent of Code
Day 17
Clumsy Crucible
jramaswami
"""


import collections
import heapq
import math


Vector = collections.namedtuple('Vector', ['row', 'col'])
Vector.__add__ = lambda a, b: Vector(a.row + b.row, a.col + b.col)
Vector.reverse = lambda a: Vector(a.row * -1, a.col * -1)


Crucible = collections.namedtuple('Crucible', ['posn', 'dirn', 'consecutive_blocks'])


QItem = collections.namedtuple('QItem', ['heat_loss', 'crucible'])


EAST, SOUTH, WEST, NORTH = (Vector(0, 1),  Vector(1, 0), Vector(0, -1), Vector(-1, 0))
DIRECTIONS   = (EAST, SOUTH, WEST, NORTH)


def read_input(path):
    with open(path, 'r') as infile:
        grid = [[int(t) for t in line.strip()] for line in infile]
    return grid


def inbounds(crucible, grid):
    return (
        crucible.posn.row >= 0 and
        crucible.posn.col >= 0 and
        crucible.posn.row < len(grid) and
        crucible.posn.col < len(grid[crucible.posn.row])
    )


def neighbors(crucible, grid):
    for dirn in DIRECTIONS:
        # Cannot go in reverse
        if crucible.dirn and dirn == crucible.dirn.reverse():
            continue
        # Consecutive blocks
        if dirn == crucible.dirn:
            crucible0 = Crucible(crucible.posn + dirn, dirn, crucible.consecutive_blocks+1)
        else:
            crucible0 = Crucible(crucible.posn + dirn, dirn, 1)
        if inbounds(crucible0, grid) and crucible0.consecutive_blocks <= 3:
            yield crucible0


def solve_a(grid):
    soln_a = math.inf
    heat_loss_to_reach = [[math.inf for _ in row] for row in grid]
    heat_loss_to_reach[0][0] = 0
    queue = collections.deque([QItem(0, Crucible(Vector(0,0), None, 0))])

    while queue:
        item = queue.popleft()
        if item.heat_loss > heat_loss_to_reach[item.crucible.posn.row][item.crucible.posn.col]:
            continue
        for neighbor in neighbors(item.crucible, grid):
            heat_loss0 = item.heat_loss + grid[neighbor.posn.row][neighbor.posn.col]
            if heat_loss0 < heat_loss_to_reach[neighbor.posn.row][neighbor.posn.col]:
                heat_loss_to_reach[neighbor.posn.row][neighbor.posn.col] = heat_loss0
                queue.append(QItem(heat_loss0, neighbor))


    with open('../../data/17/result17a.txt') as infile:
        T = [line.strip() for line in infile]

    for r, row in enumerate(heat_loss_to_reach):
        for c, x in enumerate(row):
            h = grid[r][c]
            t = '.' if T[r][c].isdigit() else T[r][c]
            print(f'{x:03}|{h}', end=' ')
        print()

    curr = Vector(0, 0)
    visited = set()
    visited.add(curr)
    hl = 0
    while curr != Vector(len(grid)-1, len(grid[-1])-1):
        for d in DIRECTIONS:
            x = curr + d
            if x in visited:
                continue
            if x.row >= 0 and x.col >= 0 and x.row < len(grid) and x.col < len(grid[0]):
                if not T[x.row][x.col].isdigit():
                    hl += grid[x.row][x.col]
                    curr = x
                    visited.add(curr)
                    print(x, hl, heat_loss_to_reach[x.row][x.col])
                    break
    print('ok')


def test_solve_a():
    grid = read_input('../../data/17/test17a.txt')
    assert solve_a(grid) == 102


def main():
    "Main program"
    import pyperclip
    grid = read_input('../../data/17/test17a.txt')
    soln_a = solve_a(grid)
    print('The minimum heatloss is', soln_a)


if __name__ == '__main__':
    main()