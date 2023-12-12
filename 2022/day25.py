import argparse

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day25.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day25_example.txt"

MINUS_SIGN = "-"
DOUBLE_MINUS_SIGN = "="
SNAFU_RADIX = 5


def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 25: Full of Hot Air")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]


def SNAFU_to_decimal(SNAFU_number):
    decimal_number = 0
    for digit_place, snafu_digit_char in enumerate(SNAFU_number[::-1]):

        if snafu_digit_char == MINUS_SIGN:
            snafu_digit = -1
        elif snafu_digit_char == DOUBLE_MINUS_SIGN:
            snafu_digit = -2
        else:
            snafu_digit = int(snafu_digit_char)

        decimal_number += snafu_digit * SNAFU_RADIX**digit_place

    return decimal_number


def decimal_to_SNAFU(decimal_number):
    radixed_number = ""
    floored_fraction = decimal_number
    while floored_fraction != 0:
        floored_fraction, remainder = divmod(floored_fraction,SNAFU_RADIX)
        radixed_number += str(remainder)
    
    radixed_number = radixed_number[::-1]

    SNAFU_number_list = list(radixed_number)
    carried_value = 0
    for idx in reversed(range(len(radixed_number))):
        radixed_digit = int(radixed_number[idx])
        if carried_value == 1:
            radixed_digit +=1 
            carried_value = 0
        
        if radixed_digit == 4:
            SNAFU_number_list[idx] = "-"
            carried_value = 1
        elif radixed_digit == 3:
            SNAFU_number_list[idx] = "="
            carried_value = 1
        else:
            SNAFU_number_list[idx] = str(radixed_digit)

    if carried_value==1:
        SNAFU_number = "1" + SNAFU_number

    SNAFU_number = "".join(SNAFU_number_list)
    return SNAFU_number


def solve_first_part(lines):
    number_sum_decimal = 0
    for line in lines:
        number_sum_decimal += SNAFU_to_decimal(line)

    number_sum_SNAFU = decimal_to_SNAFU(number_sum_decimal)

    print("The sum of the numbers in decimal is {}, which is equivalent to {} when using SNAFU".format(number_sum_decimal, number_sum_SNAFU))


def main(file_name): 
    with open(file_name) as file:
        lines = file.read().splitlines()
    while lines[-1] == "": # remove last empty lines, if any. They do not add information and can cause confusion
        lines.pop()

    solve_first_part(lines)
    # there is no second part to be coded for this puzzle


if __name__ == "__main__":
    main(parse_file_name())


