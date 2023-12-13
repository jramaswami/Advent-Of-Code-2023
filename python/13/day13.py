"""
Advent of Code
Day 13
Point of Incidence
jramaswami

22255 is too low
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


def fix_smudge(grid):
    # Fix smudge
    grid = [[c for c in row] for row in grid]

    # Find original row/col
    result = []
    result.append((find_mirror(grid), find_mirror(rotate_grid(grid))))
    # Find all smudge fixes
    for r, row in enumerate(grid):
        for c, _ in enumerate(row):
            rs, cs = 0, 0
            # Swap the character here
            if grid[r][c] == '.':
                grid[r][c] = '#'
            else:
                grid[r][c] = '.'
            result.append((find_mirror(grid), find_mirror(rotate_grid(grid))))
            # Swap the character back
            if grid[r][c] == '.':
                grid[r][c] = '#'
            else:
                grid[r][c] = '.'
    return result


def solve_b(grids):
    rs, cs = 0, 0
    for grid in grids:
        result = fix_smudge(grid)
        # Original result is first item
        cs0, rs0 = result[0]
        for cs_, rs_ in result[1:]:
            if rs_ > 0 or cs_ > 0:
                if rs_ > 0 and rs_ != rs0:
                    rs += rs_
                    break
                if cs_ > 0 and cs_ != cs0:
                    cs += cs_
                    break
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
    pyperclip.copy(str(soln_b))


if __name__ == '__main__':
    main()