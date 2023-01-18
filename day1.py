import argparse
import numpy as np

PUZZLE_INPUT_FILE_NAME = "PuzzleInputs/day1.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "PuzzleInputs/day1_example.txt"

NUMBER_ELVES = 3


def parse_file_name():
    parser = argparse.ArgumentParser(description="AoC day 1")
    parser.add_argument('file_name', type=str, default=PUZZLE_INPUT_FILE_NAME, nargs='?')
    parser.add_argument("-e", "--example", dest="use_example_file", action="store_true", help="use default (hardcoded) path of example file as file name")
    args = parser.parse_args()
    if args.use_example_file == True:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name


def first_part(lines):
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


def second_part(lines):
    most_calories_array = np.zeros(NUMBER_ELVES,dtype=int)
    current_calories = 0
    for line in lines:
        if line == '':
            most_calories = np.min(most_calories_array) # in order to have all maxima in this array, the minimum value in the array is the one that has to compete against the possible new maximum
            if(current_calories > most_calories):
                most_calories_array[np.argmin(most_calories_array)] = current_calories
            current_calories = 0
                
        else:
            current_calories += int(line)


    print("The three most carried calories combined add to", np.sum(most_calories_array))


def main(file_name):    
    with open(file_name) as file:
        lines = file.read().splitlines()
        lines += [""] # Be sure that there is an extra empty line at the end. This is just to make sure to check the maximum values in the upcoming loops of the functions

    first_part(lines)
    second_part(lines)



if __name__ == "__main__":
    main(parse_file_name())


