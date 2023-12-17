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


def ultimate_neighbors(crucible, grid):
    if crucible.dirn and crucible.consecutive_blocks < 4:
        # Once an ultra crucible starts moving in a direction, it needs
        # to move a minimum of four blocks
        crucible0 = Crucible(crucible.posn + crucible.dirn, crucible.dirn, crucible.consecutive_blocks+1)
        if inbounds(crucible0, grid):
            yield crucible0
    else:
        for dirn in DIRECTIONS:
            # Cannot go in reverse
            if crucible.dirn and dirn == crucible.dirn.reverse():
                continue
            if dirn == crucible.dirn:
                crucible0 = Crucible(crucible.posn + dirn, dirn, crucible.consecutive_blocks+1)
            else:
                crucible0 = Crucible(crucible.posn + dirn, dirn, 1)
            if inbounds(crucible0, grid) and crucible0.consecutive_blocks <= 10:
                # An ultra crucible can move a maximum of ten consecutive
                # blocks without turning
                yield crucible0


def solve(grid, neighborsfn=neighbors):
    cache = collections.defaultdict(lambda: math.inf)
    init_crucible = Crucible(Vector(0, 0), None, 0)
    target_posn = Vector(len(grid)-1, len(grid[-1])-1)
    cache[init_crucible] = 0
    queue = collections.deque()
    queue.append(QItem(0, init_crucible))
    soln = math.inf
    while queue:
        item = queue.popleft()
        if cache[item.crucible] != item.heat_loss:
            continue
        if item.crucible.posn == target_posn:
            if neighborsfn == ultimate_neighbors:
                if item.crucible.consecutive_blocks >= 4:
                    # An ultimate crucible cannot stop on the last block
                    # until it has gone at least 4 consecutive blocks
                    soln = min(soln, item.heat_loss)
            else:
                soln = min(soln, item.heat_loss)
        for crucible0 in neighborsfn(item.crucible, grid):
            heat_loss0 = item.heat_loss + grid[crucible0.posn.row][crucible0.posn.col]
            if heat_loss0 < cache[crucible0]:
                cache[crucible0] = heat_loss0
                queue.append(QItem(heat_loss0, crucible0))
    return soln


def test_solve_a():
    grid = read_input('../../data/17/test17a.txt')
    assert solve(grid) == 102


def test_solve_b():
    grid = read_input('../../data/17/test17a.txt')
    assert solve(grid, ultimate_neighbors) == 94

    grid = read_input('../../data/17/test17b.txt')
    assert solve(grid, ultimate_neighbors) == 71

def main():
    "Main program"
    import pyperclip
    grid = read_input('../../data/17/input17.txt')
    soln_a = solve(grid)
    print('The minimum heatloss is', soln_a)
    assert soln_a == 963
    soln_b = solve(grid, ultimate_neighbors)
    print('The minimum heatloss of an ultimate crucible is', soln_b)
    pyperclip.copy(str(soln_b))


if __name__ == '__main__':
    main()