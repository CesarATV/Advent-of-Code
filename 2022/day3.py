import argparse

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day3.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day3_example.txt"

BELLOW_SMALLEST_INTEGER_VALUE_LOWERCASE_LETTER = ord("a")
SMALLEST_INTEGER_VALUE_FOR_UPPERCASE_LETTER = ord("A")
PRIORITY_LOWERCASE_LETTER = 1
PRIORITY_UPPERCASE_LETTER = 27
LAST_UPPERCASE_LETTER_INTEGER_VALUE = ord("Z")


def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 3: Rucksack Reorganization")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]



def solve_first_part(lines):
    total_priority_value = 0
    for line in lines:
        half_marker = len(line) // 2
        first_compartment = line[:half_marker]
        second_compartment = line[half_marker:]
        
        same_letter = ''
        for first_comp_letter in first_compartment:
            for second_comp_letter in second_compartment:
                if(first_comp_letter == second_comp_letter):
                    same_letter = first_comp_letter
                    break
            if same_letter != '':
                break
            
        if ord(same_letter) <= LAST_UPPERCASE_LETTER_INTEGER_VALUE:
            # capital letter
            total_priority_value += ord(same_letter) - SMALLEST_INTEGER_VALUE_FOR_UPPERCASE_LETTER + PRIORITY_UPPERCASE_LETTER
        else:
            # lowercase letter
            total_priority_value += ord(same_letter) - BELLOW_SMALLEST_INTEGER_VALUE_LOWERCASE_LETTER + PRIORITY_LOWERCASE_LETTER

    print("The total priority value of the items in common is", total_priority_value)


def solve_second_part(lines):
    total_priority_value = 0
    group_counter = 0
    for line in lines:
        if group_counter == 0:
            line1 = line
            group_counter += 1
            continue
        elif group_counter == 1:
            line2 = line
            group_counter += 1
            continue
        elif group_counter == 2:
            line3 = line
            group_counter = 0
        

        same_letter = ''
        for line1_letter in line1:
            for line2_letter in line2:
                if line1_letter == line2_letter:
                    for line3_letter in line3:
                        if line1_letter == line3_letter:
                            same_letter = line1_letter
                            break
                
                if same_letter != '':
                    break
            if same_letter != '':
                break
                    
        if ord(same_letter) <= LAST_UPPERCASE_LETTER_INTEGER_VALUE:
            # capital letter
            total_priority_value += ord(same_letter) - SMALLEST_INTEGER_VALUE_FOR_UPPERCASE_LETTER + PRIORITY_UPPERCASE_LETTER
        else:
            # lowercase letter
            total_priority_value += ord(same_letter) - BELLOW_SMALLEST_INTEGER_VALUE_LOWERCASE_LETTER + PRIORITY_LOWERCASE_LETTER

    print("The total priority value of the items in common for three-Elf groups is", total_priority_value)


def main(file_name):    
    with open(file_name) as file:
        lines = file.read().splitlines()
    while lines[-1] == "": # remove last empty lines, if any. They do not add information and can cause confusion
        lines.pop()

    solve_first_part(lines)
    solve_second_part(lines)


if __name__ == "__main__":
    main(parse_file_name())


