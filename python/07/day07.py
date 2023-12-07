"""
Advent of Code
Day 7
Camel Cards
jramaswami
"""


import collections
import enum
import functools


CARD_ORDER = 'AKQJT98765432'[::-1]


class HandType(enum.IntEnum):
    HighCard = 1,
    OnePair = 2,
    TwoPair = 3,
    ThreeOfAKind = 4,
    FullHouse = 5,
    FourOfAKind = 6,
    FiveOfAKind = 7,


def compute_hand_type(cards):
    card_freqs = collections.Counter(cards)
    freq_freqs = collections.Counter(card_freqs.values())
    if freq_freqs[5] > 0:
        return HandType.FiveOfAKind
    elif freq_freqs[4] > 0:
        return HandType.FourOfAKind
    elif freq_freqs[3] > 0 and freq_freqs[2] > 0:
        return HandType.FullHouse
    elif freq_freqs[3] > 0:
        return HandType.ThreeOfAKind
    elif freq_freqs[2] > 1:
        return HandType.TwoPair
    elif freq_freqs[2] > 0:
        return HandType.OnePair
    return HandType.HighCard


def test_compute_hand_type():
    assert compute_hand_type('AAAAA') == HandType.FiveOfAKind
    assert compute_hand_type('AA8AA') == HandType.FourOfAKind
    assert compute_hand_type('23332') == HandType.FullHouse
    assert compute_hand_type('TTT98') == HandType.ThreeOfAKind
    assert compute_hand_type('23432') == HandType.TwoPair
    assert compute_hand_type('A234A') == HandType.OnePair
    assert compute_hand_type('23456') == HandType.HighCard


@functools.total_ordering
class Hand:
    def __init__(self, cards, bid=0):
        self.cards = cards
        self.hand_type = compute_hand_type(cards)
        self.bid = bid
        self.values = [CARD_ORDER.find(c) for c in self.cards]

    def __eq__(self, other):
        return self.cards == other.cards

    def __lt__(self, other):
        if self.hand_type < other.hand_type:
            return True
        if self.hand_type == other.hand_type:
            for a, b in zip(self.values, other.values):
                if a < b:
                    return True
                if a > b:
                    return False

        return False

    def __repr__(self):
        return f'Hand({self.cards}, {self.bid}, {self.hand_type.name} {self.values})'


def test_rank_hand():
    assert Hand('2AAAA') < Hand('33332')
    assert Hand('77788') < Hand('77888')
    assert Hand('KTJJT') < Hand('KK677')
    assert Hand('9K328') < Hand('A6852')



def test_sorting():
    hands = [Hand(c) for c in ['32T3K', 'T55J5', 'KK677', 'KTJJT', 'QQQJA']]
    expected = [Hand(c) for c in ['32T3K', 'KTJJT', 'KK677', 'T55J5', 'QQQJA']]
    hands.sort()
    assert hands == expected

    hands = [Hand('A6852'), Hand('9K328')]
    expected = [Hand('9K328'), Hand('A6852')]
    hands.sort()
    assert hands == expected


def solve_a(hands):
    soln = 0
    hands.sort()
    for i, h in enumerate(hands, start=1):
        soln += (i * h.bid)
    return soln


def test_solve_a():
    hands = [Hand(c, b) for c, b in [('32T3K', 765), ('T55J5', 684), ('KK677', 28), ('KTJJT', 220), ('QQQJA', 483)]]
    assert solve_a(hands) == 6440


def parse_input(lines):
    hands = []
    for line in lines:
        cards, bid = line.split()
        hands.append(Hand(cards.strip(), int(bid.strip())))
    return hands


def main():
    "Main program"
    import sys
    import pyperclip
    lines = sys.stdin.readlines()
    hands = parse_input(lines)
    soln_a = solve_a(hands)
    print('The total winnings are', soln_a)
    assert soln_a == 251058093
    pyperclip.copy(str(soln_a))



if __name__ == '__main__':
    main()