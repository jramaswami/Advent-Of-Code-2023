"""
Advent of Code
Day 15
Lens Library
jramaswami
"""


import collections


def compute_hash(s):
    x = 0
    for c in s:
        x += ord(c)
        x *= 17
        x %= 256
    return x


def test_compute_hash():
    assert compute_hash("HASH") == 52
    tokens = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'.split(',')
    expected = [30,253,97,47,14,180,9,197,48,214,231]
    result = [compute_hash(t) for t in tokens]
    assert result == expected


def solve_a(init_seq):
    return sum(compute_hash(t.strip()) for t in init_seq.split(','))


def test_solve_a():
    assert solve_a('rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7') == 1320


def read_input(path):
    with open(path, 'r') as infile:
        t = infile.readline().strip()
    return t


Lens = collections.namedtuple('Lens', ['label', 'focal_length'])


def tick(token, boxes):
    # Determine the operation:
    if token[-1] == '-':
        label = token[:-1]
        bi = compute_hash(label)
        boxes[bi] = [t for t in boxes[bi] if t.label != label]
    else:
        label, focal_length = token.split('=')
        focal_length = int(focal_length)
        new_lens = Lens(label, focal_length)
        bi = compute_hash(label)
        box_ = []
        found_old_lens = False
        for lens in boxes[bi]:
            if lens.label == new_lens.label:
                box_.append(new_lens)
                found_old_lens = True
            else:
                box_.append(lens)
        if not found_old_lens:
            box_.append(new_lens)
        boxes[bi] = box_


def boxes_str(boxes):
    box_strings = []
    for b, box in enumerate(boxes):
        if box:
            lenses = []
            for lens in box:
                lenses.append(f'[{lens.label} {lens.focal_length}]')
            bs = ' '.join(lenses)
            box_strings.append(f'Box {b}: {bs}')
    return '\n'.join(box_strings)


def test_tick():
    tokens = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'.split(',')
    boxes = [[] for _ in range(256)]
    result = []
    for t in tokens:
        tick(t, boxes)
        result.append(f'After "{t}":\n{boxes_str(boxes)}\n')
    result = '\n'.join(result)

    with open('../../data/15/result15a.txt') as infile:
        expected = infile.read()

    assert result == expected


def compute_focusing_power(boxes):
    fp = 0
    for b, box in enumerate(boxes, start=1):
        for i, lens in enumerate(box, start=1):
            fp += (b * i * lens.focal_length)
    return fp


def solve_b(input_seq):
    tokens = input_seq.split(',')
    boxes = [[] for _ in range(256)]
    for t in tokens:
        tick(t, boxes)
    return compute_focusing_power(boxes)


def test_solve_b():
    seq = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'
    assert solve_b(seq) == 145


def main():
    "Main program"
    import pyperclip
    init_seq = read_input('../../data/15/input15.txt')
    soln_a = solve_a(init_seq)
    print('The sum of the results is', soln_a)
    assert soln_a == 519041
    soln_b = solve_b(init_seq)
    print('The focusing power of the configuration is', soln_b)
    assert soln_b == 260530
    pyperclip.copy(str(soln_b))


if __name__ == '__main__':
    main()