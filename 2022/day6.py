import argparse

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day6.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day6_example.txt"

N_UNIQUE_CHARACTERS_FOR_PACKAGE = 4
N_UNIQUE_CHARACTERS_FOR_MESSAGE = 14


def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 6: Tuning Trouble")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]


def check_if_all_characters_are_different(character_list):
    are_all_different = True
    for idx, character in enumerate(character_list[:-1]):
        for sub_idx in range(idx+1,len(character_list)):
            are_all_different = are_all_different and (character_list[sub_idx] != character)
        if are_all_different == False:
            break
    return are_all_different


def search_marker(file_contents, n_unique_characters):
    previous_characters = [ [] for _ in range(n_unique_characters) ]
    for idx in range(n_unique_characters):
        previous_characters[idx] = file_contents[idx]

    are_all_characters_different = check_if_all_characters_are_different(previous_characters)
    if are_all_characters_different == False:
        for current_character_position in range(len(file_contents)):
            previous_characters = previous_characters[1:] + [file_contents[current_character_position+n_unique_characters]]
            are_all_characters_different = check_if_all_characters_are_different(previous_characters)
            if are_all_characters_different == True:
                break
            
    if are_all_characters_different == True:
        current_character_position += n_unique_characters+1
        return current_character_position
    else:
        return None


def solve_first_part(file_contents):
    n_unique_characters = N_UNIQUE_CHARACTERS_FOR_PACKAGE
    marker_position = search_marker(file_contents, n_unique_characters)
    if marker_position != None:
        print("First start-of-packet marker detected at character", marker_position)
    else:
        print("No pattern detected when looking for start-of-packet marker. This option should never happen")


def solve_second_part(file_contents):
    n_unique_characters = N_UNIQUE_CHARACTERS_FOR_MESSAGE
    marker_position = search_marker(file_contents, n_unique_characters)
    if marker_position != None:
        print("First start-of-message marker detected at character", marker_position)
    else:
        print("No pattern detected when looking for start-of-message marker. This option should never happen")


def main(file_name):    
    with open(file_name) as file:
        file_contents = file.read()

    solve_first_part(file_contents)
    solve_second_part(file_contents)


if __name__ == "__main__":
    main(parse_file_name())


