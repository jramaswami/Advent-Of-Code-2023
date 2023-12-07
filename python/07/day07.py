"""
Advent of Code
Day 7
Camel Cards
jramaswami

251647056 is too high
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
    def __init__(self, cards):
        self.cards = cards
        self.hand_type = compute_hand_type(cards)

    def __eq__(self, other):
        return self.cards == other.cards

    def __lt__(self, other):
        if self.hand_type < other.hand_type:
            return True
        if self.hand_type == other.hand_type:
            for my_card, other_card in zip(self.cards, other.cards):
                if CARD_ORDER.find(my_card) < CARD_ORDER.find(other_card):
                    return True

        return False

    def __repr__(self):
        return f'Hand({self.cards}, {self.hand_type.name})'


def test_rank_hand():
    assert Hand('2AAAA') < Hand('33332')
    assert Hand('77788') < Hand('77888')
    assert Hand('KTJJT') < Hand('KK677')


def test_sorting():
    hands = [Hand(c) for c in ['32T3K', 'T55J5', 'KK677', 'KTJJT', 'QQQJA']]
    expected = [Hand(c) for c in ['32T3K', 'KTJJT', 'KK677', 'T55J5', 'QQQJA']]
    hands.sort()
    assert hands == expected


def solve_a(hands, bids):
    soln = 0
    for i, (h, b) in enumerate(sorted((h, b) for h, b in zip(hands, bids)), start=1):
        soln += (i * b)
    return soln


def test_solve_a():
    hands = [Hand(c) for c in ['32T3K', 'T55J5', 'KK677', 'KTJJT', 'QQQJA']]
    bids = [765, 684, 28, 220, 483]
    assert solve_a(hands, bids) == 6440


def parse_input(lines):
    hands = []
    bids = []
    for line in lines:
        cards, bid = line.split()
        hands.append(Hand(cards.strip()))
        bids.append(int(bid.strip()))
    return hands, bids


def main():
    "Main program"
    import sys
    import pyperclip
    lines = sys.stdin.readlines()
    hands, bids = parse_input(lines)
    soln_a = solve_a(hands, bids)
    print('The total winnings are', soln_a)
    pyperclip.copy(str(soln_a))



if __name__ == '__main__':
    main()