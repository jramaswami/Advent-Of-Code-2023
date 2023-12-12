"""
Advent of Code
Day 12
Hot Springs
jramaswami
"""


def read_input(path):
    records = []
    with open(path, 'r') as infile:
        for line in infile:
            line = line.strip()
            grid, rle = (t.strip() for t in line.split())
            rle = tuple(int(t) for t in rle.split(','))
            records.append((grid, rle))
    return records


def compute_rle(grid):
    rle = []
    curr_ch = '.'
    curr_len = 0
    for ch in grid:
        if ch == '#':
            if curr_ch == ch:
                curr_len += 1
            else:
                curr_len = 1
        elif ch == '.':
            if curr_ch == '#':
                rle.append(curr_len)
                curr_len = 0
        else:
            ValueError("Found a character that isn't # or l.")
        curr_ch = ch
    if curr_len:
        rle.append(curr_len)
    return tuple(rle)


def test_compute_rle():
    assert compute_rle('#.#.###') == (1,1,3)
    assert compute_rle('.#...#....###.') == (1,1,3)
    assert compute_rle('.#.###.#.######') == (1,3,1,6)
    assert compute_rle('####.#...#...') == (4,1,1)
    assert compute_rle('#....######..#####.') == (1,6,5)
    assert compute_rle('.###.##....#') == (3,2,1)


def compute_arrangements(grid):
    arrangements = []

    def rec(i, acc):
        if i >= len(grid):
            arrangements.append(''.join(acc))
        elif grid[i] == '#':
            acc.append('#')
            rec(i+1, acc)
            acc.pop()
        elif grid[i] == '.':
            acc.append('.')
            rec(i+1, acc)
            acc.pop()
        elif grid[i] == '?':
            acc.append('#')
            rec(i+1, acc)
            acc.pop()
            acc.append('.')
            rec(i+1, acc)
            acc.pop()

    rec(0, [])
    return arrangements


def count_arrangements(record):
    arrangements = compute_arrangements(record[0])
    rles = [compute_rle(a) for a in arrangements]
    return sum(r == record[1] for r in rles)


def test_count_arrangements():
    records = read_input('../../data/12/test12a.txt')
    expected = [1, 4, 1, 1, 4, 10]
    result = [count_arrangements(r) for r in records]
    assert result == expected


def solve_a(records):
    return sum(count_arrangements(r) for r in records)


def test_solve_a():
    records = read_input('../../data/12/test12a.txt')
    expected = 21
    result = solve_a(records)
    assert result == expected


def count_arrangements_rec(record):
    grid, rle = record


    def rec(g, r):
        # print('rec', g, r)
        if g >= len(grid) and r >= len(rle):
            print(g, r, 'xxx')
            return 1

        if g >= len(grid) or r >= len(rle):
            print('yyy')
            return 0

        s = rec(g+1, r)
        t = 0
        if can_start_run(g, r):
            # print('g', g, 'r', r, 'can start moving to', g+rle[r]+1)
            t = rec(g+rle[r]+1, r+1)
        print('->', g, r, s, t, s+t)
        return s + t

    return rec(0, 0)


def can_start_run(g, r, grid, rle):
    "Return true if run r and start at grid[g]"
    # print('can_start_run', g, r)
    # Current cell has to be a ? or a #
    if grid[g] == '.':
        # print('w')
        return False
    # Previous cell has to have no spring on it.
    if g >= 0 and grid[g] == '#':
        # print('x')
        return False
    # All the cells of the run have to be a ? or a #
    if any(x == '.' for x in grid[g:g+rle[r]]):
        # print('y')
        return False
    # Cell after run has to be a . or a ?
    if g+rle[r] < len(grid) and grid[g+rle[r]] == '#':
        # print('z')
        return False
    # This must fit inside the grid
    if g+rle[r] > len(grid):
        return False
    return True


def count_arrangements_dp(record):
    grid, rle = record

    # dp[g][r]
    dp = [[0 for _ in range(len(rle)+1)] for _ in range(len(grid)+1)]
    dp[0][0] = 1
    for g, _ in enumerate(grid):
        for r, _ in enumerate(rle):
            # If cell is ?, you may start run
            if grid[r] == '?':
                dp[g+1][r] += dp[g][r]
                if can_start_run(g, r, grid, rle):
                    dp[g+rle[r]][r+1] += dp[g][r]
            # If cell is #, you must start run
            elif grid[r] == '#':
                if can_start_run(g, r, grid, rle):
                    dp[g+rle[r]][r+1] += dp[g][r]
            # If cell is ., you must move to next cell
            else:
                dp[g+1][r] += dp[g][r]
        # If there are no runs left, we can advance if the cell is not a #
        if grid[g] != '#':
            dp[g+1][-1] += dp[g][-1]


    for row in dp:
        print(row)
    return dp[-1][-1]


def test_count_arrangements_dp():
    records = read_input('../../data/12/test12a.txt')
    # expected = [1, 4, 1, 1, 4, 10]
    # result = [count_arrangements_dp(r) for r in records]
    # assert result == expected
    # assert count_arrangements_dp(('?', (1,))) == 1
    # assert count_arrangements_dp(('?.?', (1,))) == 2
    assert count_arrangements_dp(records[0]) == 1


def main():
    "Main program"
    import pyperclip
    records = read_input('../../data/12/input12.txt')
    soln_a = solve_a(records)
    print('The sum of the counts is', soln_a)
    assert soln_a == 6488
    pyperclip.copy(soln_a)


if __name__ == '__main__':
    main()