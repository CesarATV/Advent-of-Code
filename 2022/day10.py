import argparse
import numpy as np

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day10.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day10_example.txt"

CYCLES_OF_INTEREST = (20,60,100,140,180,220)

HEIGHT_CRT_SCREEN = 6
WIDTH_CRT_SCREEN = 40
CYCLES_OF_INTEREST_PART2 = (40,80,120,160,200,240)

# these first two characters are the default suggested by the input of the day. They are commente out as the rendered output is easier to read if using others
# MATCH_PRINTING_CHAR = "#" # default
# EMPTY_PRINTING_CHAR = "." # default
MATCH_PRINTING_CHAR = "█"
EMPTY_PRINTING_CHAR = " "


def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 10: Cathode-Ray Tube")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]



def increase_and_check_cycle(cycle_count, register_X, signal_strength, cycles_of_interest):
    cycle_count += 1
    if cycle_count in cycles_of_interest:
        signal_strength += cycle_count*register_X
    return cycle_count, signal_strength


def solve_first_part(lines):
    register_X = 1
    signal_strength = 0
    cycle_count = 0
    for line in lines:
        line_split = line.split(" ")
        instruction = line_split[0]
        if instruction == "addx":
            value_V = int(line_split[1])
            cycle_count, signal_strength = increase_and_check_cycle(cycle_count, register_X, signal_strength, CYCLES_OF_INTEREST)
            cycle_count, signal_strength = increase_and_check_cycle(cycle_count, register_X, signal_strength, CYCLES_OF_INTEREST)
            register_X += value_V

        elif instruction == "noop":
            cycle_count, signal_strength = increase_and_check_cycle(cycle_count, register_X, signal_strength, CYCLES_OF_INTEREST)
        
        
    print("The total signal strength is", signal_strength)
 


class CycleCountter:
    def __init__(self, cycles_of_interest):
        self.screen_row = 0
        self.screen_col = 0
        self.cycle_count = 0
        self.screen_CRT = np.zeros([HEIGHT_CRT_SCREEN,WIDTH_CRT_SCREEN],dtype="str")
        self.cycles_of_interest = cycles_of_interest

    def increase_and_check_cycle(self, register_X):
        if self.screen_col == register_X or (self.screen_col+1) == register_X or (self.screen_col-1) == register_X:
            self.screen_CRT[self.screen_row, self.screen_col] = MATCH_PRINTING_CHAR
        else:
            self.screen_CRT[self.screen_row, self.screen_col] = EMPTY_PRINTING_CHAR

        self.cycle_count += 1
        if self.cycle_count in self.cycles_of_interest:
            self.screen_row += 1
            self.screen_col = 0
        else:
            self.screen_col += 1


def solve_second_part(lines):
    register_X = 1
    cycle_counter = CycleCountter(CYCLES_OF_INTEREST_PART2)
    for line in lines:
        line_split = line.split(" ")
        instruction = line_split[0]
        if instruction == "addx":
            value_V = int(line_split[1])
            cycle_counter.increase_and_check_cycle(register_X)
            cycle_counter.increase_and_check_cycle(register_X)
            register_X += value_V

        elif instruction == "noop":
            cycle_counter.increase_and_check_cycle(register_X)
        

    for height_idx in range(HEIGHT_CRT_SCREEN):
        for width_idx in range(WIDTH_CRT_SCREEN):
            print(cycle_counter.screen_CRT[height_idx,width_idx], end = '')
        print("")
        

def main(file_name): 
    with open(file_name) as file:
        lines = file.read().splitlines()
    while lines[-1] == "": # remove last empty lines, if any. They do not add information and can cause confusion
        lines.pop()

    solve_first_part(lines)
    solve_second_part(lines)


if __name__ == "__main__":
    main(parse_file_name())