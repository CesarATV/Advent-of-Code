import argparse

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day1.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day1_example.txt"

NUMBER_OF_ELVES = 3


def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 1: Calorie Counting")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]


def solve_first_part(lines):
    most_calories = 0
    current_calories = 0
    for line in lines:
        if line == '':
            if(current_calories > most_calories):
                most_calories = current_calories
            current_calories = 0
                
        else:
            current_calories += int(line)

    print("The Elf that carries the most calories carries", most_calories)


def solve_second_part(lines):
    most_calories_array = [0 for _ in range(NUMBER_OF_ELVES)]
    current_calories = 0
    for line in lines:
        if line == '':
            if(current_calories > most_calories_array[0]):
                most_calories_array[0] = current_calories
                most_calories_array.sort() # place the lowest amount of calories at the beginning of the array
            current_calories = 0
                
        else:
            current_calories += int(line)

    sum_most_carried_calories = sum(most_calories_array)
    print("The {} Elves that carry most calories carry a total of {}. They carry {}".format(NUMBER_OF_ELVES,sum_most_carried_calories,most_calories_array[0]), end='')
    for elve_idx in range(1,NUMBER_OF_ELVES-1):
        print(", {}".format(most_calories_array[elve_idx]), end='')
    print(" and {} calories".format(most_calories_array[-1]))


def main(file_name):    
    with open(file_name) as file:
        lines = file.read().splitlines()
        lines += [""] # Be sure that there is an extra empty line at the end. This is just to make sure to check the maximum values in the upcoming loops of the functions

    solve_first_part(lines)
    solve_second_part(lines)


if __name__ == "__main__":
    main(parse_file_name())


