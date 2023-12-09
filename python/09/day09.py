"""
Advent of Code
Day 9
Mirage Maintenance
jramaswami

2040549387 is too high
"""


def extrapolate_value(sequence):
    rows = [[]]
    for i, _ in enumerate(sequence[:-1]):
        d = sequence[i+1] - sequence[i]
        rows[0].append(d)
        for r, row in enumerate(rows):
            if len(row) >= 2:
                d = row[-1] - row[-2]
                if d > 0:
                    if r + 1 >= len(rows):
                        rows.append([])
                    rows[r+1].append(d)
    rows.append([0 for _ in rows[-1]])

    for r in range(len(rows)-1, 0, -1):
        rows[r-1].append(rows[r-1][-1] + rows[r][-1])

    return sequence[-1] + rows[0][-1]


def test_extrapolate():
    inputs = ['0 3 6 9 12 15', '1 3 6 10 15 21', '10 13 16 21 30 45']
    sequences = [[int(n) for n in inp.split()] for inp in inputs]
    expected = [18, 28, 68]
    assert [extrapolate_value(seq) for seq in sequences] == expected


def solve_a(sequences):
    return sum(extrapolate_value(seq) for seq in sequences)


def test_solve_a():
    inputs = ['0 3 6 9 12 15', '1 3 6 10 15 21', '10 13 16 21 30 45']
    sequences = [[int(n) for n in inp.split()] for inp in inputs]
    assert solve_a(sequences) == 114


def main():
    "Main program"
    import pyperclip
    with open('../../data/09/input09.txt', 'r') as infile:
        sequences = [[int(n) for n in t.strip().split()] for t in infile.readlines()]
    soln_a = solve_a(sequences)
    print('The sum of the extrapolated values is', soln_a)
    pyperclip.copy(str(soln_a))




if __name__ == '__main__':
    main()