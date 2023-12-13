"""
Advent of Code
Day 13
Point of Incidence
jramaswami
"""


def read_input(path):
    grids = []
    with open(path, 'r') as infile:
        curr_grid = []
        for line in infile:
            line = line.strip()
            if line:
                curr_grid.append(line)
            else:
                grids.append(curr_grid)
                curr_grid = []
        grids.append(curr_grid)
    return grids


def test_read_input():
    grids = read_input('../../data/13/test13a.txt')
    assert len(grids) == 2


def has_mirror_at(c, row):
    """
    Return True if row has mirror in position p where p is the
    first postion of the reflection.
    """
    image = row[:c]
    reflection = row[c:]
    return all(a == b for a, b in zip(reflection, reversed(image)))


def test_has_mirror_at():
    row = '#.##..##.'
    assert has_mirror_at(5, row)
    assert not has_mirror_at(4, row)
    col = '##.##.#'
    assert has_mirror_at(4, col)
    assert not has_mirror_at(5, col)


def rotate_grid(grid):
    grid_t = []
    for c, _ in enumerate(grid[0]):
        row_t = []
        for r, _ in enumerate(grid):
            row_t.append(grid[r][c])
        grid_t.append(''.join(row_t))
    return grid_t


def test_rotate_grid():
    grid = ['#.', '#.']
    expected = ['##', '..']
    grid_t = rotate_grid(grid)
    assert grid_t == expected


def find_mirror(grid):
    for c, _ in enumerate(grid[0][1:], start=1):
        if all(has_mirror_at(c, row) for row in grid):
            return c
    return -1


def test_find_mirror():
    grid1, grid2 = read_input('../../data/13/test13a.txt')
    assert find_mirror(grid1) == 5
    grid2_t = rotate_grid(grid2)
    assert find_mirror(grid2_t) == 4

    grid1 = read_input('../../data/13/test13b.txt')[0]
    grid1_t = rotate_grid(grid1)
    assert find_mirror(rotate_grid(grid1)) == 1


def solve_a(grids):
    rs, cs = 0, 0
    for grid in grids:
        p = find_mirror(grid)
        cs += max(0, p)
        if p == -1:
            grid_t = rotate_grid(grid)
            p = find_mirror(grid_t)
            rs += max(0, p)
        assert p != -1
    return (100 * rs) + cs


def test_solve_a():
    grids = read_input('../../data/13/test13a.txt')
    expected = 405
    assert solve_a(grids) == expected


def find_mirror_b(grid):
    "Return list of all possible reflection points in grid"
    result = []
    for c, _ in enumerate(grid[0][1:], start=1):
        if all(has_mirror_at(c, row) for row in grid):
            result.append(c)
    return result


def fix_smudge(grid):
    # Find original row/col
    rs0, cs0 = find_mirror(rotate_grid(grid)), find_mirror(grid)

    # Transform into list of list of chars to make it mutable
    grid = [[c for c in row] for row in grid]

    # For every possible smudge find any reflection points that are different
    # than the original reflection point
    rs1, cs1 = -1, -1
    for r, row in enumerate(grid):
        for c, _ in enumerate(row):

            # Swap the character here
            if grid[r][c] == '.':
                grid[r][c] = '#'
            else:
                grid[r][c] = '.'

            grid_t = rotate_grid(grid)
            for rs_ in find_mirror_b(grid_t):
                if rs_ > 0 and rs_ != rs0:
                    rs1 = rs_
            if rs1 == -1:
                for cs_ in find_mirror_b(grid):
                    if cs_ > 0 and cs_ != cs0:
                        cs1 = cs_

            # Swap the character back
            if grid[r][c] == '.':
                grid[r][c] = '#'
            else:
                grid[r][c] = '.'

            if rs1 > 0 or cs1 > 0:
                break

    return rs1, cs1


def solve_b(grids):
    rs, cs = 0, 0
    for g, grid in enumerate(grids):
        result = fix_smudge(grid)
        # Original result is first item
        rs1, cs1 = fix_smudge(grid)
        if rs1 == -1 and cs1 == -1:
            print('NOT OK')
        rs += max(0, rs1)
        cs += max(0, cs1)
    return (100 * rs) + cs


def test_solve_b():
    grids = read_input('../../data/13/test13a.txt')
    expected = 400
    assert solve_b(grids) == expected


def main():
    "Main program"
    import pyperclip
    grids = read_input('../../data/13/input13.txt')
    soln_a = solve_a(grids)
    print('The summary number is', soln_a)
    assert soln_a == 37113
    soln_b = solve_b(grids)
    print('The summary number with new reflection lines is', soln_b)
    assert soln_b == 30449
    pyperclip.copy(str(soln_b))


if __name__ == '__main__':
    main()