"""
Advent of Code
Day 1
Trebuchet?!
jramaswami
"""


def recover_calibration_code(line):
    "Return two-digit number formed by the first and last digit"
    digits = [c for c in line if c.isdigit()]
    return (int(digits[0]) * 10 ) + int(digits[-1])


def test_recover_calibration_code():
    "Test for recover_calibration_code()"
    lines = ["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"]
    expected = [12, 38, 15, 77]
    assert [recover_calibration_code(t) for t in lines] == expected


def get_calibration_value(lines):
    "Return the calibration value for the given lines"
    return sum(recover_calibration_code(t) for t in lines)


def test_get_calibration_value():
    "Test for get_calibration_value()"
    lines = ["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"]
    expected = 142
    assert get_calibration_value(lines) == expected


def main():
    "Main program."
    import pyperclip
    import sys
    calibration_value = get_calibration_value(sys.stdin)
    print('The calibration value is', calibration_value)
    assert calibration_value == 56042
    pyperclip.copy(str(calibration_value))
    print('It has been copied to the clipboard')


if __name__ == '__main__':
    main()