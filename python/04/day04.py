"""
Advent of Code
Day 4
Scratchcards
"""





def parse_card(line):
    """
    Parse the card from the given line.
    Returns a tuple of winning numbers and a tuple of numbers you have.
    """
    # Split away the card number.
    _, line = (t.strip() for t in line.split(':'))
    # Split the two lists of numbers
    winning_text, numbers_text = (t.strip() for t in line.split('|'))
    # Split out winning numbers
    winning_numbers = [int(t) for t in winning_text.split()]
    numbers_you_have = [int(t) for t in numbers_text.split()]
    return winning_numbers, numbers_you_have


def compute_card_score(winning_numbers, numbers_you_have):
    "Compute the score of the card according to the Elf's rules."
    your_winning_numbers = [n for n in numbers_you_have if n in winning_numbers]
    if your_winning_numbers:
        return pow(2, len(your_winning_numbers) - 1)
    return 0


def test_compute_card_score():
    with open('../../data/04/test04a.txt') as testfile:
        cards = [parse_card(line) for line in testfile.readlines()]
    expected = [8, 2, 2, 1, 0, 0]
    assert [compute_card_score(*c) for c in cards] == expected


def solve_a(lines):
    "Return the total score of the cards in the input lines."
    return sum(compute_card_score(*parse_card(l)) for l in lines)


def test_solve_a():
    with open('../../data/04/test04a.txt') as testfile:
        result = solve_a(testfile.readlines())
    assert result == 13


def main():
    "Main program"
    import sys
    import pyperclip
    lines = sys.stdin.readlines()
    soln_a = solve_a(lines)
    print('The total points for the scratchcards is', soln_a)
    assert soln_a == 23028
    pyperclip.copy(str(soln_a))


if __name__ == '__main__':
    main()