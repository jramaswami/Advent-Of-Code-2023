"""
Advent of Code
Day 11
Cosmic Expansion
jramaswami
"""


def read_input(path):
    with open(path,'r') as infile:
        grid = [line.strip() for line in infile.readlines()]
    return grid


def solve_a(grid):
    soln_a = 0

    # Find location of all galaxies
    galaxies = []
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == '#':
                galaxies.append((r, c))

    # Find empty rows/cols
    empty_rows = []
    for r, row in enumerate(grid):
        if all(t == '.' for t in row):
            empty_rows.append(r)

    empty_cols = []
    for c, _ in enumerate(grid[0]):
        if all(row[c] == '.' for row in grid):
            empty_cols.append(c)

    # For each pair of galaxies
    pairs = 0
    for i, g1 in enumerate(galaxies):
        for j, g2 in enumerate(galaxies[i+1:], start=i+1):
            pairs += 1
            dist = 0
            r1, r2 = min(g1[0], g2[0]), max(g1[0], g2[0])
            dist += r2 - r1
            ers = sum(1 for er in empty_rows if r1 <= er <= r2)
            dist += ers
            # Compute how many empty cols are crossed and add them distance.
            c1, c2 = min(g1[1], g2[1]), max(g1[1], g2[1])
            dist += c2 - c1
            ecs = sum(1 for ec in empty_cols if c1 <= ec <= c2)
            dist += ecs
            soln_a += dist
    return soln_a


def test_solve_a():
    grid = read_input('../../data/11/test11a.txt')
    soln_a = solve_a(grid)
    assert soln_a == 374


def main():
    "Main program"
    import pyperclip
    grid = read_input('../../data/11/input11.txt')
    soln_a = solve_a(grid)
    print('The sum of the lengths is', soln_a)
    assert soln_a == 9648398
    pyperclip.copy(str(soln_a))


if __name__ == '__main__':
    main()