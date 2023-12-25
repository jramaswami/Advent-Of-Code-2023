"""
Advent of Code 2023
Day 25
Snowverload
jramaswami
"""


import collections
import functools
import operator


def read_input(path):
    edges = list()
    with open(path, 'r') as infile:
        for line in infile:
            line = line.strip()
            u, tokens = line.split(': ')
            for v in tokens.split():
                edges.append((u, v))
    return edges



def solve_a(edges):
    # Drawing graph with neato reveals that the edges to remove are:
    edges_to_remove = (('gsk', 'ncg'), ('gmr', 'ntx'), ('mrd', 'rjs'))

    # Create graph without those edges.
    graph = collections.defaultdict(list)
    edges_removed = 0
    for u, v in edges:
        if (u, v) in edges_to_remove or (v, u) in edges_to_remove:
            print('removing', u, '-', v)
            edges_removed += 1
        else:
            graph[u].append(v)
            graph[v].append(u)
    assert edges_removed == 3

    # Count the components created
    visited = set()
    component_size = dict()
    for root in graph:
        if root not in visited:
            visited.add(root)
            component_size[root] = 0
            queue = collections.deque()
            queue.append(root)
            while queue:
                u = queue.popleft()
                component_size[root] += 1
                for v in graph[u]:
                    if v not in visited:
                        queue.append(v)
                        visited.add(v)
    assert len(component_size) == 2
    return functools.reduce(operator.mul, component_size.values(), 1)


def main():
    "Main program"
    import pyperclip
    graph = read_input('../../data/25/input25.txt')
    # graph = read_input('../../data/25/test25a.txt')
    soln_a = solve_a(graph)
    print('You get', soln_a, 'if you multiply the sizes of these two groups together')
    pyperclip.copy(str(soln_a))


if __name__ == '__main__':
    main()