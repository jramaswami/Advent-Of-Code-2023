"""
Advent of Code
Day 22
Sand Slabs
jramaswami
"""


import collections


Vector = collections.namedtuple('Vector', ['x', 'y', 'z'])
Brick = collections.namedtuple('Brick', ['p1', 'p2', 'id'])
Brick.minz = lambda b: min(b.p1.z, b.p2.z)


def bricks_intersect_xy(b1, b2):
    if min(b2.p1.x, b2.p2.x) > max(b1.p1.x, b1.p2.x):
        # b2 misses to the right
        return False
    if max(b2.p1.x, b2.p2.x) < min(b1.p1.x, b1.p2.x):
        # b2 misses to the left
        return False
    if min(b2.p1.y, b2.p2.y) > max(b1.p1.y, b1.p2.y):
        # b2 misses to the above
        return False
    if max(b2.p1.y, b2.p2.y) < min(b1.p1.y, b1.p2.y):
        # b2 misses to the below
        return False

    return True


def parse_input(path):
    bricks = []
    with open(path, 'r') as infile:
        for line in infile:
            line = line.strip()
            left, right = line.split('~')
            p1 = Vector._make(int(x) for x in left.split(','))
            p2 = Vector._make(int(x) for x in right.split(','))
            bricks.append(Brick(p1, p2, len(bricks)+1))
    return bricks


def solve_a(bricks_):
    # Don't mutate and sort bricks by their minimum z coordinate
    bricks = collections.deque(sorted(bricks_, key=lambda b: b.minz()))
    # Build a graph from the ground up through the bricks.
    # Zero is the ground
    graph = [[] for _ in range(len(bricks)+1)]
    # Find bricks on the ground, that is bricks with z of one.
    grounded_bricks = []
    while bricks[0].p1.z == 1 or bricks[0].p1.z == 1:
        brick = bricks.popleft()
        grounded_bricks.append(brick)
        graph[0].append(brick.id)

    # In order, move the bricks to the ground, connecting them in a graph.
    while bricks:
        brick = bricks.popleft()
        x1, x2 = min(brick.p1.x, brick.p2.x), max(brick.p1.x, brick.p2.x)
        y1, y2 = min(brick.p1.y, brick.p2.y), max(brick.p1.y, brick.p2.y)
        # Find the brick to the largest z coordinate in the plane (x1,y1) (x2,y2)
        supports = []
        support_z = 0
        for gb in grounded_bricks:
            if bricks_intersect_xy(brick, gb):
                gb_maxz = max(gb.p1.z, gb.p2.z)
                if gb_maxz == support_z:
                    supports.append(gb)
                if supports is None or gb_maxz > support_z:
                    supports = [gb]
                    support_z = gb_maxz
        for gb in supports:
            graph[gb.id].append(brick.id)
        if support_z == 0:
            graph[0].append(brick.id)
        dz = min(brick.p1.z, brick.p2.z) - (support_z + 1)
        p1 = Vector(brick.p1.x, brick.p1.y, brick.p1.z - dz)
        p2 = Vector(brick.p2.x, brick.p2.y, brick.p2.z - dz)
        brick_ = Brick(p1, p2, brick.id)
        grounded_bricks.append(brick_)

    soln_a = 0
    for x in range(1, len(graph)):
        # Can this be removed?
        queue = collections.deque([0])
        visited = set()
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if v == x:
                    continue
                if v in visited:
                    continue
                queue.append(v)
                visited.add(v)

        if len(visited) == len(bricks_) - 1:
            soln_a += 1

    return soln_a


def test_solve_a():
    bricks = parse_input('../../data/22/test22a.txt')
    assert solve_a(bricks) == 5


def main():
    "Main program"
    import pyperclip
    bricks = parse_input('../../data/22/input22.txt')
    # bricks = parse_input('../../data/22/test22a.txt')
    soln_a = solve_a(bricks)
    print('The number of bricks you can disintegrate is', soln_a)
    assert soln_a == 509
    pyperclip.copy(str(soln_a))



if __name__ == '__main__':
    main()