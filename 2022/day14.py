'''
For both parts, this program simulates each movement of falling sand, checking in every step is it hits a blocked node, in which case it needs to drop to another position or remains stacked. To avoid many computations, all movements of the falling sand are stored in a vector. This allows to avoid computing every movement for every sand unit, as every unit of sand moves exactly as the previous unit except for the last movement.

Although the second part is fast enough, it could be possible to do it in another, perhaps faster, way: calculating the amount of sand that would be occupied by the sand if there were no blocked nodes, and then subtracting to this number the amount occupied by the blocked nodes plus the nodes that the blocked nodes make inaccessible 
'''

import argparse

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day14.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day14_example.txt"


SAND_SOURCE_POSITION = (500,0)
EXTRA_BORDER_LIMIT = 2


def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 14: Regolith Reservoir")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]


def parse_puzzle_file(lines):
    blocked_nodes = set()
    for line in lines:
        path_nodes = line.split(" -> ")

        path_begin = [int(x) for x in path_nodes[0].split(",")]
        for path_end_string in path_nodes[1:]:
            path_end = [int(x) for x in path_end_string.split(",")]

            if path_begin[0] == path_end[0]:
                sorted_begin, sorted_end  = sorted([path_begin[1],path_end[1]])
                for idx in range(sorted_begin,sorted_end+1):
                    blocked_nodes.add((path_begin[0],idx))
            else:
                sorted_begin, sorted_end  = sorted([path_begin[0],path_end[0]])
                for idx in range(sorted_begin,sorted_end+1):
                    blocked_nodes.add((idx,path_begin[1]))

            path_begin = path_end
            
    return blocked_nodes


def solve_first_part(blocked_nodes):
    lower_border = max([node[1] for node in blocked_nodes]) # after this border (y coordinate), the sand falls into the abyss

    falling_sand_positions = [SAND_SOURCE_POSITION] # positions in x and y coordinates. This vector tracks all the positions visited by falling sand. As every falling sand follows the same path until their last movement, this vector allows to compute the same movements every time
    stacked_sand = 0
    sand_fell_into_abyss = False
    while sand_fell_into_abyss == False:
        sand_has_stacked = False
        while sand_has_stacked == False:
            sand_position = falling_sand_positions[-1]
            # vertical drop
            if (sand_position[0], sand_position[1] +1) in blocked_nodes:

                # left diagonal
                if (sand_position[0]-1, sand_position[1] +1) in blocked_nodes:

                    # right diagonal
                    if (sand_position[0]+1, sand_position[1]+1) in blocked_nodes:

                        blocked_nodes.add(sand_position)
                        falling_sand_positions.pop()
                        sand_has_stacked = True
                                
                    else:
                        falling_sand_positions.append( (sand_position[0]+1,sand_position[1]+1) )
                else:
                    falling_sand_positions.append( (sand_position[0]-1,sand_position[1]+1) )
                    
            else:
                falling_sand_positions.append( (sand_position[0],sand_position[1]+1) )

            if sand_position[1] > lower_border:
                sand_fell_into_abyss = True
                break

        if(sand_fell_into_abyss == False):
            stacked_sand += 1
            
    print("The amount of stacked sand before some fells into the abyss is", stacked_sand)


def solve_second_part(blocked_nodes):
    '''
    This function is very similar to solve_first_part bar some small differences. These are mostly result of checking if sand tries to bypass the border
    '''

    lower_border = max([node[1] for node in blocked_nodes]) + EXTRA_BORDER_LIMIT # is a separate variable from blocked_nodes because the x size is infinite. This variable represents then only the y coordinate

    falling_sand_positions = [SAND_SOURCE_POSITION] # positions in x and y coordinates. This vector tracks all the positions visited by falling sand. As every falling sand follows the same path until their last movement, this vector allows to compute the same movements every time
    stacked_sand = 0
    source_is_blocked = False
    while source_is_blocked == False:
        sand_has_stacked = False
        while sand_has_stacked == False:

            sand_position = falling_sand_positions[-1]
            if sand_position[1]+1 == lower_border:
                blocked_nodes.add(sand_position)
                falling_sand_positions.pop()
                sand_has_stacked = True

                if sand_position == SAND_SOURCE_POSITION:
                    source_is_blocked = True

            # vertical drop
            elif (sand_position[0], sand_position[1] +1) in blocked_nodes:

                # left diagonal
                if (sand_position[0]-1, sand_position[1] +1) in blocked_nodes:

                    # right diagonal
                    if (sand_position[0]+1, sand_position[1]+1) in blocked_nodes:

                        blocked_nodes.add(sand_position)
                        falling_sand_positions.pop()
                        sand_has_stacked = True


                        if sand_position == SAND_SOURCE_POSITION:
                            source_is_blocked = True
                                
                    else:
                        falling_sand_positions.append( (sand_position[0]+1,sand_position[1]+1) )
                else:
                    falling_sand_positions.append( (sand_position[0]-1,sand_position[1]+1) )
                    
            else:
                falling_sand_positions.append( (sand_position[0],sand_position[1]+1) )

        stacked_sand += 1
            
    print("The amount of stacked sand before the sand source is blocked is", stacked_sand)


def main(file_name): 
    with open(file_name) as file:
        lines = file.read().splitlines()
    while lines[-1] == "": # remove last empty lines, if any. They do not add information and can cause confusion
        lines.pop()

    blocked_nodes = parse_puzzle_file(lines)
    solve_first_part(blocked_nodes.copy())
    solve_second_part(blocked_nodes)

if __name__ == "__main__":
    main(parse_file_name())


