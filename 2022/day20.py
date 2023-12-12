# NOTE: Python takes into account negatives as well as positives when using the modulo operator (it implements the flored modulo) e.g. -1 % 7 = -7

import argparse

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day20.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day20_example.txt"


BASE_DECRYPTING_NUMBER = 0 # although not explicitly stated, there has to be only one number with this value in the file
DECRYPTING_MOVEMENT_1 = 1000
DECRYPTING_MOVEMENT_2 = 2000
DECRYPTING_MOVEMENT_3 = 3000

ENCRYPTION_KEY = 811589153
N_MIXES = 10


def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 20: Grove Positioning System")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]


def solve_first_part(encrypted_file, unencrypted_line_indexes=None, print_result=True, extra_printing_string=""):
    encryption_length = len(encrypted_file)
    if unencrypted_line_indexes == None:
        unencrypted_line_indexes = list(range(encryption_length)) # stores the original indexes of the file
    encryption_movement_limit = encryption_length -1 # after this index position, the file wraps

    for encrypted_file_idx in range(encryption_length):
        idx_list_idx = unencrypted_line_indexes.index(encrypted_file_idx) # get the index of the element in the encrypted file that is being processed, so it can show its current index in the variable that stores all initial indexes
        suggested_movement = encrypted_file[encrypted_file_idx]
        if suggested_movement < 0: 
            # moves to the left
            movement = suggested_movement % - encryption_movement_limit 

            if (movement+idx_list_idx) <= 0:
                # wraps to the left, so the movement has to become positive
                movement = suggested_movement % encryption_movement_limit
                unencrypted_line_indexes = unencrypted_line_indexes[:idx_list_idx] + unencrypted_line_indexes[idx_list_idx+1:idx_list_idx+1+movement] + [unencrypted_line_indexes[idx_list_idx]] + unencrypted_line_indexes[idx_list_idx+movement+1:]
            else:
                unencrypted_line_indexes = unencrypted_line_indexes[:idx_list_idx+movement] + [unencrypted_line_indexes[idx_list_idx]] + unencrypted_line_indexes[idx_list_idx+movement:idx_list_idx] + unencrypted_line_indexes[idx_list_idx+1:]

        else:
            # moves to the right
            movement = suggested_movement % encryption_movement_limit 
            if (movement+idx_list_idx) > encryption_movement_limit:
                # wraps to the right, so the movement has to become negative
                movement = movement % -encryption_movement_limit
                unencrypted_line_indexes = unencrypted_line_indexes[:idx_list_idx+movement] + [unencrypted_line_indexes[idx_list_idx]] + unencrypted_line_indexes[idx_list_idx+movement:idx_list_idx] + unencrypted_line_indexes[idx_list_idx+1:]

            else:
                unencrypted_line_indexes = unencrypted_line_indexes[:idx_list_idx] + unencrypted_line_indexes[idx_list_idx+1:idx_list_idx+1+movement] + [unencrypted_line_indexes[idx_list_idx]] + unencrypted_line_indexes[idx_list_idx+movement+1:]


    if print_result == True:
        original_base_decrypting_number_index = encrypted_file.index(BASE_DECRYPTING_NUMBER)
        new_base_decrypting_number_index = unencrypted_line_indexes.index(original_base_decrypting_number_index)

        decrypting_movement_1 = (new_base_decrypting_number_index + DECRYPTING_MOVEMENT_1 % encryption_length) % encryption_length
        decrypting_movement_2 = (new_base_decrypting_number_index + DECRYPTING_MOVEMENT_2 % encryption_length) % encryption_length
        decrypting_movement_3 = (new_base_decrypting_number_index + DECRYPTING_MOVEMENT_3 % encryption_length) % encryption_length

        coordinate_part_1 = encrypted_file[unencrypted_line_indexes[decrypting_movement_1]]
        coordinate_part_2 = encrypted_file[unencrypted_line_indexes[decrypting_movement_2]]
        coordinate_part_3 = encrypted_file[unencrypted_line_indexes[decrypting_movement_3]]

        grove_coordinates = coordinate_part_1 + coordinate_part_2 + coordinate_part_3
        print("The " + extra_printing_string + "grove coordinates are", grove_coordinates)
    else:
        return unencrypted_line_indexes


def solve_second_part(encrypted_file):
    for idx in range(len(encrypted_file)):
        encrypted_file[idx] *= ENCRYPTION_KEY

    unencrypted_line_indexes = list(range(len(encrypted_file))) # stores the original indexes of the file

    for _ in range(N_MIXES-1):
        unencrypted_line_indexes = solve_first_part(encrypted_file, unencrypted_line_indexes, print_result=False)
    solve_first_part(encrypted_file, unencrypted_line_indexes, print_result=True, extra_printing_string="correct ")



def main(file_name):    
    with open(file_name) as file:
        lines = file.read().splitlines()
    while lines[-1] == "": # remove last empty lines, if any. They do not add information and can cause confusion
        lines.pop()

    encrypted_file = list(map(int,lines))
    solve_first_part(encrypted_file)
    solve_second_part(encrypted_file)


if __name__ == "__main__":
    main(parse_file_name())