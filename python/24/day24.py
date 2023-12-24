"""
Advent of Code
Day 24
Never Tell Me The Odds
jramaswami

Thank you HyperNeutrino!
REF: https://www.youtube.com/watch?v=guOyA7Ijqgk
"""


import collections
import math
import sympy


Vector = collections.namedtuple('Vector', ['x', 'y', 'z'])
Vector.__add__ = lambda a, b: Vector(a.x + b.x, a.y + b.y, a.z + b.z)
Vector.__mul__ = lambda a, x: Vector(a.x * x, a.y * x, a.z * x)


Hailstone = collections.namedtuple('Hailstone', ['position', 'velocity'])


def parse_input(path):
    hailstones = []
    with open(path, 'r') as infile:
        for line in infile:
            line = line.strip()
            position_clause, velocity_clause = line.split(' @ ')
            position_tokens = (int(p) for p in position_clause.split(', '))
            velocity_tokens = (int(v) for v in velocity_clause.split(', '))
            position = Vector._make(position_tokens)
            velocity = Vector._make(velocity_tokens)
            hailstones.append(Hailstone(position, velocity))
    return hailstones


def solve_a(hailstones, range):
    eqns = []
    for hs in hailstones:
        m = hs.velocity.y / hs.velocity.x
        c = (m * hs.position.x) - hs.position.y
        eqns.append((m, c))

    soln_a = 0
    for i, eqn1 in enumerate(eqns):
        for j, eqn2 in enumerate(eqns[i+1:], start=i+1):
            # eqn1[0]x - eqn1[1] = eqn2[0]x - eqn2[1]
            # (eqn1[0]- eqn2[0])x = eqn1[1] - eqn2[1]
            # (eqn1[1] - eqn2[1]) / (eqn1[0] - eqn2[0])
            if math.isclose(eqn1[0], eqn2[0]):
                continue
            x = (eqn1[1] - eqn2[1]) / (eqn1[0] - eqn2[0])
            y1 = (eqn1[0] * x) - eqn1[1]
            y2 = (eqn2[0] * x) - eqn2[1]
            if range[0] <= x <= range[1] and range[0] <= y1 <= range[1]:
                # The intersection must be in the future for both hailstones
                # so the sign of dx and dy must the the same as the hailstone's
                # velocity ont he x and y axis respectively
                future1 = future2 = False
                dx1 = x - hailstones[i].position.x
                dy1 = y1 - hailstones[i].position.y
                if dx1 * hailstones[i].velocity.x > 0 and dy1 * hailstones[i].velocity.y > 0:
                    future1 = True
                dx2 = x - hailstones[j].position.x
                dy2 = y2 - hailstones[j].position.y
                if dx2 * hailstones[j].velocity.x > 0 and dy2 * hailstones[j].velocity.y > 0:
                    future2 = True

                if future1 and future2:
                    soln_a += 1
    return soln_a


def test_solve_a():
    hailstones = parse_input('../../data/24/test24a.txt')
    assert solve_a(hailstones, (7, 27)) == 2


def solve_b(hailstones):
    xr, yr, zr, vxr, vyr, vzr = sympy.symbols('xr, yr, zr, vxr, vyr, vzr')
    equations = []
    for (sx, sy, sz), (vx, vy, vz) in hailstones:
        equations.append((xr - sx) * (vy - vyr) - (yr - sy) * (vx - vxr))
        equations.append((yr - sy) * (vz - vzr) - (zr - sz) * (vy - vyr))
    (answer, ) = sympy.solve(equations)
    soln_b = answer[xr] + answer[yr] + answer[zr]
    return soln_b


def test_solve_b():
    hailstones = parse_input('../../data/24/test24a.txt')
    assert solve_b(hailstones) == 47


def main():
    "Main program"
    import pyperclip
    hailstones = parse_input('../../data/24/input24.txt')
    soln_a = solve_a(hailstones, (200000000000000, 400000000000000))
    print(soln_a, 'intersections between hailstones will occur')
    assert soln_a == 16812
    soln_b = solve_b(hailstones)
    print('You get', soln_b, 'if you add up the X, Y, and Z coordinates of that initial position')
    assert soln_b == 880547248556435
    pyperclip.copy(str(soln_b))


if __name__ == '__main__':
    main()