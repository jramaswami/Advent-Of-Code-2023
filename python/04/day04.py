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


def count_your_winning_numbers(winning_numbers, numbers_you_have):
    "Return the count of cards that you have that are in winning numbers."
    return sum(1 for n in numbers_you_have if n in winning_numbers)


def compute_card_score(winning_numbers, numbers_you_have):
    "Compute the score of the card according to the Elf's rules."
    your_winning_numbers = count_your_winning_numbers(winning_numbers, numbers_you_have)
    if your_winning_numbers > 0:
        return pow(2, your_winning_numbers - 1)
    return 0


def test_compute_card_score():
    with open('../../data/04/test04a.txt') as testfile:
        cards = [parse_card(line) for line in testfile.readlines()]
    expected = [8, 2, 2, 1, 0, 0]
    assert [compute_card_score(*c) for c in cards] == expected


def solve_a(cards):
    "Return the total score of the cards in the input lines."
    return sum(compute_card_score(*c) for c in cards)


def test_solve_a():
    with open('../../data/04/test04a.txt') as testfile:
        cards = [parse_card(l) for l in testfile.readlines()]
    assert solve_a(cards) == 13


def solve_b(cards):
    "Return the number of cards you end up with after all the copying."
    card_copies = [1 for _ in cards]
    for card_index, _ in enumerate(cards):
        copies_you_win = count_your_winning_numbers(*cards[card_index])
        for offset in range(1, copies_you_win+1):
            card_copies[card_index+offset] += card_copies[card_index]
    return sum(card_copies)


def test_solve_b():
    with open('../../data/04/test04a.txt') as testfile:
        cards = [parse_card(l) for l in testfile.readlines()]
    assert solve_b(cards) == 30


def main():
    "Main program"
    import pyperclip
    with open('../../data/04/input04.txt') as infile:
        cards = [parse_card(l) for l in infile.readlines()]
    soln_a = solve_a(cards)
    print('The total points for the scratchcards is', soln_a)
    assert soln_a == 23028
    soln_b = solve_b(cards)
    print('You end up with', soln_b, 'total scratchcards')
    assert soln_b == 9236992
    pyperclip.copy(str(soln_b))


if __name__ == '__main__':
    main()