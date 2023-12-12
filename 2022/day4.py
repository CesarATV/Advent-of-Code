import argparse

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day4.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day4_example.txt"


def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 4: Camp Cleanup")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]


def solve_first_part(lines):
    n_fully_overlaping_pairs = 0
    for line in lines:
        elf1, elf2 = line.split(",")
        elf1_task_first, elf1_task_last = [int(section_number) for section_number in elf1.split("-")]
        elf2_task_first, elf2_task_last = [int(section_number) for section_number in elf2.split("-")]
        
        if elf1_task_first <= elf2_task_first and elf1_task_last >= elf2_task_last:
            n_fully_overlaping_pairs += 1
        elif elf2_task_first <= elf1_task_first and elf2_task_last >= elf1_task_last:
            n_fully_overlaping_pairs +=1

    print("The assignment pairs fully overlap", n_fully_overlaping_pairs, "times")


def solve_second_part(lines):
    n_overlaping_pairs = 0
    for line in lines:
        elf1, elf2 = line.split(",")
        elf1_task_first, elf1_task_last = [int(section_number) for section_number in elf1.split("-")]
        elf2_task_first, elf2_task_last = [int(section_number) for section_number in elf2.split("-")]
        
        if (
            (elf1_task_first <= elf2_task_first and elf1_task_last >= elf2_task_first) or
            (elf1_task_first <= elf2_task_last and elf1_task_last >= elf2_task_last) 
        ):
            n_overlaping_pairs += 1
        elif (
            (elf2_task_first <= elf1_task_first and elf2_task_last >= elf1_task_first) or
            (elf2_task_first <= elf1_task_last and elf2_task_last >= elf1_task_last) 
        ):
            n_overlaping_pairs +=1

    print("The assignment pairs overlap", n_overlaping_pairs, "times")


def main(file_name):    
    with open(file_name) as file:
        lines = file.read().splitlines()
    while lines[-1] == "": # remove last empty lines, if any. They do not add information and can cause confusion
        lines.pop()

    solve_first_part(lines)
    solve_second_part(lines)


if __name__ == "__main__":
    main(parse_file_name())


