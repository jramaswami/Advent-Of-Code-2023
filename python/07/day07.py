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
CARD_ORDER_WITH_JOKERS = 'AKQT98765432J'[::-1]


class HandType(enum.IntEnum):
    HighCard = 1,
    OnePair = 2,
    TwoPair = 3,
    ThreeOfAKind = 4,
    FullHouse = 5,
    FourOfAKind = 6,
    FiveOfAKind = 7,


def compute_hand_type_with_jokers(cards):
    best_hand_type = HandType.HighCard
    for joker_becomes in CARD_ORDER_WITH_JOKERS:
        cards0 = cards.replace('J', joker_becomes)
        best_hand_type = max(best_hand_type, compute_hand_type(cards0))
    return best_hand_type


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


def test_compute_hand_type_with_jokers():
    assert compute_hand_type_with_jokers('QJJQ2') == HandType.FourOfAKind
    assert compute_hand_type_with_jokers('32T3K') == HandType.OnePair
    assert compute_hand_type_with_jokers('KK677') == HandType.TwoPair
    assert compute_hand_type_with_jokers('T55J5') == HandType.FourOfAKind
    assert compute_hand_type_with_jokers('KTJJT') == HandType.FourOfAKind
    assert compute_hand_type_with_jokers('QQQJA') == HandType.FourOfAKind


@functools.total_ordering
class Hand:
    def __init__(self, cards, bid=0, with_jokers=False):
        self.cards = cards
        if with_jokers:
            self.hand_type = compute_hand_type_with_jokers(cards)
        else:
            self.hand_type = compute_hand_type(cards)

        self.bid = bid
        card_order = CARD_ORDER
        if with_jokers:
            card_order = CARD_ORDER_WITH_JOKERS
        self.values = [card_order.find(c) for c in self.cards]
        self.with_jokers = with_jokers

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
        return f'Hand({self.cards}, {self.bid}, {self.with_jokers}, {self.hand_type.name} {self.values})'


def test_rank_hand():
    assert Hand('2AAAA') < Hand('33332')
    assert Hand('77788') < Hand('77888')
    assert Hand('KTJJT') < Hand('KK677')
    assert Hand('9K328') < Hand('A6852')

    assert Hand('JKKK2', with_jokers=True) < Hand('QQQQ2', with_jokers=True)


def test_sorting():
    hands = [Hand(c) for c in ['32T3K', 'T55J5', 'KK677', 'KTJJT', 'QQQJA']]
    expected = [Hand(c) for c in ['32T3K', 'KTJJT', 'KK677', 'T55J5', 'QQQJA']]
    hands.sort()
    assert hands == expected

    hands = [Hand('A6852'), Hand('9K328')]
    expected = [Hand('9K328'), Hand('A6852')]
    hands.sort()
    assert hands == expected

    hands = [Hand(c, with_jokers=True) for c in ['32T3K', 'T55J5', 'KK677', 'KTJJT', 'QQQJA']]
    expected = [Hand(c, with_jokers=True) for c in ['32T3K', 'KK677', 'T55J5', 'QQQJA', 'KTJJT']]
    hands.sort()
    assert hands == expected


def solve(hands):
    soln = 0
    hands.sort()
    for i, h in enumerate(hands, start=1):
        soln += (i * h.bid)
    return soln


def test_solve():
    hands = [Hand(c, b) for c, b in [('32T3K', 765), ('T55J5', 684), ('KK677', 28), ('KTJJT', 220), ('QQQJA', 483)]]
    assert solve(hands) == 6440
    hands_with_jokers = [Hand(h.cards, h.bid, True) for h in hands]
    assert solve(hands_with_jokers) == 5905


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
    soln_a = solve(hands)
    print('The total winnings are', soln_a)
    assert soln_a == 251058093
    hands_with_jokers = [Hand(h.cards, h.bid, True) for h in hands]
    soln_b = solve(hands_with_jokers)
    print('The total winnings with wild jokers are', soln_b)
    assert soln_b == 249781879
    pyperclip.copy(str(soln_b))


if __name__ == '__main__':
    main()