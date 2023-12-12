import argparse
import numpy as np
import ast

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day13.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day13_example.txt"

DIVIDER_PACKAGE_BEGIN = [[2]]
DIVIDER_PACKAGE_END = [[6]]


def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 13: Distress Signal")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]


def looped_decision(left_value,right_value,current_index,n_correctly_ordered_pairs, is_package_ordered):
    is_left_a_list = type(left_value) is list
    is_right_a_list = type(right_value) is list
    if is_left_a_list == True and is_right_a_list == False:
        right_value = [right_value]
        is_right_a_list = True

    elif is_left_a_list == False and is_right_a_list == True:
        left_value = [left_value]
        is_left_a_list = True


    if is_left_a_list == True and is_right_a_list == True:
        n_left_values = len(left_value)
        n_right_values = len(right_value)
        if n_left_values == 0:
            if n_right_values == 0:
                continue_decision_loop = True
                return continue_decision_loop, n_correctly_ordered_pairs, is_package_ordered
            else:
                n_correctly_ordered_pairs += 1*current_index
                is_package_ordered = True
                continue_decision_loop = False
                return continue_decision_loop, n_correctly_ordered_pairs, is_package_ordered
        elif n_right_values == 0:
            is_package_ordered = False
            continue_decision_loop = False
            return continue_decision_loop, n_correctly_ordered_pairs, is_package_ordered

        continue_decision_loop = True
        idx = 0
        while continue_decision_loop == True:
            continue_decision_loop, n_correctly_ordered_pairs, is_package_ordered = looped_decision(left_value[idx],right_value[idx],current_index, n_correctly_ordered_pairs, is_package_ordered)
            if continue_decision_loop == True:
                n_left_values = len(left_value[idx+1:])
                n_right_values = len(right_value[idx+1:])
                if n_left_values == 0:
                    if n_right_values == 0:
                        continue_decision_loop = True
                        break
                    else:
                        is_package_ordered = True
                        n_correctly_ordered_pairs += 1*current_index
                        continue_decision_loop = False
                        break
                elif(n_right_values == 0):
                    continue_decision_loop = False
                    is_package_ordered = False
                    break

                idx += 1

    else:
        if left_value < right_value:
            is_package_ordered = True
            n_correctly_ordered_pairs += 1*current_index
            continue_decision_loop = False

        elif left_value > right_value:
            is_package_ordered = False
            continue_decision_loop = False
        else:
            continue_decision_loop = True

    return continue_decision_loop, n_correctly_ordered_pairs, is_package_ordered


def solve_first_part(lines):
    n_correctly_ordered_pairs = 0
    current_index = 0
    process_left_list = True
    for line in lines:

        if line == "":
            process_left_list = True

        elif process_left_list:
            left_list = ast.literal_eval(line) # used to ease parsing, it is not strictly necessary
            process_left_list = False

        else:
            right_list = ast.literal_eval(line) # used to ease parsing, it is not strictly necessary
            current_index += 1
            _, n_correctly_ordered_pairs, _ = looped_decision(left_list,right_list,current_index, n_correctly_ordered_pairs, None)



    print("There are", n_correctly_ordered_pairs, "ordered package pairs")


def solve_second_part(lines):
    lines_evaled = [ast.literal_eval(line) for line in lines if line != ""] # remove all blank spaces

    is_package_ordered = False
    lines_bigger_than_divider_begin = np.zeros(len(lines_evaled), dtype=bool)
    lines_bigger_than_divider_end = np.zeros(len(lines_evaled), dtype=bool)
    for line_idx, line in enumerate(lines_evaled):
        continue_decision_loop = True
        while continue_decision_loop == True:
            continue_decision_loop, _, is_package_ordered = looped_decision(DIVIDER_PACKAGE_BEGIN,line,0,0,is_package_ordered)
        lines_bigger_than_divider_begin[line_idx] = is_package_ordered # you can read as: Is begin smaller than X

        continue_decision_loop = True
        while continue_decision_loop == True:
            continue_decision_loop, _, is_package_ordered = looped_decision(DIVIDER_PACKAGE_END,line,0,0,is_package_ordered)
        lines_bigger_than_divider_end[line_idx] = is_package_ordered

    n_below_top_divider = np.sum(lines_bigger_than_divider_begin == False)
    _n_above_top_divider = np.sum(lines_bigger_than_divider_end)
    n_between_dividers = np.sum(lines_bigger_than_divider_begin != lines_bigger_than_divider_end)


    print("The decoder key is", (n_below_top_divider+1) * (n_below_top_divider+n_between_dividers+2) )



def main(file_name): 
    with open(file_name) as file:
        lines = file.read().splitlines()
    while lines[-1] == "": # remove last empty lines, if any. They do not add information and can cause confusion
        lines.pop()
    
    solve_first_part(lines)
    solve_second_part(lines)


if __name__ == "__main__":
    main(parse_file_name())


