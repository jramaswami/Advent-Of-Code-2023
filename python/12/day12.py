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