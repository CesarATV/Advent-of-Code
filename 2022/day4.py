import argparse
import numpy as np

PUZZLE_INPUT_FILE_NAME = "puzzleInputs/day4.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzleInputs/day4_example.txt"


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


def first_part(lines):
    fully_overlaping_pair = 0
    for line in lines:
        elf1, elf2 = line.split(",")
        elf1_task_first, elf1_task_last = np.array(elf1.split("-")).astype(int)
        elf2_task_first, elf2_task_last = np.array(elf2.split("-")).astype(int)
        
        if(elf1_task_first <= elf2_task_first and elf1_task_last >= elf2_task_last):
            fully_overlaping_pair += 1
        elif(elf2_task_first <= elf1_task_first and elf2_task_last >= elf1_task_last):
            fully_overlaping_pair +=1

    print("The assignment pairs fully overlap", fully_overlaping_pair, "times")


def second_part(lines):
    overlaping_pair = 0
    for line in lines:
        elf1, elf2 = line.split(",")
        elf1_task_first, elf1_task_last = np.array(elf1.split("-")).astype(int)
        elf2_task_first, elf2_task_last = np.array(elf2.split("-")).astype(int)
        
        if(
            (elf1_task_first <= elf2_task_first and elf1_task_last >= elf2_task_first) or
            (elf1_task_first <= elf2_task_last and elf1_task_last >= elf2_task_last) 
        ):
            overlaping_pair += 1
        elif(
            (elf2_task_first <= elf1_task_first and elf2_task_last >= elf1_task_first) or
            (elf2_task_first <= elf1_task_last and elf2_task_last >= elf1_task_last) 
        ):
            overlaping_pair +=1

    print("The assignment pairs overlap", overlaping_pair, "times")


def main(file_name):    
    with open(file_name) as file:
        lines = file.read().splitlines()
    while lines[-1] == "": # remove last empty lines, if any. They do not add information and can cause confusion
        lines.pop()

    first_part(lines)
    second_part(lines)


if __name__ == "__main__":
    main(parse_file_name())


