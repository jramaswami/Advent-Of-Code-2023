"""
Advent of Code
Day 3
Gear Ratios
jramaswami
"""


import collections


OFFSETS = (
    (0, 1), (0, -1), (1, 0), (-1, 0),
    (1, 1), (-1, 1), (1, -1), (-1, -1)
)


def solve(grid):
    def inbounds(r, c):
        return r >= 0 and c >= 0 and r < len(grid) and c < len(grid[r])

    def neighbors(r, c):
        for dr, dc in OFFSETS:
            r0, c0 = r + dr, c + dc
            if inbounds(r0, c0):
                yield r0, c0

    visited = [[False for _ in row] for row in grid]

    queue = collections.deque()
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if grid[r][c] != '.' and not grid[r][c].isdigit():
                queue.append((r, c))

    while queue:
        r, c = queue.popleft()
        for r0, c0 in neighbors(r, c):
            if not visited[r0][c0] and grid[r0][c0].isdigit():
                queue.append((r0, c0))
                visited[r0][c0] = True

    numbers = []
    gears = collections.defaultdict(list)

    curr = 0
    is_gear = False
    gear_posn = None
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if visited[r][c]:
                curr *= 10
                curr += int(grid[r][c])
                for r0, c0 in neighbors(r, c):
                    if grid[r0][c0] == '*':
                        is_gear = True
                        gear_posn = (r0, c0)
            else:
                if curr > 0:
                    numbers.append(curr)
                    if is_gear:
                        gears[gear_posn].append(curr)
                curr = 0
                is_gear = False
                gear_posn = None
    soln_a = sum(numbers)
    soln_b = sum(t[0] * t[1] for t in gears.values() if len(t) > 1)
    return soln_a, soln_b


def test_solve():
    with open('../../data/03/test03a.txt', 'r') as infile:
        lines = infile.readlines()
    grid = [line.strip() for line in lines]
    expected_a, expected_b = 4361, 467835
    soln_a, soln_b = solve(grid)
    assert soln_a == expected_a
    assert soln_b == expected_b


def main():
    "Main program"
    import sys
    import pyperclip
    grid = [line.strip() for line in sys.stdin]
    soln_a, soln_b = solve(grid)
    print('The sum of the numbers adjacent to the symbols is', soln_a)
    assert soln_a == 531932
    print('The sum of the gear ratios is', soln_b)
    pyperclip.copy(str(soln_b))
    assert soln_b == 73646890


if __name__ == '__main__':
    main()