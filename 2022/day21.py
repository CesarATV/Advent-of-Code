'''
It was not explicitely stated, but the base numbers are not negative and are integers. This allows to use the string function isnumeric()

Also not explicitely stated, and very relevant for the second part: all yelled numbers (numbers that do not require math operations) are used only once by one individual monkey. This means that it is possible to find one of the numbers yelled by the root monkey in the same way than in the first part, as there is only one unknown number. Also, this means that the other missing number can be found just by reversing the operations that would normally give the second number to the root monkey.

The program could benefit from deleting the lines that have been processed, instead of just adding conditions to not check them twice. The program, however, finishes in a small amount of time
'''

import argparse
import sys

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day21.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day21_example.txt"


ROOT_MONKEY_NAME = "root"
NAME_CORRESPONDING_TO_YOU = "humn"


def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 21: Monkey Math")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]


def parse_puzzle_file(file_contents):
    stacked_lines = file_contents
    lines = stacked_lines.splitlines()
    while lines[-1] == "": # remove last empty lines, if any. They do not add information and can cause confusion
        lines.pop()
        stacked_lines = stacked_lines[:-1]

    stacked_lines_part2 = stacked_lines
    for line in lines:
        split_line = line.split(" ")
        if(len(split_line)==2): # lines that fulfill this condition are the ones that do not contain a math operation but numbers
            monkey_name = split_line[0][:-1]
            yelled_number = split_line[1]
            stacked_lines = stacked_lines.replace(monkey_name, yelled_number)

            if(monkey_name != NAME_CORRESPONDING_TO_YOU):
                yelled_number_part2 = split_line[1]
                stacked_lines_part2 = stacked_lines_part2.replace(monkey_name, yelled_number_part2)

    return stacked_lines, stacked_lines_part2


def monkey_math_operation(leftmost_number, rightmost_number, operation_type):
    if(operation_type == "*"):
        math_result = leftmost_number * rightmost_number
    elif(operation_type == "/"):
        math_result = leftmost_number // rightmost_number
    elif(operation_type == "+"):
        math_result = leftmost_number + rightmost_number
    elif(operation_type == "-"):
        math_result = leftmost_number - rightmost_number
    else:
        print("Wrong math operator received")
        sys.exit()

    return math_result



def solve_first_part(stacked_lines):
    loop_got_stuck = False # variable use to avoid infinite loops, something that should never happen 
    while loop_got_stuck == False:

        root_line = stacked_lines[stacked_lines.find(ROOT_MONKEY_NAME):].splitlines()[0].split(" ")
        if root_line[1].isnumeric() and root_line[3].isnumeric():
            break

        processed_lines = stacked_lines.splitlines()
        loop_got_stuck = True # will become false if the loop does not get stuck
        for line in processed_lines:
            split_line = line.split(" ")
            monkey_name = split_line[0][:-1]
            if len(split_line)>2 and (not monkey_name.isnumeric()):
                if split_line[1].isnumeric() and split_line[3].isnumeric():
                    
                    math_result = monkey_math_operation(int(split_line[1]), int(split_line[3]), split_line[2])
                    stacked_lines = stacked_lines.replace(monkey_name, str(math_result))
                    loop_got_stuck = False

    if loop_got_stuck == True:
        print("This should never happen: the program ended in an infinite loop")
    else:
        math_result = monkey_math_operation(int(root_line[1]), int(root_line[3]), root_line[2])
        print("The monkey named", ROOT_MONKEY_NAME,  "will yell", math_result)


def solve_second_part(stacked_lines):
    loop_got_stuck = False # in this case, the loop has to get stuck before leaving it
    while loop_got_stuck == False:
        processed_lines = stacked_lines.splitlines()
        loop_got_stuck = True
        for line in processed_lines:
            split_line = line.split(" ")
            monkey_name = split_line[0][:-1]
            if len(split_line)>2 and (not monkey_name.isnumeric()):
                if split_line[1].isnumeric() and split_line[3].isnumeric():
                    
                    math_result = monkey_math_operation(int(split_line[1]), int(split_line[3]), split_line[2])

                    if monkey_name != ROOT_MONKEY_NAME:
                        stacked_lines = stacked_lines.replace(monkey_name, str(math_result))
                    loop_got_stuck = False


    root_line = stacked_lines[stacked_lines.find(ROOT_MONKEY_NAME):].splitlines()[0].split(" ")
    if root_line[1].isnumeric() == True:
        upper_math_result = root_line[3]
        lower_monkey_name = root_line[1]
    elif root_line[3].isnumeric() == True:
        upper_math_result = root_line[3]
        lower_monkey_name = root_line[1]
    else:
        print("This should never happen: the root monkey did not find one number")
        sys.exit()


    loop_got_stuck = False
    base_monkey_value_found = False
    while loop_got_stuck == False and base_monkey_value_found == False:

        processed_lines = stacked_lines.splitlines()
        loop_got_stuck = True
        for line in processed_lines:
            split_line = line.split(" ")
            monkey_name = split_line[0][:-1]

            if lower_monkey_name != monkey_name:
                continue

            if split_line[1].isnumeric():
                lower_monkey_name = split_line[3]
                complementary_math_result = split_line[1]
                lower_monkey_on_left_side = False
            elif split_line[3].isnumeric():
                lower_monkey_name = split_line[1]
                complementary_math_result = split_line[3]
                lower_monkey_on_left_side = True


            if split_line[2] == "*":
                math_result = int(upper_math_result) // int(complementary_math_result)
            elif split_line[2] == "/":
                math_result = int(upper_math_result) * int(complementary_math_result)
            elif split_line[2] == "-":
                if lower_monkey_on_left_side == False:
                    math_result = int(complementary_math_result) - int(upper_math_result)
                else:
                    math_result = int(upper_math_result) + int(complementary_math_result)
            elif split_line[2] == "+":
                math_result = int(upper_math_result) - int(complementary_math_result)
            else:
                print("Wrong math operator received. This line should have never been executed")
                sys.exit()

            stacked_lines = stacked_lines.replace(monkey_name, str(math_result))
            upper_math_result = str(math_result)

            loop_got_stuck = False
            if lower_monkey_name == NAME_CORRESPONDING_TO_YOU:
                base_monkey_value_found = True
                break
            
    if loop_got_stuck == True:
        print("This should never happen: the program ended in an infinite loop")
    else:
        print("The number to be yelled is", math_result)


def main(file_name):    
    with open(file_name) as file:
        file_contents = file.read()

    stacked_lines, stacked_lines_part2 = parse_puzzle_file(file_contents)

    solve_first_part(stacked_lines)
    solve_second_part(stacked_lines_part2)


if __name__ == "__main__":
    main(parse_file_name())