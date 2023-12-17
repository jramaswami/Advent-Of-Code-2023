"""
Advent of Code
Day 17
Clumsy Crucible
jramaswami
"""


import collections
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
    cache = collections.defaultdict(lambda: math.inf)
    init_crucible = Crucible(Vector(0, 0), None, 0)
    target_posn = Vector(len(grid)-1, len(grid[-1])-1)
    cache[init_crucible] = 0
    queue = collections.deque()
    queue.append(QItem(0, init_crucible))
    soln_a = math.inf
    while queue:
        item = queue.popleft()
        if cache[item.crucible] != item.heat_loss:
            continue
        if item.crucible.posn == target_posn:
            soln_a = min(soln_a, item.heat_loss)
        for crucible0 in neighbors(item.crucible, grid):
            heat_loss0 = item.heat_loss + grid[crucible0.posn.row][crucible0.posn.col]
            if heat_loss0 < cache[crucible0]:
                cache[crucible0] = heat_loss0
                queue.append(QItem(heat_loss0, crucible0))
    return soln_a


def test_solve_a():
    grid = read_input('../../data/17/test17a.txt')
    assert solve_a(grid) == 102


def main():
    "Main program"
    import pyperclip
    grid = read_input('../../data/17/input17.txt')
    soln_a = solve_a(grid)
    print('The minimum heatloss is', soln_a)
    assert soln_a == 963
    pyperclip.copy(str(soln_a))


if __name__ == '__main__':
    main()