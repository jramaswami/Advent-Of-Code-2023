"""
Advent of Code
Day 1
Trebuchet?!
jramaswami
"""

DIGITS = {
    "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9,
}


def recover_calibration_code_a(line):
    "Return two-digit number formed by the first and last digit"
    digits = [c for c in line if c.isdigit()]
    return (int(digits[0]) * 10 ) + int(digits[-1])


def test_recover_calibration_code():
    "Test for recover_calibration_code()"
    lines = ["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"]
    expected = [12, 38, 15, 77]
    assert [recover_calibration_code_a(t) for t in lines] == expected


def get_calibration_value(lines, func):
    "Return the calibration value for the given lines"
    return sum(func(t) for t in lines)


def test_get_calibration_value():
    "Test for get_calibration_value()"
    lines_a = ["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"]
    expected_a = 142
    assert get_calibration_value(lines_a, recover_calibration_code_a) == expected_a
    lines_b = [
        "two1nine", "eightwothree", "abcone2threexy",
        "xtwone3four", "4nineeightseve2",
        "zoneight234", "7pqrstsixteen",
    ]
    expected_b = 281
    assert get_calibration_value(lines_b, recover_calibration_code_b) == expected_b


def recover_calibration_code_b(line):
    "Return calibration code taking into account digits as words"
    left_posns = [line.find(d) for d in DIGITS]
    right_posns = [line.rfind(d) for d in DIGITS]
    _, left_digit = min((i, d) for i, d in zip(left_posns, DIGITS) if i >= 0)
    _, right_digit = max((i, d) for i, d in zip(right_posns, DIGITS) if i >= 0)
    return (10 * DIGITS[left_digit]) + DIGITS[right_digit]


def test_recover_calibration_code_b():
    "Tests for recover_calibration_code_b"
    lines = [
        "two1nine", "eightwothree", "abcone2threexy",
        "xtwone3four", "4nineeightseve2",
        "zoneight234", "7pqrstsixteen",
        '21xfxfourmzmqbqp1'
    ]
    expected = [29, 83, 13, 24, 42, 14, 76, 21]
    assert [recover_calibration_code_b(l) for l in lines] == expected



def main():
    "Main program."
    import pyperclip
    import sys
    lines = [line.strip() for line in sys.stdin]
    calibration_value_a = get_calibration_value(lines, recover_calibration_code_a)
    print('The calibration a is', calibration_value_a)
    assert calibration_value_a == 56042
    calibration_value_b = get_calibration_value(lines, recover_calibration_code_b)
    print('The calibration b is', calibration_value_b)
    assert calibration_value_b == 55358
    pyperclip.copy(str(calibration_value_b))
    print('It has been copied to the clipboard')


if __name__ == '__main__':
    main()