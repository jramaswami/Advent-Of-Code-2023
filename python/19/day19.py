"""
Advent of Code
Day 19
Aplenty
jramaswami
"""


import collections
import operator

Operation = collections.namedtuple('Operation', ['comparison', 'destination'])
Comparison = collections.namedtuple('Comparison', ['attribute', 'comparison', 'value'])

COMPARISONS = {'>': operator.gt, '<': operator.lt}

def parse_workflow(raw_workflow):
    workflow = []
    first_brace = raw_workflow.index('{')
    wf_name = raw_workflow[:first_brace]
    raw_ops = raw_workflow[first_brace+1:-1].split(',')
    for raw_op in raw_ops[:-1]:
        colon = raw_op.index(':')
        attribute = raw_op[0]
        comparison = COMPARISONS[raw_op[1]]
        value = int(raw_op[2:colon])
        destination = raw_op[colon+1:]
        workflow.append(Operation(Comparison(attribute, comparison, value), destination))
    # Last operation is an else operation
    workflow.append(Operation(None, raw_ops[-1]))
    return wf_name, workflow


def parse_workflows(raw_workflows):
    workflows = dict()
    for raw_workflow in raw_workflows:
        wf_name, workflow = parse_workflow(raw_workflow)
        workflows[wf_name] = workflow
    return workflows


def parse_parts(raw_parts):
    parts = []
    for raw_part in raw_parts:
        part = {}
        tokens = raw_part[1:-1].split(',')
        for token in tokens:
            attribute = token[0]
            value = int(token[2:])
            part[attribute] = value
        parts.append(part)
    return parts


def read_input(path):
    raw_workflows = []
    raw_parts = []
    with open(path, 'r') as infile:
        appending_to = raw_workflows
        for line in infile:
            line = line.strip()
            if line:
                appending_to.append(line)
            else:
                appending_to = raw_parts

    workflows = parse_workflows(raw_workflows)
    parts = parse_parts(raw_parts)

    return workflows, parts


def classify_part(part, workflows):
    # Start at in
    classifications = ['in']
    while classifications[-1] not in ['A', 'R']:
        for operation in workflows[classifications[-1]]:
            if operation.comparison is None:
                classifications.append(operation.destination)
                break
            else:
                if operation.comparison.comparison(part[operation.comparison.attribute], operation.comparison.value):
                    classifications.append(operation.destination)
                    break
    return classifications


def solve_a(parts, workflows):
    soln_a = 0
    for part in parts:
        classifications = classify_part(part, workflows)
        if classifications[-1] == 'A':
            soln_a += sum(part.values())
    return soln_a


def test_solve_a():
    workflows, parts = read_input('../../data/19/test19a.txt')
    expected = 19114
    result = solve_a(parts, workflows)
    assert result == expected


def main():
    "Main program"
    import pyperclip
    # workflows, parts = read_input('../../data/19/test19a.txt')
    workflows, parts = read_input('../../data/19/input19.txt')
    soln_a = solve_a(parts, workflows)
    print('The sum of the rating numbers is', soln_a)
    assert soln_a == 391132
    soln_b = 0
    pyperclip.copy(str(soln_b))


if __name__ == '__main__':
    main()
