import argparse
import copy
import numpy as np
import enum
from dataclasses import dataclass

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day11.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day11_example.txt"


MONKEY_TEXT_LENGTH = 7
N_ROUNDS = 20
N_ROUNDS_PART2 = 10000

class OperationType(enum.Enum):
    SUM_OPERATION = enum.auto()
    MULTIPLICATION_OPERATION = enum.auto()
    EXPONENTIATION_OPERATION = enum.auto()

@dataclass
class Monkey:
    items: list
    operation_type: OperationType
    operation_value: int
    test_dividend: int
    true_target: int
    false_target: int
    n_inspections: int = 0


def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 11: Monkey in the Middle")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]



def parse_puzzle_file(lines):
    monkey_list = []
    are_there_more_monkeys = len(lines[0:]) > MONKEY_TEXT_LENGTH
    line_index = 0
    while are_there_more_monkeys == True:
        split_item_line = lines[line_index + 1].replace(",","").split(" ")
        new_items = [[] for _ in range(len(split_item_line[4:]))]
        for item_idx in range(len(split_item_line[4:])):
            new_items[item_idx] = int(split_item_line[4 +item_idx ])

        if lines[line_index + 2].split(" ")[-1] == "old":
            new_operation_type = OperationType.EXPONENTIATION_OPERATION
            new_operation_value = 0
        else:
            if lines[line_index + 2].find("*") != -1:
                new_operation_type = OperationType.MULTIPLICATION_OPERATION
            else:
                new_operation_type = OperationType.SUM_OPERATION
            new_operation_value = int(lines[line_index + 2].split(" ")[-1])

        new_test_dividend = int(lines[line_index + 3].split(" ")[-1])

        new_true_target = int(lines[line_index + 4].split(" ")[-1])

        new_false_target = int(lines[line_index + 5].split(" ")[-1])

        monkey_list.append( Monkey(new_items, new_operation_type, new_operation_value, new_test_dividend, new_true_target, new_false_target) )

        are_there_more_monkeys = len(lines[line_index+MONKEY_TEXT_LENGTH-1:]) >= MONKEY_TEXT_LENGTH
        line_index += MONKEY_TEXT_LENGTH

    return monkey_list


def solve_first_part(monkey_list):
    n_monkeys = len(monkey_list)
    for _ in range(N_ROUNDS):
        for current_monkey_id in range(n_monkeys):
            
            n_items = len(monkey_list[current_monkey_id].items)
            for _ in range(n_items):
                item_worry = monkey_list[current_monkey_id].items.pop(0)
                
                if monkey_list[current_monkey_id].operation_type == OperationType.EXPONENTIATION_OPERATION:
                    item_worry *= item_worry
                elif monkey_list[current_monkey_id].operation_type == OperationType.MULTIPLICATION_OPERATION:
                    item_worry *=  monkey_list[current_monkey_id].operation_value
                else:
                    item_worry +=  monkey_list[current_monkey_id].operation_value
                    
                item_worry //= 3

                if (item_worry % monkey_list[current_monkey_id].test_dividend) == 0:
                    target_monkey = monkey_list[current_monkey_id].true_target
                else:
                    target_monkey = monkey_list[current_monkey_id].false_target

                monkey_list[target_monkey].items.append(item_worry)

            monkey_list[current_monkey_id].n_inspections += n_items


    n_inspections_list = [[] for _ in range(n_monkeys)]
    for idx, monkey in enumerate(monkey_list):
        n_inspections_list[idx] = monkey.n_inspections

    print("The monkey business level is", np.sort(n_inspections_list)[-1] * np.sort(n_inspections_list)[-2])
 

def solve_second_part(monkey_list):
    '''
    As the item_worry values are no longer divided by 3 in each iteration, and the number of rounds has increased to 10000, reusing the old code to solve the second part of this challenge is, although possible, absurdly inefficient. There are exponentations of always-increasing numbers, these create a risk of overflowing and do slow down the program too much (maybe days).

    The only important operation that alters the desired result (the number of times each monkey manipulated an item), is the operation that decides which monkey receives which item. This is just a module operation, which uses different but predefined (in the given text file) numbers. 
    The remainder of a number N divided by another D is the same remainder as the remainder of the remainder of N divided by D divided by D (i.e. N % D == (N % D) % D)), also when another number A is added to N (i.e. (N+A) % D == ((N%D)+A) % D)). Therefore, a number D that works with all given dividend numbers can be used to keep the item_worry (N in this case) values low, and still give the same result for this challenge. This D can be the multiplication between all given dividend numbers (e.g., if D = d1*d2, (N+A) % d1 == (N%D+A) % d1 and (N+A) % d2 == (N%D+A) % d2), as this is the common multiple of the dividends.

    Note: It was considered to eliminate the exponentation altogether, but the idea can not work, e.g in many cases (N*N-A) % D != (N-A) % D
    '''

    n_monkeys = len(monkey_list)
    common_dividend = 1
    for current_monkey_id in range(n_monkeys):
        n_items = len(monkey_list[current_monkey_id].items)
        for _ in range(n_items):
            common_dividend *= monkey_list[current_monkey_id].test_dividend


    for _ in range(N_ROUNDS_PART2):
        for current_monkey_id in range(n_monkeys):
            
            n_items = len(monkey_list[current_monkey_id].items)
            for _ in range(n_items):
                item_worry = monkey_list[current_monkey_id].items.pop(0)
                
                if monkey_list[current_monkey_id].operation_type == OperationType.EXPONENTIATION_OPERATION:
                    item_worry *= item_worry
                elif monkey_list[current_monkey_id].operation_type == OperationType.MULTIPLICATION_OPERATION:
                    item_worry *= monkey_list[current_monkey_id].operation_value
                else:
                    item_worry += monkey_list[current_monkey_id].operation_value

                if (item_worry % monkey_list[current_monkey_id].test_dividend) == 0:
                    target_monkey = monkey_list[current_monkey_id].true_target
                else:
                    target_monkey = monkey_list[current_monkey_id].false_target

                monkey_list[target_monkey].items.append(item_worry % common_dividend)

            monkey_list[current_monkey_id].n_inspections += n_items


    n_inspections_list = [[] for _ in range(n_monkeys)]
    for idx, monkey in enumerate(monkey_list):
        n_inspections_list[idx] = monkey.n_inspections

    print("Without constant division of worry levels, the monkey business level is", np.sort(n_inspections_list)[-1] * np.sort(n_inspections_list)[-2])
        

def main(file_name): 
    with open(file_name) as file:
        lines = file.read().splitlines()
    while lines[-1] == "": # remove last empty lines, if any. They do not add information and can cause confusion
        lines.pop()

    monkey_list = parse_puzzle_file(lines)
    solve_first_part(copy.deepcopy(monkey_list))
    solve_second_part(monkey_list)


if __name__ == "__main__":
    main(parse_file_name())