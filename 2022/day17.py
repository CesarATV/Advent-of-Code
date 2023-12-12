'''
The instructions did not specify exactly how the height of the tower of rocks (the puzzle answer) is defined. It has been found that this is simply the height of the highest stacked rock (so it does not matter if there are empty spots within that tower)

The first part simulates the movement of each rock, declaring that movement possible if it does not interfere with any rock (the variable blocked_positions keeps track of this). In retrospective, blocked_positions should have been a set instead of a numpy array


For the second part, the new number of falling rocks would require an absurd long amount of time to estimate the heigh of the resulting tower by simulating every rock movement. It would also require a high amount of memory containing all the fallen blocks. Part of this memory could be freed when all the width cells of the cave at a particular height are blocked, allowing to make that new height the new floor of the cave. However, adding a check to verify when these cells are blocked would also slow the program more

As the movements of the rock follow a pattern, and the order in which the rocks come from the ceiling are sequential, it can be assumed that at some point part of the structure of the tower will be repeated. If this pattern is found, it is possible to calculate what would be the height of the tower over any desired amount of falling rocks

After a number of rocks has fallen, the implemented program begins to look for a pattern by storing the position of all the rocks when a specific jet instruction (which determines rock movements) happens. The program will try to find those positions of the rock (considering a higher height) when that same jet instruction is repeated, hoping to find a match

TODO find if there is a number of rocks from which to start to look for a pattern, although seems to be random at first, there has to be a minimum rock number. Currently, the implemented program choses an arbitrary high number function of the times the jet pattern has been repeated

TODO Another improvement that the code could have would be to describe the rock shapes in terms of occupied coordinates in a boolean rock array, and then extract the relevant dimensions of that rock (the corners) with an automatized function. As it is right now, if more shapes were to be added, they would require to hardcode their dimensions in multiple places, instead of in a simple array 
'''

import argparse
import numpy as np
import enum

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day17.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day17_example.txt"


CAVE_WIDENESS = 7
FLOOR_ORIGINAL_HEIGHT = 4
BEGINNING_WIDENESS = 2 # with respect to bottom edge
BEGINNING_HEIGHT = 3


N_FALLING_ROCKS = 2022
N_FALLING_ROCKS_PART2 = 1000000000000
ARBITRARY_HIGH_NUMBER_TO_BEGIN_TO_LOOK_FOR_A_PATTERN = 200


def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 17: Pyroclastic Flow")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]


class RockShape(enum.Enum):
    HORIZONTAL_LINE = 0
    CROSS = 1
    LEFT_L = 2
    VERTICAL_LINE = 3
    SQUARE = 4
    N_SHAPES = 5
    

class FallingRock():
    def __init__(self, jet_pattern):
        self.jet_pattern = jet_pattern
        self.pattern_length = len(jet_pattern)

    def check_rock_blockedness(self, combinations_in_conflict):
        movement_is_possible = True
        for position in combinations_in_conflict:
            if position in self.blocked_positions:
                movement_is_possible = False
                return movement_is_possible
  
        return movement_is_possible

    def simulate_falling_rock(self, current_top_rock_height, jet_pattern_idx, blocked_positions, independent_jet_pattern_idx=0, unlooped_jet_pattern_idx=0):
        self.blocked_positions = blocked_positions
        self.prepare_falling_rock(current_top_rock_height)
        
        has_rock_stacked = False
        while has_rock_stacked == False:
            jet = self.jet_pattern[jet_pattern_idx]
            unlooped_jet_pattern_idx += 1
            independent_jet_pattern_idx += 1
            jet_pattern_idx += 1
            if(jet_pattern_idx == self.pattern_length):
                jet_pattern_idx = 0

            if jet == ">":
                self.move_to_the_right()
            else:
                self.move_to_the_left()

            has_rock_stacked = self.move_down()

        if self.topmost_point > current_top_rock_height:
            current_top_rock_height = self.topmost_point
        return current_top_rock_height, jet_pattern_idx, self.blocked_positions, independent_jet_pattern_idx, unlooped_jet_pattern_idx



class HorizontalLineRock(FallingRock):
    def __init__(self, jet_pattern):
        super().__init__(jet_pattern)

    def prepare_falling_rock(self, top_rock_height):
        self.leftmost_point = BEGINNING_WIDENESS
        self.lowmost_point = top_rock_height + BEGINNING_HEIGHT + 1
        self.rightmost_point = self.leftmost_point + 3

    def move_to_the_right(self):
        possible_new_rightmost_point = self.rightmost_point + 1 
        if possible_new_rightmost_point < CAVE_WIDENESS:
            rightmost_combinations = [(possible_new_rightmost_point, self.lowmost_point)] # right of horizontal line
            movement_is_possible = self.check_rock_blockedness(rightmost_combinations)
            if movement_is_possible == True:
                self.rightmost_point = possible_new_rightmost_point
                self.leftmost_point += 1

    def move_to_the_left(self):
        possible_new_leftmost_point = self.leftmost_point - 1 
        if possible_new_leftmost_point >= 0:
            leftmost_combinations = [(possible_new_leftmost_point, self.lowmost_point)] # left of horizontal line
            movement_is_possible = self.check_rock_blockedness(leftmost_combinations) 
            if movement_is_possible == True:
                self.leftmost_point = possible_new_leftmost_point
                self.rightmost_point -= 1

    def move_down(self):
        possible_new_lowmost_point = self.lowmost_point - 1
        lowermost_combinations = [(self.leftmost_point, possible_new_lowmost_point), (self.leftmost_point+1, possible_new_lowmost_point),(self.rightmost_point-1, possible_new_lowmost_point), (self.rightmost_point, possible_new_lowmost_point)]
        movement_is_possible = self.check_rock_blockedness(lowermost_combinations)        
        if movement_is_possible == True:
            self.lowmost_point = possible_new_lowmost_point
        else:
            self.final_positions = [(self.leftmost_point,self.lowmost_point),(self.leftmost_point+1,self.lowmost_point),(self.rightmost_point-1,self.lowmost_point),(self.rightmost_point,self.lowmost_point)]
            for a_final_position in self.final_positions:
                self.blocked_positions.add(a_final_position)

            self.topmost_point = self.lowmost_point

        return not movement_is_possible


class CrossRock(FallingRock):
    def __init__(self, jet_pattern):
        super().__init__(jet_pattern)

    def prepare_falling_rock(self, top_rock_height):
        self.leftmost_point = BEGINNING_WIDENESS
        self.lowmost_point = top_rock_height + BEGINNING_HEIGHT + 1
        self.rightmost_point = self.leftmost_point + 2
        
    def move_to_the_right(self):
        possible_new_rightmost_point = self.rightmost_point + 1 
        if possible_new_rightmost_point < CAVE_WIDENESS:
            rightmost_combinations = [(possible_new_rightmost_point,self.lowmost_point+1),(self.rightmost_point,self.lowmost_point),(self.rightmost_point,self.lowmost_point+2)] # center-right, bottom, top of cross
            movement_is_possible = self.check_rock_blockedness(rightmost_combinations)
            if movement_is_possible == True:
                self.rightmost_point = possible_new_rightmost_point
                self.leftmost_point += 1

    def move_to_the_left(self):
        possible_new_leftmost_point = self.leftmost_point - 1 
        if possible_new_leftmost_point >= 0:
            leftmost_combinations = [(possible_new_leftmost_point,self.lowmost_point+1),(self.leftmost_point,self.lowmost_point),(self.leftmost_point,self.lowmost_point+2)] # center-right, bottom and top of cross
            movement_is_possible = self.check_rock_blockedness(leftmost_combinations)
            if movement_is_possible == True:
                self.leftmost_point = possible_new_leftmost_point
                self.rightmost_point -= 1

    def move_down(self):
        possible_new_lowmost_point = self.lowmost_point - 1
        lowermost_combinations = [(self.rightmost_point-1, possible_new_lowmost_point), (self.rightmost_point, self.lowmost_point), (self.leftmost_point, self.lowmost_point)] # bottom, center-right and center-left of cross
        movement_is_possible = self.check_rock_blockedness(lowermost_combinations)     
        if movement_is_possible == True:
            self.lowmost_point = possible_new_lowmost_point
        else:
            self.final_positions = [(self.leftmost_point+1,self.lowmost_point),(self.leftmost_point,self.lowmost_point+1),(self.rightmost_point-1,self.lowmost_point+1),(self.rightmost_point,self.lowmost_point+1),(self.leftmost_point+1,self.lowmost_point+2)]
            for a_final_position in self.final_positions:
                self.blocked_positions.add(a_final_position)

            self.topmost_point = self.lowmost_point+2
        
        return not movement_is_possible


class LeftLRock(FallingRock):
    def __init__(self, jet_pattern):
        super().__init__(jet_pattern)

    def prepare_falling_rock(self, top_rock_height):
        self.leftmost_point = BEGINNING_WIDENESS
        self.lowmost_point = top_rock_height + BEGINNING_HEIGHT + 1
        self.rightmost_point = self.leftmost_point + 2

    def move_to_the_right(self):
        possible_new_rightmost_point = self.rightmost_point + 1 
        if possible_new_rightmost_point < CAVE_WIDENESS:
            rightmost_combinations = [(possible_new_rightmost_point,self.lowmost_point),(possible_new_rightmost_point,self.lowmost_point+1),(possible_new_rightmost_point,self.lowmost_point+2)] # lower_right, center_right and top_right of left-L
            movement_is_possible = self.check_rock_blockedness(rightmost_combinations)
            if movement_is_possible == True:
                self.rightmost_point = possible_new_rightmost_point
                self.leftmost_point += 1

    def move_to_the_left(self):
        possible_new_leftmost_point = self.leftmost_point - 1 
        if possible_new_leftmost_point >= 0:
            leftmost_combinations = [(possible_new_leftmost_point,self.lowmost_point)] # lower left of left-L
            movement_is_possible = self.check_rock_blockedness(leftmost_combinations) 
            if(movement_is_possible == True):
                self.leftmost_point = possible_new_leftmost_point
                self.rightmost_point -= 1

    def move_down(self):
        possible_new_lowmost_point = self.lowmost_point - 1
        lowermost_combinations = [(self.leftmost_point, possible_new_lowmost_point), (self.leftmost_point+1, possible_new_lowmost_point), (self.rightmost_point, possible_new_lowmost_point)] # left, center and lower_right of left-L
        movement_is_possible = self.check_rock_blockedness(lowermost_combinations)        
        if movement_is_possible == True:
            self.lowmost_point = possible_new_lowmost_point
        else:
            self.final_positions = [(self.leftmost_point,self.lowmost_point),(self.leftmost_point+1,self.lowmost_point),(self.rightmost_point,self.lowmost_point),(self.rightmost_point,self.lowmost_point+1),(self.rightmost_point,self.lowmost_point+2)]
            for a_final_position in self.final_positions:
                self.blocked_positions.add(a_final_position)

            self.topmost_point = self.lowmost_point + 2
        
        return not movement_is_possible


class VerticalLineRock(FallingRock):
    def __init__(self, jet_pattern):
        super().__init__(jet_pattern)

    def prepare_falling_rock(self, top_rock_height):
        self.leftmost_point = BEGINNING_WIDENESS
        self.lowmost_point = top_rock_height + BEGINNING_HEIGHT + 1
        self.rightmost_point = self.leftmost_point

    def move_to_the_right(self):
        possible_new_rightmost_point = self.rightmost_point + 1 
        if possible_new_rightmost_point < CAVE_WIDENESS:
            rightmost_combinations = [(possible_new_rightmost_point,self.lowmost_point),(possible_new_rightmost_point,self.lowmost_point+1),(possible_new_rightmost_point,self.lowmost_point+2),(possible_new_rightmost_point,self.lowmost_point+3)] # top, centers and bottom of vertical line
            movement_is_possible = self.check_rock_blockedness(rightmost_combinations)
            if movement_is_possible == True:
                self.rightmost_point = possible_new_rightmost_point
                self.leftmost_point += 1

    def move_to_the_left(self):
        possible_new_leftmost_point = self.leftmost_point - 1 
        if possible_new_leftmost_point >= 0:
            leftmost_combinations = [(possible_new_leftmost_point,self.lowmost_point),(possible_new_leftmost_point,self.lowmost_point+1),(possible_new_leftmost_point,self.lowmost_point+2),(possible_new_leftmost_point,self.lowmost_point+3)] # top, centers and bottom of vertical line
            movement_is_possible = self.check_rock_blockedness( leftmost_combinations) 
            if movement_is_possible == True:
                self.leftmost_point = possible_new_leftmost_point
                self.rightmost_point -= 1

    def move_down(self):
        possible_new_lowmost_point = self.lowmost_point - 1
        lowermost_combinations = [(self.leftmost_point, possible_new_lowmost_point)] # bottom of vertical line
        movement_is_possible = self.check_rock_blockedness(lowermost_combinations)        
        if movement_is_possible == True:
            self.lowmost_point = possible_new_lowmost_point
        else:
            self.final_positions = [(self.leftmost_point,self.lowmost_point),(self.leftmost_point,self.lowmost_point+1),(self.leftmost_point,self.lowmost_point+2),(self.leftmost_point,self.lowmost_point+3)]
            for a_final_position in self.final_positions:
                self.blocked_positions.add(a_final_position)

            self.topmost_point = self.lowmost_point + 3
        
        return not movement_is_possible


class SquareRock(FallingRock):
    def __init__(self, jet_pattern):
        super().__init__(jet_pattern)

    def prepare_falling_rock(self, top_rock_height):
        self.leftmost_point = BEGINNING_WIDENESS
        self.lowmost_point = top_rock_height + BEGINNING_HEIGHT + 1
        self.rightmost_point = self.leftmost_point + 1

    def move_to_the_right(self):
        possible_new_rightmost_point = self.rightmost_point + 1 
        if possible_new_rightmost_point < CAVE_WIDENESS:
            rightmost_combinations = [(possible_new_rightmost_point,self.lowmost_point),(possible_new_rightmost_point,self.lowmost_point+1)] # bottom-right and top-right of square
            movement_is_possible = self.check_rock_blockedness(rightmost_combinations)
            if movement_is_possible == True:
                self.rightmost_point = possible_new_rightmost_point
                self.leftmost_point += 1

    def move_to_the_left(self):
        possible_new_leftmost_point = self.leftmost_point - 1 
        if possible_new_leftmost_point >= 0:
            leftmost_combinations = [(possible_new_leftmost_point,self.lowmost_point),(possible_new_leftmost_point,self.lowmost_point+1)] # bottom-left and top-left of square
            movement_is_possible = self.check_rock_blockedness(leftmost_combinations) 
            if movement_is_possible == True:
                self.leftmost_point = possible_new_leftmost_point
                self.rightmost_point -= 1

    def move_down(self):
        possible_new_lowmost_point = self.lowmost_point - 1
        lowermost_combinations = [(self.leftmost_point, possible_new_lowmost_point),(self.rightmost_point, possible_new_lowmost_point)] # bottom-left and bottom-right of square
        movement_is_possible = self.check_rock_blockedness(lowermost_combinations)        
        if movement_is_possible == True:
            self.lowmost_point = possible_new_lowmost_point
        else:
            self.final_positions = [(self.leftmost_point,self.lowmost_point),(self.leftmost_point,self.lowmost_point+1),(self.rightmost_point,self.lowmost_point),(self.rightmost_point,self.lowmost_point+1)]
            for a_final_position in self.final_positions:
                self.blocked_positions.add(a_final_position)

            self.topmost_point = self.lowmost_point + 1

        return not movement_is_possible



def solve_first_part(jet_pattern, print_result=True):
    blocked_positions = set( (floor_width, -1) for floor_width in range(CAVE_WIDENESS) ) # block the bottom of the cave

    horizontal_line_rock = HorizontalLineRock(jet_pattern)
    cross_rock = CrossRock(jet_pattern)
    left_L_rock = LeftLRock(jet_pattern)
    vertical_line_rock = VerticalLineRock(jet_pattern)
    square_rock = SquareRock(jet_pattern)

    jet_pattern_idx = 0
    top_rock_height = -1
    for rock_idx in range(N_FALLING_ROCKS):
        rock_shape = RockShape(rock_idx % RockShape.N_SHAPES.value)
    
        if rock_shape == RockShape.HORIZONTAL_LINE:
            top_rock_height, jet_pattern_idx, blocked_positions, _, _ = horizontal_line_rock.simulate_falling_rock(top_rock_height, jet_pattern_idx, blocked_positions)

        elif rock_shape == RockShape.CROSS:
            top_rock_height, jet_pattern_idx, blocked_positions, _, _  = cross_rock.simulate_falling_rock(top_rock_height, jet_pattern_idx, blocked_positions)

        elif rock_shape == RockShape.LEFT_L:
            top_rock_height, jet_pattern_idx, blocked_positions, _, _  = left_L_rock.simulate_falling_rock(top_rock_height, jet_pattern_idx, blocked_positions)

        elif rock_shape == RockShape.VERTICAL_LINE:
            top_rock_height, jet_pattern_idx, blocked_positions, _, _  = vertical_line_rock.simulate_falling_rock(top_rock_height, jet_pattern_idx, blocked_positions)

        elif rock_shape == RockShape.SQUARE:
            top_rock_height, jet_pattern_idx, blocked_positions, _, _  = square_rock.simulate_falling_rock(top_rock_height, jet_pattern_idx, blocked_positions)
    
    if print_result:
        total_tower_height = top_rock_height+1
        print("After", N_FALLING_ROCKS, "falling rocks the tower will be", total_tower_height, "units tall")
    return blocked_positions # variable returned only for data visualization


def solve_second_part(jet_pattern):
    blocked_positions = set( (floor_width, -1) for floor_width in range(CAVE_WIDENESS) ) # block the bottom of the cave

    horizontal_line_rock = HorizontalLineRock(jet_pattern)
    cross_rock = CrossRock(jet_pattern)
    left_L_rock = LeftLRock(jet_pattern)
    vertical_line_rock = VerticalLineRock(jet_pattern)
    square_rock = SquareRock(jet_pattern)

    for pass_idx in range(2): # the first pass to find the pattern, the second to check the extra missing heights (the ones at the beginning, before the pattern began)
        if pass_idx == 0:
            maximum_number_falling_rocks = N_FALLING_ROCKS_PART2
        else:
            maximum_number_falling_rocks = n_second_pass_rocks
            blocked_positions = set( (floor_width, -1) for floor_width in range(CAVE_WIDENESS) ) # block the bottom of the cave
        rock_reference_taken = False

        # jet_pattern_idx loops at the size of jet_pattern, to keep indexing it. independent_jet_pattern_idx loops only when all rock types have been processed. unlooped_jet_pattern_idx does not loop at all
        unlooped_jet_pattern_idx = 0 
        independent_jet_pattern_idx = 0
        jet_pattern_idx = 0
        reference_independent_jet_pattern_idx = None # a reference will be taken further in the program, overwritting this value

        top_rock_height = -1
        for rock_idx in range(maximum_number_falling_rocks):
            rock_shape = RockShape(rock_idx % RockShape.N_SHAPES.value)
        
            if rock_shape == RockShape.HORIZONTAL_LINE:
                top_rock_height, jet_pattern_idx, blocked_positions, unlooped_jet_pattern_idx, independent_jet_pattern_idx = horizontal_line_rock.simulate_falling_rock(top_rock_height, jet_pattern_idx, blocked_positions, unlooped_jet_pattern_idx, independent_jet_pattern_idx)

            elif rock_shape == RockShape.CROSS:
                top_rock_height, jet_pattern_idx, blocked_positions, unlooped_jet_pattern_idx, independent_jet_pattern_idx = cross_rock.simulate_falling_rock(top_rock_height, jet_pattern_idx, blocked_positions, unlooped_jet_pattern_idx, independent_jet_pattern_idx)

            elif rock_shape == RockShape.LEFT_L:
                top_rock_height, jet_pattern_idx, blocked_positions, unlooped_jet_pattern_idx, independent_jet_pattern_idx = left_L_rock.simulate_falling_rock(top_rock_height, jet_pattern_idx, blocked_positions, unlooped_jet_pattern_idx, independent_jet_pattern_idx)

            elif rock_shape == RockShape.VERTICAL_LINE:
                top_rock_height, jet_pattern_idx, blocked_positions, unlooped_jet_pattern_idx, independent_jet_pattern_idx = vertical_line_rock.simulate_falling_rock(top_rock_height, jet_pattern_idx, blocked_positions, unlooped_jet_pattern_idx, independent_jet_pattern_idx)

            elif rock_shape == RockShape.SQUARE:
                top_rock_height, jet_pattern_idx, blocked_positions, unlooped_jet_pattern_idx, independent_jet_pattern_idx = square_rock.simulate_falling_rock(top_rock_height, jet_pattern_idx, blocked_positions, unlooped_jet_pattern_idx, independent_jet_pattern_idx)


                if rock_reference_taken == False and unlooped_jet_pattern_idx > len(jet_pattern) and rock_idx > ARBITRARY_HIGH_NUMBER_TO_BEGIN_TO_LOOK_FOR_A_PATTERN :
                    # take a reference at the moment of time in which, hopefully, the falling rocks began to loop
                    reference_rock_list = list([np.array(horizontal_line_rock.final_positions), np.array(cross_rock.final_positions), np.array(left_L_rock.final_positions), np.array(vertical_line_rock.final_positions), np.array(square_rock.final_positions)])
                    for idx in range(len(reference_rock_list)):
                        reference_rock_list[idx][:,1] -= top_rock_height
                    reference_independent_jet_pattern_idx = independent_jet_pattern_idx
                    reference_rock_idx = rock_idx
                    reference_top_rock_height = top_rock_height
                    rock_reference_taken = True

                elif reference_independent_jet_pattern_idx == independent_jet_pattern_idx:
                    # compare to the previous reference of rock positions to check if the falling rocks have looped. To avoid comparing it every time, it is done only when the jet pattern is in the same position as it was when the reference was taken
                    rock_to_compare_list = list([np.array(horizontal_line_rock.final_positions), np.array(cross_rock.final_positions), np.array(left_L_rock.final_positions), np.array(vertical_line_rock.final_positions), np.array(square_rock.final_positions)])
                    for idx in range(len(reference_rock_list)):
                        rock_to_compare_list[idx][:,1] -= top_rock_height
                        
                    all_rocks_are_repeated = True
                    for reference_rock, rock_to_compare in zip(reference_rock_list, rock_to_compare_list):
                        if not np.all(reference_rock == rock_to_compare):
                            all_rocks_are_repeated = False
                            break

                    if all_rocks_are_repeated == True:
                        repeated_rock_patterns_height = top_rock_height - reference_top_rock_height
                        n_rocks_between_repeated_rock_patterns = rock_idx - reference_rock_idx

                        n_repeated_rock_patterns = int(N_FALLING_ROCKS_PART2 / n_rocks_between_repeated_rock_patterns)
                        n_second_pass_rocks = N_FALLING_ROCKS_PART2 - n_repeated_rock_patterns*n_rocks_between_repeated_rock_patterns

                        break

                independent_jet_pattern_idx = 0

    total_tower_height = n_repeated_rock_patterns * repeated_rock_patterns_height + top_rock_height + 1
    print("After", N_FALLING_ROCKS_PART2, "falling rocks the tower will be", total_tower_height, "units tall")


def main(file_name):    
    with open(file_name) as file:
        jet_pattern = file.read().splitlines()[0]

    solve_first_part(jet_pattern)
    solve_second_part(jet_pattern)


if __name__ == "__main__":
    main(parse_file_name())