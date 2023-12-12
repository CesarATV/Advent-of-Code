import argparse
import numpy as np

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day12.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day12_example.txt"


INITIAL_POSITION_CHAR = 'S'
TARGET_POSITION_CHAR = 'E'
MINIMUM_ELEVATION_CHAR = 'a'
MAXIMUM_ELEVATION_CHAR = 'z'


def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 12: Hill Climbing Algorithm")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]


def parse_puzzle_file(lines):
    n_rows = len(lines)
    n_cols = len(lines[0])
    climbing_grid = np.zeros([n_rows,n_cols],dtype=int)
    possible_starting_positions = []
    for row_idx, line in enumerate(lines):
        climbing_grid[row_idx,:] = [ord(character) for character in line]

        col_idxs = [pos for pos, character in enumerate(line) if character == MINIMUM_ELEVATION_CHAR]
        for col_idx in col_idxs:
            possible_starting_positions.append((row_idx, col_idx))

        col_idx = line.find(INITIAL_POSITION_CHAR)
        if col_idx != -1:
            starting_position = (row_idx, col_idx)
            climbing_grid[row_idx, col_idx] = ord(MINIMUM_ELEVATION_CHAR) # INITIAL_POSITION_CHAR has an elevation of MINIMUM_ELEVATION_CHAR. The fact that the cell is labeled as INITIAL_POSITION_CHAR does not give extra information once its position is stored

    return starting_position, possible_starting_positions, climbing_grid



def check_cell(climbing_grid, checked_paths, paths_to_check, cell_position, maximum_next_elevation, n_steps, necessary_n_steps_list):
    possible_step = climbing_grid[cell_position[0],cell_position[1]]

    if possible_step == ord(TARGET_POSITION_CHAR):
        possible_step = ord(MAXIMUM_ELEVATION_CHAR) # the elevation of TARGET_POSITION_CHAR corresponds to MAXIMUM_ELEVATION_CHAR
        if maximum_next_elevation >= possible_step:
            necessary_n_steps_list.append(n_steps)
            paths_to_check = [[]] # There is no need to keep checking paths. An empty list is left nested, so calling pop() from solve_first_part does not throw an error

    elif maximum_next_elevation >= possible_step:
        if cell_position not in checked_paths:
            checked_paths[cell_position] = n_steps
            paths_to_check.append(cell_position)


def check_neighbours(climbing_grid, checked_paths, paths_to_check, row_idx, col_idx, elevation, current_n_steps, n_rows, n_cols, necessary_n_steps_list):
    maximum_next_elevation = elevation+1
    n_steps_to_target = current_n_steps + 1

    # check up
    if row_idx != 0:
        cell_position = (row_idx-1, col_idx)
        check_cell(climbing_grid, checked_paths, paths_to_check, cell_position, maximum_next_elevation, n_steps_to_target, necessary_n_steps_list)
    
    # check down
    if row_idx != (n_rows-1):
        cell_position = (row_idx+1, col_idx)
        check_cell(climbing_grid, checked_paths, paths_to_check, cell_position, maximum_next_elevation, n_steps_to_target, necessary_n_steps_list)


    # check right
    if col_idx != (n_cols-1):
        cell_position = (row_idx, col_idx+1)
        check_cell(climbing_grid, checked_paths, paths_to_check, cell_position, maximum_next_elevation, n_steps_to_target, necessary_n_steps_list)

    # check left
    if col_idx != 0:
        cell_position = (row_idx, col_idx-1)
        check_cell(climbing_grid, checked_paths, paths_to_check, cell_position, maximum_next_elevation, n_steps_to_target, necessary_n_steps_list)



def solve_first_part(starting_position, climbing_grid, print_result=True):
    checked_paths = {} # dictionary of paths that have alreay been checked, storing the position as key and the number of steps as valu
    paths_to_check = [starting_position]
    necessary_n_steps_list = [] # it will hold just 1 value, but is declared as a list to facilitate solve_second_part and to avoid passing the variable by value, which would require many checks until it is assigned
    checked_paths[starting_position] = 0
    while len(paths_to_check) != 0:
        cell_position = paths_to_check[0]
        check_neighbours(climbing_grid, checked_paths, paths_to_check, cell_position[0], cell_position[1], climbing_grid[cell_position[0],cell_position[1]], checked_paths[cell_position], climbing_grid.shape[0], climbing_grid.shape[1], necessary_n_steps_list)

        paths_to_check.pop(0)

    if print_result == True:
        print("To reach '{}', it is necessary to do at least {} steps starting from '{}'".format(TARGET_POSITION_CHAR, necessary_n_steps_list[0], INITIAL_POSITION_CHAR))
    else:
        return necessary_n_steps_list


def solve_second_part(possible_starting_positions, climbing_grid):
    necessary_n_steps_list = []
    for starting_position in possible_starting_positions:
        necessary_n_steps_list += solve_first_part(starting_position, climbing_grid, print_result=False)
    
    print("To reach '{}', it is necessary to do at least {} steps from any position of elevation '{}'".format(TARGET_POSITION_CHAR, np.min(necessary_n_steps_list), MINIMUM_ELEVATION_CHAR))


def main(file_name):
    with open(file_name) as file:
        lines = file.read().splitlines()
    while lines[-1] == "": # remove last empty lines, if any. They do not add information and can cause confusion
        lines.pop()

    starting_position, possible_starting_positions, climbing_grid = parse_puzzle_file(lines)
    
    solve_first_part(starting_position, climbing_grid)
    solve_second_part(possible_starting_positions, climbing_grid)


if __name__ == "__main__":
    main(parse_file_name())