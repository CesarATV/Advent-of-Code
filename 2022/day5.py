import argparse

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day5.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day5_example.txt"


def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 5: Supply Stacks")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]



def solve_first_part(lines):
    stack_list = [ [] for _ in range(9) ]
    for line_idx, line in enumerate(lines):
        if(line[1] == '1'):
            break

        for list_idx in range(len(stack_list)):
            if((1+list_idx*4) < len(line)):
                if(line[1+list_idx*4] != ' '):
                    stack_list[list_idx].insert(0,line[1+list_idx*4])

    for line in lines[line_idx+2:]:
        _, n_pops, _, pop_origin, _, pop_destination = line.split(" ")
        n_pops = int(n_pops)
        pop_origin = int(pop_origin) - 1
        pop_destination = int(pop_destination) - 1
        
        for _ in range(n_pops):
            stack_list[pop_destination].append(stack_list[pop_origin].pop())
            
    top_items = ''
    for idx in range(len(stack_list)):
        if (len(stack_list[idx]) != 0):
            top_items += stack_list[idx][-1]
        else: # No items on the stack
            top_items += ' ' # the instructions do not specify whether should be left blank or with space (or if this case may ever happen)

    print("After the rearrangement procedure the items on top are:", top_items)


def solve_second_part(lines):
    stack_list = [ [] for _ in range(9) ]
    for line_idx, line in enumerate(lines):
        if(line[1] == '1'):
            break

        for list_idx in range(len(stack_list)):
            if (1+list_idx*4) < len(line):
                if(line[1+list_idx*4] != ' '):
                    stack_list[list_idx].insert(0,line[1+list_idx*4])

    for line in lines[line_idx+2:]:
        _, n_pops, _, pop_origin, _, pop_destination = line.split(" ")
        n_pops = int(n_pops)
        pop_origin = int(pop_origin) - 1
        pop_destination = int(pop_destination) - 1
        
        sub_stack = stack_list[pop_origin][-n_pops:]
        del stack_list[pop_origin][-n_pops:]
        stack_list[pop_destination] = stack_list[pop_destination] + (sub_stack)

            
    top_items = ''
    for idx in range(len(stack_list)):
        if len(stack_list[idx]) != 0:
            top_items += stack_list[idx][-1]
        else: # No items on the stack
            top_items += ' ' # the instructions do not specify whether should be left blank or with space (or if this case may ever happen)

    print("After the rearrangement procedure considering multiple crates moved at once, the items on top are:", top_items)

def main(file_name):    
    with open(file_name) as file:
        lines = file.read().splitlines()
    while lines[-1] == "": # remove last empty lines, if any. They do not add information and can cause confusion
        lines.pop()

    solve_first_part(lines)
    solve_second_part(lines)


if __name__ == "__main__":
    main(parse_file_name())


