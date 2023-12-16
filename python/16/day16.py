"""
Advent of Code
Day 16
The Floor Will Be Lava
jramaswami
"""


import collections


Vector = collections.namedtuple('Vector', ['row', 'col'])
Vector.__add__ = lambda a, b: Vector(a.row + b.row, a.col + b.col)


Beam = collections.namedtuple('Beam', ['posn', 'dirn'])


EAST, SOUTH, WEST, NORTH = (Vector(0, 1),  Vector(1, 0), Vector(0, -1), Vector(-1, 0))


def read_input(path):
    with open(path, 'r') as infile:
        grid = [line.strip() for line in infile]
    return grid


def next_positions(beam, grid):
    cell = grid[beam.posn.row][beam.posn.col]
    if cell == '.':
        # Beam on '.' continues the same.
        return [Beam(beam.posn + beam.dirn, beam.dirn)]
    if cell == '/':
        # Beam on / turns 90deg
        if beam.dirn == EAST:
            # EAST -> NORTH
            new_dirn = NORTH
        elif beam.dirn == SOUTH:
            # SOUTH -> WEST
            new_dirn = WEST
        elif beam.dirn == NORTH:
            # NORTH -> EAST
            new_dirn = EAST
        elif beam.dirn == WEST:
            # WEST -> SOUTH
            new_dirn = SOUTH
        else:
            raise ValueError('Unable to match direction for cell "/"')
        return [Beam(beam.posn + new_dirn, new_dirn)]
    elif cell == '\\':
        # Beam on \ turns 90deg
        if beam.dirn == EAST:
            # EAST -> SOUTH
            new_dirn = SOUTH
        elif beam.dirn == SOUTH:
            # SOUTH -> EAST
            new_dirn = EAST
        elif beam.dirn == NORTH:
            # NORTH -> WEST
            new_dirn = WEST
        elif beam.dirn == WEST:
            # WEST -> NORTH
            new_dirn = NORTH
        else:
            raise ValueError('Unable to match direction for cell "\\"')
        return [Beam(beam.posn + new_dirn, new_dirn)]
    elif cell == '|':
        if beam.dirn == SOUTH or beam.dirn == NORTH:
            # Beam goes through splitter when striking parallel
            result = [Beam(beam.posn + beam.dirn, beam.dirn)]
        else:
            # Beam splits when striking splitter perpendicular
            result = [Beam(beam.posn + NORTH, NORTH), Beam(beam.posn + SOUTH, SOUTH)]
        return result
    elif cell == '-':
        if beam.dirn == EAST or beam.dirn == WEST:
            # Beam goes through splitter when striking parallel
            return [Beam(beam.posn + beam.dirn, beam.dirn)]
        else:
            # Beam splits when striking splitter perpendicular
            return [Beam(beam.posn + EAST, EAST), Beam(beam.posn + WEST, WEST)]


def inbounds(beam, grid):
    return (
        beam.posn.row >= 0 and
        beam.posn.col >= 0 and
        beam.posn.row < len(grid) and
        beam.posn.col < len(grid[beam.posn.row])
    )


def get_energized(grid, init_beam):
    energized = [[False for _ in row] for row in grid]
    queue = collections.deque()
    energized[init_beam.posn.row][init_beam.posn.col] = True
    visited = set()
    visited.add(init_beam)
    queue.append(init_beam)

    while queue:
        beam = queue.popleft()
        energized[beam.posn.row][beam.posn.col] = True
        for beam0 in next_positions(beam, grid):
            if inbounds(beam0, grid) and beam0 not in visited:
                visited.add(beam0)
                queue.append(beam0)
    return energized


def test_get_energized():
    grid = read_input('../../data/16/test16a.txt')
    result = get_energized(grid, Beam(Vector(0,0), EAST))
    sample = read_input('../../data/16/result16a.txt')
    expected = [[True if t == '#' else False for t in row] for row in sample]
    assert result == expected


def solve_a(grid, init_beam=Beam(Vector(0,0), EAST)):
    energized = get_energized(grid, init_beam)
    result = sum(sum(row) for row in energized)
    return result


def test_solve_a():
    grid = read_input('../../data/16/test16a.txt')
    result = solve_a(grid)
    assert result == 46


def solve_b(grid):
    soln_b = 0
    for c, _ in enumerate(grid[0]):
        # Top row heads south
        soln_b = max(soln_b, solve_a(grid, Beam(Vector(0, c), SOUTH)))
        # Bottom row heads north
        soln_b = max(soln_b, solve_a(grid, Beam(Vector(len(grid)-1, c), NORTH)))
    for r, _ in enumerate(grid):
        # Left col heads east
        soln_b = max(soln_b, solve_a(grid, Beam(Vector(r, 0), EAST)))
        # Right col head west
        soln_b = max(soln_b, solve_a(grid, Beam(Vector(r, len(grid[0])-1), WEST)))
    return soln_b


def test_solve_b():
    grid = read_input('../../data/16/test16a.txt')
    result = solve_b(grid)
    assert result == 51


def main():
    "Main program"
    import pyperclip
    grid = read_input('../../data/16/input16.txt')
    soln_a = solve_a(grid)
    print(soln_a, 'tiles end up begin energized')
    assert soln_a == 8539
    soln_b = solve_b(grid)
    print('The maximum possible number of energized tiles is', soln_b)
    pyperclip.copy(str(soln_b))


if __name__ == '__main__':
    main()