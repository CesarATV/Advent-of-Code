'''
Both parts follow the position of a variable moving according to the given orientations. To take borders into account, a lists of dictionary containing the wrapping points shows how these borders are connected (a position is used as a key and the position in which it is wrapped is the value of that key, and viceversa). Similar to this, another lists of dictionaries carries the orientation change after wrapping.

The second part has hardcoded the structure of the map for both the example puzzle file and the real puzzle file. It does seem however, that should work in any real puzzle file generate by the Advent of Code website. It is considered hardcoded because it does not work with any arbitrary cube input.
'''

import argparse
import enum

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day22.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day22_example.txt"

EXAMPLE_FILE_LENGTH_LINES = 14 # necessary for the second part, as the format of the cube of the example file is different from the actual puzzle file, and no arbitrary-cube parsing has been done

class Orientation(enum.IntEnum):
    LOWER_LIMIT = -1
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3
    UPPER_LIMIT = 4


NO_PATH = " "
SOLID_WALL = "#"
OPEN_TILE = "."
CLOCKWISE_INSTRUCTION = "R"
COUNTERCLOCKWISE_INSTRUCTION = "L"


def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 22: Monkey Map")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]


def partially_parse_puzzle_file(lines):
    steps_instructions = lines[-1]
    maze = lines[:-2]
    n_rows = len(maze)
    n_cols = 0
    for line in maze:
        possible_n_cols = len(line)
        if possible_n_cols > n_cols:
            n_cols = possible_n_cols

    blocked_paths = set()
    for row_n in range(n_rows):
        n_cols_in_row = len(maze[row_n])
        
        for col_n in range(n_cols_in_row):
            if maze[row_n][col_n] == SOLID_WALL:
                blocked_paths.add((row_n,col_n))

    for col_n in range(n_cols):
        for row_n in range(1,n_rows):

            if col_n >= len(maze[row_n]):
                continue

            if maze[row_n][col_n] == SOLID_WALL:
                blocked_paths.add((row_n,col_n))

    initial_position = (0, maze[0].find(OPEN_TILE))

    return initial_position, steps_instructions, blocked_paths, maze, n_rows, n_cols


def parse_wrapping_points_and_orientations_for_first_part(maze, n_rows, n_cols):
    wrap_points_correspondences_right = {}
    wrap_points_correspondences_left = {}
    wrap_points_correspondences_up = {}
    wrap_points_correspondences_down = {}

    # the use of orientation dictionaries for the first part of the puzzle is a bit redundant (the orientation is mantained when wrapping). It is mostly used for consistency, using the same structure as for the second part of the puzzle
    wrap_points_orientations_right = {}
    wrap_points_orientations_left = {}
    wrap_points_orientations_up = {}
    wrap_points_orientations_down = {}


    for row_n in range(n_rows):
        n_cols_in_row = len(maze[row_n])

        if maze[row_n][0] == NO_PATH:
            possible_wrap_col = -1
        else:
            possible_wrap_col = 0

        for col_n in range(1,n_cols_in_row-1):
            if(maze[row_n][col_n] == NO_PATH):
                continue
            
            else:                    
                if(possible_wrap_col == -1):
                    possible_wrap_col = col_n

        
        wrap_points_correspondences_left[(row_n,possible_wrap_col)] = (row_n,n_cols_in_row-1)
        wrap_points_correspondences_right[(row_n,n_cols_in_row-1)] = (row_n,possible_wrap_col)
        wrap_points_orientations_left[(row_n,possible_wrap_col)] = Orientation.LEFT
        wrap_points_orientations_right[(row_n,n_cols_in_row-1)] = Orientation.RIGHT


    for col_n in range(n_cols):
        if col_n >= len(maze[0]):
            possible_wrap_row = -1
            beginning_has_been_found = False
        elif maze[0][col_n] == NO_PATH:
            possible_wrap_row = -1
            beginning_has_been_found = False
        else:
            possible_wrap_row = 0
            beginning_has_been_found = True

        for row_n in range(1,n_rows):
            
            if col_n >= len(maze[row_n]):
                if beginning_has_been_found == True:
                    
                    wrap_points_correspondences_up[(possible_wrap_row,col_n)] = (row_n-1,col_n)
                    wrap_points_correspondences_down[(row_n-1,col_n)] = (possible_wrap_row,col_n)
                    wrap_points_orientations_up[(possible_wrap_row,col_n)] = Orientation.UP
                    wrap_points_orientations_down[(row_n-1,col_n)] = Orientation.DOWN

                    possible_wrap_row = -1
                    beginning_has_been_found = False

            elif maze[row_n][col_n] == NO_PATH:
                if beginning_has_been_found == True:
                    wrap_points_correspondences_up[(possible_wrap_row,col_n)] = (row_n-1,col_n)
                    wrap_points_correspondences_down[(row_n-1,col_n)] = (possible_wrap_row,col_n)
                    wrap_points_orientations_up[(possible_wrap_row,col_n)] = Orientation.UP
                    wrap_points_orientations_down[(row_n-1,col_n)] = Orientation.DOWN
                    possible_wrap_row = -1
                    break
                
            
            elif beginning_has_been_found == False and possible_wrap_row == -1:
                    possible_wrap_row = row_n
                    beginning_has_been_found = True
            
            

        if possible_wrap_row != -1:
            wrap_points_correspondences_up[(possible_wrap_row,col_n)] = (row_n,col_n)
            wrap_points_correspondences_down[(row_n,col_n)] = (possible_wrap_row,col_n)
            wrap_points_orientations_up[(possible_wrap_row,col_n)] = Orientation.UP
            wrap_points_orientations_down[(row_n,col_n)] = Orientation.DOWN


    wrap_points_correspondences = [0]*Orientation.UPPER_LIMIT
    wrap_points_correspondences[Orientation.RIGHT] = wrap_points_correspondences_right
    wrap_points_correspondences[Orientation.DOWN] = wrap_points_correspondences_down
    wrap_points_correspondences[Orientation.LEFT] = wrap_points_correspondences_left
    wrap_points_correspondences[Orientation.UP] = wrap_points_correspondences_up

    wrap_points_orientations = [0]*Orientation.UPPER_LIMIT
    wrap_points_orientations[Orientation.RIGHT] = wrap_points_orientations_right
    wrap_points_orientations[Orientation.DOWN] = wrap_points_orientations_down
    wrap_points_orientations[Orientation.LEFT] = wrap_points_orientations_left
    wrap_points_orientations[Orientation.UP] = wrap_points_orientations_up


    return wrap_points_correspondences, wrap_points_orientations


def follow_steps(initial_position, steps_instructions, blocked_paths, wrap_points_correspondences, wrap_points_orientations):
    possible_steps = [0 for _ in range(Orientation.UPPER_LIMIT)]
    possible_steps[Orientation.RIGHT] = (0,1)
    possible_steps[Orientation.DOWN] = (1,0)
    possible_steps[Orientation.LEFT] = (0,-1)
    possible_steps[Orientation.UP] = (-1,0)

    next_orientation = Orientation.RIGHT
    position = initial_position
    end_following_path = False
    while end_following_path == False:
        current_orientation = next_orientation

        clockwise_instruction_pos = steps_instructions.find(CLOCKWISE_INSTRUCTION)
        counterclockwise_instruction_pos = steps_instructions.find(COUNTERCLOCKWISE_INSTRUCTION)

        if counterclockwise_instruction_pos == -1 and clockwise_instruction_pos == -1:
            end_following_path = True
            n_steps = int(steps_instructions)
            next_orientation = current_orientation
            orientation_step = 0
        else:
            if counterclockwise_instruction_pos == -1:
                counterclockwise_instruction_pos = clockwise_instruction_pos + 1 # force it to fulfill the conditions below
            elif clockwise_instruction_pos == -1:
                clockwise_instruction_pos = counterclockwise_instruction_pos + 1 # force it to fulfill the conditions below

            if clockwise_instruction_pos < counterclockwise_instruction_pos:
                n_steps = int(steps_instructions[:clockwise_instruction_pos])
                steps_instructions = steps_instructions[clockwise_instruction_pos+1:]
                orientation_step = 1

            elif clockwise_instruction_pos > counterclockwise_instruction_pos:
                n_steps = int(steps_instructions[:counterclockwise_instruction_pos])
                steps_instructions = steps_instructions[counterclockwise_instruction_pos+1:]
                orientation_step = -1

        possible_next_position = list(position)
        possible_current_orientation = current_orientation
        step = possible_steps[current_orientation]
        for _ in range(n_steps):
            possible_next_position[0] += step[0]
            possible_next_position[1] += step[1]
            if position in wrap_points_correspondences[current_orientation]:
                possible_next_position = list(wrap_points_correspondences[current_orientation][position])
                possible_current_orientation = wrap_points_orientations[current_orientation][position]
                step = possible_steps[possible_current_orientation]
                
            if tuple(possible_next_position) not in blocked_paths:
                position = tuple(possible_next_position)
                current_orientation = possible_current_orientation
            else:
                break

        
        next_orientation = Orientation(current_orientation + orientation_step)
        if(next_orientation == Orientation.LOWER_LIMIT):
            next_orientation = Orientation(Orientation.UPPER_LIMIT - 1)
        elif(next_orientation == Orientation.UPPER_LIMIT):
            next_orientation = Orientation(Orientation.LOWER_LIMIT + 1)

    return position, current_orientation


def solve_first_part(initial_position, steps_instructions, blocked_paths, maze, n_rows, n_cols):
    wrap_points_correspondences, wrap_points_orientations = parse_wrapping_points_and_orientations_for_first_part(maze, n_rows, n_cols)

    last_position, last_orientation = follow_steps(initial_position, steps_instructions, blocked_paths, wrap_points_correspondences, wrap_points_orientations)

    position_1_based = (last_position[0]+1, last_position[1]+1)  
    password = 1000*position_1_based[0] + position_1_based[1]*4 + last_orientation

    print("The final position is row {}, column {} and oriented {}, which gives the password {}".format(position_1_based[0], position_1_based[1], Orientation(last_orientation).name.lower(), password) )


def parse_wrapping_points_and_orientations_for_second_part(lines):
    wrap_points_correspondences_right = {}
    wrap_points_correspondences_left = {}
    wrap_points_correspondences_up = {}
    wrap_points_correspondences_down = {}
    wrap_points_orientations_right = {}
    wrap_points_orientations_left = {}
    wrap_points_orientations_up = {}
    wrap_points_orientations_down = {}

    if len(lines) == EXAMPLE_FILE_LENGTH_LINES: # if it is the example file
        cube_dimensions = 4

        # first row of cubes
        col_begin = cube_dimensions*2
        row_begin = 0
        row_dest = cube_dimensions
        col_dest = cube_dimensions
        for movement_step in range(cube_dimensions):
            incoming = (row_begin + movement_step, col_begin) # goes left
            destination = (row_dest, col_dest + movement_step) # appears top
            wrap_points_correspondences_left[incoming] = destination
            wrap_points_correspondences_up[destination] = incoming
            wrap_points_orientations_left[incoming] = Orientation.DOWN
            wrap_points_orientations_up[destination] = Orientation.RIGHT

        col_begin = cube_dimensions*3-1
        row_begin = 0
        row_dest = cube_dimensions*4 - 1
        col_dest = cube_dimensions*3 - 1
        for movement_step in range(cube_dimensions):
            incoming = (row_begin + movement_step, col_begin) # goes right
            destination = (row_dest - movement_step, col_dest) # appears right
            wrap_points_correspondences_right[incoming] = destination
            wrap_points_correspondences_left[destination] = incoming
            wrap_points_orientations_right[incoming] = Orientation.LEFT
            wrap_points_orientations_left[destination] = Orientation.LEFT


        # second row of cubes 
        col_begin = 0
        row_begin = cube_dimensions
        row_dest = cube_dimensions*3-1
        col_dest = cube_dimensions*4-1
        for movement_step in range(cube_dimensions):
            incoming = (row_begin + movement_step, col_begin) # goes left
            destination = (row_dest, col_dest - movement_step) # appears down
            wrap_points_correspondences_left[incoming] = destination
            wrap_points_correspondences_down[destination] = incoming
            wrap_points_orientations_left[incoming] = Orientation.UP
            wrap_points_orientations_down[destination] = Orientation.RIGHT

        col_begin = cube_dimensions*3-1
        row_begin = cube_dimensions
        row_dest = cube_dimensions*2
        col_dest = cube_dimensions*4 - 1
        for movement_step in range(cube_dimensions):
            incoming = (row_begin + movement_step, col_begin) # goes right
            destination = (row_dest, col_dest - movement_step) # appears top
            wrap_points_correspondences_right[incoming] = destination
            wrap_points_correspondences_up[destination] = incoming
            wrap_points_orientations_right[incoming] = Orientation.DOWN
            wrap_points_orientations_up[destination] = Orientation.LEFT


        # third row of cubes (only leftmost)
        col_begin = cube_dimensions*2
        row_begin = cube_dimensions*2
        row_dest = cube_dimensions*2-1
        col_dest = cube_dimensions*2-1
        for movement_step in range(cube_dimensions):
            incoming = (row_begin + movement_step, col_begin) # goes left
            destination = (row_dest, col_dest - movement_step) # appears down
            wrap_points_correspondences_left[incoming] = destination
            wrap_points_correspondences_down[destination] = incoming
            wrap_points_orientations_left[incoming] = Orientation.UP
            wrap_points_orientations_down[destination] = Orientation.RIGHT

        # first column of cubes
        col_begin = 0
        row_begin = cube_dimensions
        row_dest = 0
        col_dest = cube_dimensions*3-1
        for movement_step in range(cube_dimensions):
            incoming = (row_begin, col_begin + movement_step) # goes top
            destination = (row_dest, col_dest - movement_step) # appears top
            wrap_points_correspondences_up[incoming] = destination
            wrap_points_correspondences_up[destination] = incoming
            wrap_points_orientations_up[incoming] = Orientation.DOWN
            wrap_points_orientations_up[destination] = Orientation.DOWN

        col_begin = 0
        row_begin = cube_dimensions*2-1
        row_dest = cube_dimensions*3-1
        col_dest = cube_dimensions*3-1
        for movement_step in range(cube_dimensions):
            incoming = (row_begin, col_begin + movement_step) # goes bottom
            destination = (row_dest, col_dest - movement_step) # appears bottom
            wrap_points_correspondences_down[incoming] = destination
            wrap_points_correspondences_down[destination] = incoming
            wrap_points_orientations_down[incoming] = Orientation.UP
            wrap_points_orientations_down[destination] = Orientation.UP



    else: 
        cube_dimensions = 50

        # first row of cubes
        row_begin = 0
        col_begin = cube_dimensions
        row_dest = cube_dimensions*3-1
        col_dest = 0
        for movement_step in range(cube_dimensions):
            incoming = (row_begin + movement_step, col_begin) # goes left
            destination = (row_dest - movement_step, col_dest) # appears left
            wrap_points_correspondences_left[incoming] = destination 
            wrap_points_correspondences_left[destination] = incoming
            wrap_points_orientations_left[incoming] = Orientation.RIGHT
            wrap_points_orientations_left[destination] = Orientation.RIGHT

        row_begin = 0
        col_begin = cube_dimensions*3-1
        row_dest = cube_dimensions*3 - 1
        col_dest = cube_dimensions*2 - 1
        for movement_step in range(cube_dimensions):
            incoming = (row_begin + movement_step, col_begin) # goes right
            destination = (row_dest - movement_step, col_dest) # appears right
            wrap_points_correspondences_right[incoming] = destination
            wrap_points_correspondences_right[destination] = incoming
            wrap_points_orientations_right[incoming] = Orientation.LEFT
            wrap_points_orientations_right[destination] = Orientation.LEFT

        # second row of cubes
        row_begin = cube_dimensions
        col_begin = cube_dimensions
        row_dest = cube_dimensions*2
        col_dest = 0
        for movement_step in range(cube_dimensions):
            incoming = (row_begin + movement_step, col_begin) # goes left
            destination = (row_dest, col_dest + movement_step) # appears top
            wrap_points_correspondences_left[incoming] = destination
            wrap_points_correspondences_up[destination] = incoming
            wrap_points_orientations_left[incoming] = Orientation.DOWN
            wrap_points_orientations_up[destination] = Orientation.RIGHT

        row_begin = cube_dimensions
        col_begin = cube_dimensions*2-1
        row_dest = cube_dimensions - 1
        col_dest = cube_dimensions*2
        for movement_step in range(cube_dimensions):
            incoming = (row_begin + movement_step, col_begin) # goes right
            destination = (row_dest, col_dest + movement_step) # appears down
            wrap_points_correspondences_right[incoming] = destination
            wrap_points_correspondences_down[destination] = incoming
            wrap_points_orientations_right[incoming] = Orientation.UP
            wrap_points_orientations_down[destination] = Orientation.LEFT

        
        # fourth row of cubes
        row_begin = cube_dimensions*3
        col_begin = 0
        row_dest = 0
        col_dest = cube_dimensions*2 - 1
        for movement_step in range(cube_dimensions):
            incoming = (row_begin + movement_step, col_begin) # goes left
            destination = (row_dest, col_dest - movement_step) # appears top
            wrap_points_correspondences_left[incoming] = destination
            wrap_points_correspondences_up[destination] = incoming
            wrap_points_orientations_left[incoming] = Orientation.DOWN
            wrap_points_orientations_up[destination] = Orientation.RIGHT

        row_begin = cube_dimensions*3
        col_begin = cube_dimensions - 1
        row_dest = cube_dimensions*3 - 1
        col_dest = cube_dimensions
        for movement_step in range(cube_dimensions):
            incoming = (row_begin + movement_step, col_begin) # goes right
            destination = (row_dest, col_dest + movement_step) # appears down
            wrap_points_correspondences_right[incoming] = destination
            wrap_points_correspondences_down[destination] = incoming
            wrap_points_orientations_right[incoming] = Orientation.UP
            wrap_points_orientations_down[destination] = Orientation.LEFT


        # first column of cubes
        row_begin = cube_dimensions*4-1
        col_begin = 0
        row_dest = 0
        col_dest = cube_dimensions*2
        for movement_step in range(cube_dimensions):
            incoming = (row_begin, col_begin + movement_step) # goes down
            destination = (row_dest, col_dest + movement_step) # appears up
            wrap_points_correspondences_down[incoming] = destination
            wrap_points_correspondences_up[destination] = incoming
            wrap_points_orientations_down[incoming] = Orientation.DOWN
            wrap_points_orientations_up[destination] = Orientation.UP


    wrap_points_correspondences = [0]*Orientation.UPPER_LIMIT
    wrap_points_correspondences[Orientation.RIGHT] = wrap_points_correspondences_right
    wrap_points_correspondences[Orientation.DOWN] = wrap_points_correspondences_down
    wrap_points_correspondences[Orientation.LEFT] = wrap_points_correspondences_left
    wrap_points_correspondences[Orientation.UP] = wrap_points_correspondences_up

    wrap_points_orientations = [0]*Orientation.UPPER_LIMIT
    wrap_points_orientations[Orientation.RIGHT] = wrap_points_orientations_right
    wrap_points_orientations[Orientation.DOWN] = wrap_points_orientations_down
    wrap_points_orientations[Orientation.LEFT] = wrap_points_orientations_left
    wrap_points_orientations[Orientation.UP] = wrap_points_orientations_up


    return wrap_points_correspondences, wrap_points_orientations


def solve_second_part(lines, initial_position, steps_instructions, blocked_paths):
    wrap_points_correspondences, wrap_points_orientations = parse_wrapping_points_and_orientations_for_second_part(lines)

    last_position, last_orientation = follow_steps(initial_position, steps_instructions, blocked_paths, wrap_points_correspondences, wrap_points_orientations)

    position_1_based = (last_position[0]+1, last_position[1]+1)  
    password = 1000*position_1_based[0] + position_1_based[1]*4 + last_orientation

    print("Considering walking in a cube, the final position is row {}, column {} and oriented {}, which gives the password {}".format(position_1_based[0], position_1_based[1], Orientation(last_orientation).name.lower(), password) )


def main(file_name):    
    with open(file_name) as file:
        lines = file.read().splitlines()
    while lines[-1] == "": # remove last empty lines, if any. They do not add information and can cause confusion
        lines.pop()

    initial_position, steps_instructions, blocked_paths, maze, n_rows, n_cols = partially_parse_puzzle_file(lines)

    solve_first_part(initial_position, steps_instructions, blocked_paths, maze, n_rows, n_cols)
    solve_second_part(lines, initial_position, steps_instructions, blocked_paths)


if __name__ == "__main__":
    main(parse_file_name())