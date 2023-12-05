"""
Advent of Code
Day 5
If You Give A Seed A Fertilizer
jramaswami
"""


import collections


Entry = collections.namedtuple('Entry', ['next', 'curr', 'range'])


def parse_input(lines):
    "Parse input and return seeds and almanac"
    # Read seeds line.
    seeds_line = lines[0]
    # Parse seeds line.
    _, tokens = seeds_line.split(': ')
    seeds = tuple(int(t) for t in tokens.split())
    i = 2
    almanac = []
    while i < len(lines):
        # Header line.
        assert lines[i]
        # Create a new map for it.
        almanac.append([])
        i += 1
        while i < len(lines) and lines[i]:
            almanac[-1].append(Entry(*(int(t) for t in lines[i].split())))
            i += 1
        # Skip blank line
        i += 1
    return seeds, almanac


def transform_seed(seed, almanac):
    "Transform a seed through all the transformations in the almanac."
    for t, transformation in enumerate(almanac):
        for entry in transformation:
            seed0 = seed
            if entry.curr <= seed < (entry.curr + entry.range):
                delta = seed - entry.curr
                seed = entry.next + delta
                break
    return seed


def solve_a(seeds, almanac):
    "Solve first part of puzzle."
    return min(transform_seed(seed, almanac) for seed in seeds)


def solve_b(seeds, almanac):
    "Solve second part of puzzle."
    # Transform seeds into ranges.
    seed_ranges = []
    for i, _ in enumerate(seeds):
        if i % 2 == 0:
            seed_ranges.append((seeds[i], seeds[i] + seeds[i+1] - 1))
    # Transform almanac into ranges
    almanac0 = []
    for page in almanac:
        almanac0.append([])
        for entry in page:
            delta = entry.next - entry.curr
            almanac0[-1].append((entry.curr, entry.curr + entry.range - 1, delta))

    # Take a sum of the number of seeds we have.  We will uses this to make sure
    # that we do not lose any seeds along the way.
    checksum = sum(seed[1] - seed[0] + 1 for seed in seed_ranges)
    # For every page in the almanac, we will have a current queue and the queue
    # for the next page of the almanac.
    currq = collections.deque(seed_ranges)
    nextq = collections.deque()
    # For every page compute all the transformations *by range*.
    for page in almanac0:
        while currq:
            # For each range in the queue, see if there is a transformation that
            # overlaps that range.
            x1, x2 = currq.popleft()
            overlap_found = False
            for y1, y2, d in page:
                if max(x1,y1) <= min(x2,y2):
                    # If there is an overlap, compute the range of the overlap
                    # and any ranges that do not overlap.  Put each of the
                    # nonoverlapping ranges in the current queue.
                    overlap_found = True
                    overlap = (max(x1, y1)+d, min(x2, y2)+d)
                    nonoverlap_sum = 0
                    if x1 < y1:
                        # xxxxx
                        #   yyyyyy
                        nonoverlap = (x1, y1-1)
                        currq.append(nonoverlap)
                        nonoverlap_sum += (nonoverlap[1] - nonoverlap[0] + 1)
                    if x2 > y2:
                        #   xxxx
                        # yyyy
                        nonoverlap = (y2+1,x2)
                        currq.append(nonoverlap)
                        nonoverlap_sum += (nonoverlap[1] - nonoverlap[0] + 1)

                    # Check to make sure that the ranges we broke into still
                    # sum to the same number of seeds.
                    overlap_sum = (overlap[1] - overlap[0] + 1)
                    range_sum = (x2 - x1 + 1)
                    assert overlap_sum + nonoverlap_sum == range_sum
                    # Put the transformed overlap into the queue for the next
                    # page of the almanac.
                    nextq.append(overlap)
                    # Stop looking for a match for this range.
                    break
            # If there were no overlapping transformations on this page of the
            # almanac, put our range in the queue for the next page.
            if not overlap_found:
                nextq.append((x1,x2))
        # Check to make sure the queue for the next page of the almanac still
        # has the required number of seeds.
        checksum0 = sum(seed[1] - seed[0] + 1 for seed in nextq)
        assert checksum0 == checksum
        currq, nextq = nextq, collections.deque()

    # Return the minimum range start, as that will be the lowest location value.
    return min(t[0] for t in currq)


def main():
    "Main program"
    import sys
    import pyperclip
    with open(sys.argv[1]) as infile:
        lines = [t.strip() for t in infile.readlines()]
    seeds, almanac = parse_input(lines)
    soln_a = solve_a(seeds, almanac)
    print('The lowest location number is', soln_a)
    assert soln_a == 261668924
    soln_b = solve_b(seeds, almanac)
    print('The lowest location number with ranges is', soln_b)
    pyperclip.copy(str(soln_b))
    assert soln_b == 24261545


if __name__ == '__main__':
    main()