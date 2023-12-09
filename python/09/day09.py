"""
Advent of Code
Day 9
Mirage Maintenance
jramaswami
"""


def extrapolate_value(sequence):
    rows = [[]]
    for i, _ in enumerate(sequence[:-1]):
        d = sequence[i+1] - sequence[i]
        rows[0].append(d)
        for r, row in enumerate(rows):
            if len(row) >= 2:
                d = row[-1] - row[-2]
                if r + 1 >= len(rows):
                    rows.append([])
                rows[r+1].append(d)
    rows.append([0 for _ in rows[-1]])

    for r in range(len(rows)-1, 0, -1):
        rows[r-1].append(rows[r-1][-1] + rows[r][-1])
    soln_a = sequence[-1] + rows[0][-1]

    # sequence0 = list(sequence)
    # sequence0.append(sequence[-1] + rows[0][-1])
    # print('*' * 60)
    # print(sequence0)
    # for row in rows:
    #     print(row)

    # z   y
    #   x
    # y - z = x
    # -z = x - y
    # z = y - x
    reverse_values = [0]
    for r in range(len(rows)-1, -1, -1):
        reverse_values.append(rows[r][0] - reverse_values[-1])
    soln_b = sequence[0] - reverse_values[-1]

    return soln_a, soln_b


def test_extrapolate():
    inputs = ['0 3 6 9 12 15', '1 3 6 10 15 21', '10 13 16 21 30 45']
    sequences = [[int(n) for n in inp.split()] for inp in inputs]
    expected = [18, 28, 68]
    assert [extrapolate_value(seq)[0] for seq in sequences] == expected


def solve_a(sequences):
    return sum(extrapolate_value(seq)[0] for seq in sequences)


def test_solve_a():
    inputs = ['0 3 6 9 12 15', '1 3 6 10 15 21', '10 13 16 21 30 45']
    sequences = [[int(n) for n in inp.split()] for inp in inputs]
    assert solve_a(sequences) == 114


def solve_b(sequences):
    return sum(extrapolate_value(seq)[1] for seq in sequences)


def test_solve_b():
    inputs = ['0 3 6 9 12 15', '1 3 6 10 15 21', '10 13 16 21 30 45']
    sequences = [[int(n) for n in inp.split()] for inp in inputs]
    assert solve_b(sequences) == 2


def main():
    "Main program"
    import pyperclip
    with open('../../data/09/input09.txt', 'r') as infile:
        sequences = [[int(n) for n in t.strip().split()] for t in infile.readlines()]
    soln_a = solve_a(sequences)
    print('The sum of the extrapolated values is', soln_a)
    assert soln_a == 2038472161
    soln_b = solve_b(sequences)
    print('The sum of the reverse extrapolated values is', soln_b)
    assert soln_b == 1091
    pyperclip.copy(str(soln_b))


if __name__ == '__main__':
    main()