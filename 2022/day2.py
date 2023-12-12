import argparse

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day2.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day2_example.txt"


def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 2: Rock Paper Scissors")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]



def solve_first_part(lines):
    # X is rock, Y is paper, Z is scissors
    total_score = 0
    for line in lines:
        if line[0] == "A":
            if line[2] == "X":
                shape_score = 1
                total_score += 3 + shape_score
            elif line[2] == "Y":
                shape_score = 2
                total_score += 6 + shape_score
            elif line[2] == "Z":
                shape_score = 3
                total_score += 0 + shape_score
                
        elif line[0] == "B":
            if line[2] == "X":
                shape_score = 1
                total_score += 0 + shape_score
            elif line[2] == "Y":
                shape_score = 2
                total_score += 3 + shape_score
            elif line[2] == "Z":
                shape_score = 3
                total_score += 6 + shape_score

        elif line[0] == "C":
            if line[2] == "X":
                shape_score = 1
                total_score += 6 + shape_score
            elif line[2] == "Y":
                shape_score = 2
                total_score += 0 + shape_score
            elif line[2] == "Z":
                shape_score = 3
                total_score += 3 + shape_score

    print("The total score is", total_score, "according to the strategy guide")


def solve_second_part(lines):
    # X is rock, Y is paper, Z is scissors
    total_score = 0
    for line in lines:
        if line[0] == "A":
            if line[2] == "X":
                shape_score = 3
                total_score += 0 + shape_score
            elif line[2] == "Y":
                shape_score = 1
                total_score += 3 + shape_score
            elif line[2] == "Z":
                shape_score = 2
                total_score += 6 + shape_score
                
        elif line[0] == "B":
            if line[2] == "X":
                shape_score = 1
                total_score += 0 + shape_score
            elif line[2] == "Y":
                shape_score = 2
                total_score += 3 + shape_score
            elif line[2] == "Z":
                shape_score = 3
                total_score += 6 + shape_score

        elif line[0] == "C":
            if line[2] == "X":
                shape_score = 2
                total_score += 0 + shape_score
            elif line[2] == "Y":
                shape_score = 3
                total_score += 3 + shape_score
            elif line[2] == "Z":
                shape_score = 1
                total_score += 6 + shape_score

    print("Considering the Elf's instructions, the total score is", total_score, "according to the strategy guide")


def main(file_name):    
    with open(file_name) as file:
        lines = file.read().splitlines()
    while lines[-1] == "": # remove last empty lines, if any. They do not add information and can cause confusion
        lines.pop()

    solve_first_part(lines)
    solve_second_part(lines)


if __name__ == "__main__":
    main(parse_file_name())


