'''
The code used for the second part of the puzzle is really slow when using non-example data, taking about half an hour to complete. This is despite using numpy notation trying to avoid loops as much as possible. It is likely that numpy is not the ideal tool to solve the puzzle. TODO: Improve this program

Maybe further improvements could include excluding too far away elves when checking if their positions are occupied, as there is a tendency that only one group in the map moves.
It has not been found yet a solution that can predict the final positions of the elves without computing every single movement of them. There was no completely cyclical behaviour found.
'''

import argparse
import numpy as np
import enum

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day23.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day23_example.txt"


ELF_CELL = "#"
N_ROUNDS = 10

class CardinalDirections(enum.IntEnum):
    NORTH = 0
    SOUTH = 1
    WEST = 2
    EAST = 3


def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 23: Unstable Diffusion")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]


def parse_puzzle_file(lines):
    elf_list = []
    for row_idx, line in enumerate(lines):
        for col_idx, cell_character in enumerate(line):
            if(cell_character == ELF_CELL):
                elf_list.append([row_idx,col_idx])

    elf_positions = np.array(elf_list)
    return elf_positions


def round_first_half(elf_positions, n_elves):
    '''
    Elves consider to move based on the eight positions adjacent to themselves
    '''
    positions_elves_able_to_move = elf_positions
    occupied_cells_mask = np.zeros(n_elves,dtype=bool)
    for extra_row in range(-1,2):
        for extra_col in range(-1,2):
            if extra_col == 0 and extra_row == 0:
                continue

            cell_occupied_uppermask = (positions_elves_able_to_move + [extra_row,extra_col])[:,None] == elf_positions # create a mask used to check if every row of positions_elves_able_to_move is the same as a position in elf_positions
            occupied_cells_mask = np.sum(np.sum(cell_occupied_uppermask,axis=2) == 2, axis=1, dtype=bool) + occupied_cells_mask # extract the rows that already contain an elf position. The condition == 2 checks that both the row and the column of a row of the position array fulfill the condition
    
    positions_elves_able_to_move = positions_elves_able_to_move[occupied_cells_mask]
    return positions_elves_able_to_move, occupied_cells_mask

    
def round_second_half(elf_positions, positions_elves_able_to_move, orientation_instructions, movement_direction_array):
    '''
    Elves move to their proposed new positions if only one of them wants to move to it
    '''
    n_movible_elves = positions_elves_able_to_move.shape[0]

    next_movement_array = np.zeros([n_movible_elves,2])
    uncompleted_movements_mask = np.ones(n_movible_elves,dtype=bool)

    not_allowed_planned_movements_mask = np.zeros(n_movible_elves,dtype=bool)
    unoccuppied_planned_movements_mask = np.ones(n_movible_elves,dtype=bool)
    
    next_considered_movement_array = next_movement_array.copy()
    positions_elves_able_to_move_considerated = positions_elves_able_to_move.copy() # not strictly necessary to copy, just done for clarity
    not_allowed_considered_movements_mask = not_allowed_planned_movements_mask.copy() # not strictly necessary to copy, just done for clarity
    unoccuppied_considered_movements_mask = unoccuppied_planned_movements_mask.copy() # not strictly necessary to copy, just done for clarity

    for next_orientation in orientation_instructions:
        for movement_direction in movement_direction_array[next_orientation.value]:
            next_considered_movement_array[unoccuppied_considered_movements_mask] = movement_direction

            considered_movements = positions_elves_able_to_move_considerated + next_considered_movement_array
            occuppied_considered_movements_uppermask = considered_movements[:,None] == elf_positions
            not_allowed_considered_movements_mask = np.sum(np.sum(occuppied_considered_movements_uppermask,axis=2) == 2, axis=1, dtype=bool) + not_allowed_considered_movements_mask
            unoccuppied_considered_movements_mask = np.logical_not(not_allowed_considered_movements_mask)
        

        next_considered_movement_array[not_allowed_considered_movements_mask] = [0,0]
        next_movement_array[uncompleted_movements_mask == True] = next_considered_movement_array
        uncompleted_movements_mask[uncompleted_movements_mask == True] = not_allowed_considered_movements_mask

        considered_movements = next_movement_array + positions_elves_able_to_move
        occuppied_planned_movements_uppermask = considered_movements[:,None] == considered_movements
        occuppied_planned_movements_diagonalized = np.sum(occuppied_planned_movements_uppermask,axis=2)
        occuppied_planned_movements_undiagonalized = occuppied_planned_movements_diagonalized[~np.eye(occuppied_planned_movements_diagonalized.shape[0],dtype=bool)].reshape(occuppied_planned_movements_diagonalized.shape[0],-1) # remove diagonal so in the comparison they are not compared with themselves
        not_allowed_planned_movements_mask = np.sum(occuppied_planned_movements_undiagonalized == 2, axis=1, dtype=bool) + not_allowed_planned_movements_mask
        unoccuppied_planned_movements_mask = np.logical_not(not_allowed_planned_movements_mask)

        n_elves_still_to_move = np.sum(uncompleted_movements_mask)
        if n_elves_still_to_move == 0:
            break

        next_considered_movement_array = next_movement_array[uncompleted_movements_mask == True]
        positions_elves_able_to_move_considerated = positions_elves_able_to_move[uncompleted_movements_mask == True]
        unoccuppied_considered_movements_mask = np.ones(n_elves_still_to_move, dtype=bool)
        not_allowed_considered_movements_mask = np.zeros(n_elves_still_to_move, dtype=bool)

    positions_elves_able_to_move[unoccuppied_planned_movements_mask] = considered_movements[unoccuppied_planned_movements_mask]

    


def solve_first_part(elf_positions):
    movement_direction_array = np.array([[[-1,-1],[-1,1],[-1,0]],[[1,-1],[1,1],[1,0]],[[-1,-1],[1,-1],[0,-1]],[[-1,1],[1,1],[0,1]]]) # ordered as north, south, west and east

    n_elves = elf_positions.shape[0]

    orientation_instructions = [CardinalDirections.NORTH, CardinalDirections.SOUTH, CardinalDirections.WEST, CardinalDirections.EAST]
    for round_n in range(N_ROUNDS):

        positions_elves_able_to_move, occupied_cells_mask = round_first_half(elf_positions, n_elves)
        if positions_elves_able_to_move.size == 0:
            print("Elves cannot move anymore. The movement process stopped in round", round_n)
            break
        
        # Second phase
        round_second_half(elf_positions, positions_elves_able_to_move, orientation_instructions, movement_direction_array)
        elf_positions = np.vstack([elf_positions[np.logical_not(occupied_cells_mask)], positions_elves_able_to_move])
        orientation_instructions = orientation_instructions[1:] + [orientation_instructions[0]]

    highest_occupied_row, highest_occupied_column = np.max(elf_positions,axis=0)
    lowest_occupied_row, lowest_occupied_column = np.min(elf_positions,axis=0)

    rectangle_height = np.abs(highest_occupied_row) + np.abs(lowest_occupied_row) + 1 
    rectangle_width = np.abs(highest_occupied_column) + np.abs(lowest_occupied_column) + 1
    n_empty_spaces = rectangle_height*rectangle_width - n_elves

    # elf_positions[np.lexsort((elf_positions[:,1],elf_positions[:,0]))]
    print("After", N_ROUNDS, "rounds, the smallest rectangle that contains all Elves has", n_empty_spaces, "emtpy spaces")
        


def solve_second_part(elf_positions):
    '''
    solve_second_part is almost identical to solve_first_part. The only difference is that it loops until all elves cannot move instead of a fixed number of rounds
    '''
    
    movement_direction_array = np.array([[[-1,-1],[-1,1],[-1,0]],[[1,-1],[1,1],[1,0]],[[-1,-1],[1,-1],[0,-1]],[[-1,1],[1,1],[0,1]]]) # ordered as north, south, west and east
    n_elves = elf_positions.shape[0]

    orientation_instructions = [CardinalDirections.NORTH, CardinalDirections.SOUTH, CardinalDirections.WEST, CardinalDirections.EAST]
    round_n = 0
    while(True):
        round_n += 1  # the number of rounds begins at 1

        positions_elves_able_to_move, occupied_cells_mask = round_first_half(elf_positions, n_elves)
        if positions_elves_able_to_move.size == 0:
            print("Elves cannot move anymore. The movement process stopped in round", round_n)
            break
        
        # Second phase
        round_second_half(elf_positions, positions_elves_able_to_move, orientation_instructions, movement_direction_array)
        elf_positions = np.vstack([elf_positions[np.logical_not(occupied_cells_mask)], positions_elves_able_to_move])
        orientation_instructions = orientation_instructions[1:] + [orientation_instructions[0]]

    highest_occupied_row, highest_occupied_column = np.max(elf_positions,axis=0)
    lowest_occupied_row, lowest_occupied_column = np.min(elf_positions,axis=0)

    rectangle_height = np.abs(highest_occupied_row) + np.abs(lowest_occupied_row) + 1 
    rectangle_width = np.abs(highest_occupied_column) + np.abs(lowest_occupied_column) + 1
    n_empty_spaces = rectangle_height*rectangle_width - n_elves

    print("After", round_n, "rounds, the smallest rectangle that contains all Elves has", n_empty_spaces, "emtpy spaces") # information not actually requested by the puzzle, but nice to have


def main(file_name):    
    with open(file_name) as file:
        lines = file.read().splitlines()
    while lines[-1] == "": # remove last empty lines, if any. They do not add information and can cause confusion
        lines.pop()

    elf_positions = parse_puzzle_file(lines)
    
    solve_first_part(elf_positions)
    solve_second_part(elf_positions)
    

if __name__ == "__main__":
    main(parse_file_name())


