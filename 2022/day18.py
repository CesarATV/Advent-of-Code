'''
TODO the code for the second part takes to long to compute (more than 2 minutes) while there are many possibilities to improve it
TODO the code can benefit a lot from more numpy notation instead of loops
TODO the recursive function that checks if a block is in air pocket should mark all members of the air pocket in order to not visit them again
'''

import argparse
import numpy as np

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day18.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day18_example.txt"

N_FACES_OF_A_CUBE = 6

def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 18: Boiling Boulders")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]


def parse_puzzle_file(lines):
    maximum_x = 0
    maximum_y = 0
    maximum_z = 0
    for line in lines:
        proposed_x, proposed_y, proposed_z = list(map(int,line.split(",")))
        if proposed_x>maximum_x:
            maximum_x = proposed_x
        if proposed_y>maximum_y:
            maximum_y = proposed_y
        if proposed_z>maximum_z:
            maximum_z = proposed_z

    border_space = 2 # add extra space in each dimension (e.g. 1 on the bottom and 1 on the top) to leave at least 1 empty space beteen the boulder and the air 
    boulder = np.zeros([maximum_x+1+border_space,maximum_y+1+border_space,maximum_z+1+border_space], dtype=bool) # every True element represents that there is a block in the boulder 
    for line in lines:
        boulder[tuple(np.array(list(map(int,line.split(",")))) +1)] = True

    return boulder


def check_surface_of_boulder_block(boulder, x_base, y_base, z_base):
    exposed_surface = 0
    exposed_surface += np.sum(boulder[x_base-1:x_base+2:2, y_base, z_base] == False)

    exposed_surface += np.sum(boulder[x_base, y_base-1:y_base+2:2, z_base] == False)

    exposed_surface += np.sum(boulder[x_base, y_base, z_base-1:z_base+2:2] == False)

    return exposed_surface


def solve_first_part(boulder):
    surface_area = 0
    for x, y, z in np.ndindex(boulder.shape):
        if boulder[x,y,z] == True: # if there is a block in the boulder, it may have exposed surface
            surface_area += check_surface_of_boulder_block(boulder, x,y,z)
    
    print("The total surface area is", surface_area)



def is_block_a_exterior_border(boulder,x,y,z):
    idxmax = np.where(boulder[:,y,z] == True)[0]
    if len(idxmax) == 0 or x > np.max(idxmax):
        return True

    idymax = np.where(boulder[x,:,z] == True)[0]
    if len(idymax) == 0 or y > np.max(idymax):
        return True

    idzmax = np.where(boulder[x,y,:] == True)[0]
    if len(idzmax) == 0:
        return True
    else:
        idzmax = np.max(idzmax)

    idxmin = np.where(boulder[:,y,z] == 1)[0]
    if len(idxmin) == 0:
        return True
    else:
        idxmin = np.min(idxmin)

    idymin = np.where(boulder[x,:,z] == 1)[0]
    if len(idymin) == 0:
        return True
    else:
        idymin = np.min(idymin)

    idzmin = np.where(boulder[x,y,:] == 1)[0]
    if len(idzmin) == 0:
        return True
    else:
        idzmin = np.min(idzmin)

    if z > idzmax or x < idxmin or y < idymin or z < idzmin:
        return True

    return False


def is_block_in_an_air_pocket(boulder,x,y,z):
    visited_list = [[x+1,y,z],[x-1,y,z],[x,y+1,z],[x,y-1,z],[x,y,z+1],[x,y,z-1]]
    air_pocket_neighbours = [[x+1,y,z],[x-1,y,z],[x,y+1,z],[x,y-1,z],[x,y,z+1],[x,y,z-1]]
    while len(air_pocket_neighbours) != 0:
        test_x,test_y,test_z = air_pocket_neighbours.pop(0)
        if boulder[(test_x,test_y,test_z)] == 1:
            continue
        elif is_block_a_exterior_border(boulder,test_x,test_y,test_z) == True:
            return False
        else:
            for proposal in [[test_x+1,test_y,test_z],[test_x-1,test_y,test_z],[test_x,test_y+1,test_z],[test_x,test_y-1,test_z],[test_x,test_y,test_z+1],[test_x,test_y,test_z-1]]:
                if proposal not in visited_list:
                    air_pocket_neighbours += [proposal]
                    visited_list += [proposal]
    return True



def solve_second_part(boulder):
    surface_area = 0
    for x, y, z in np.ndindex(boulder.shape):
        if boulder[x,y,z] == True:
            surface_area += check_surface_of_boulder_block(boulder,x,y,z)
        else:
            if is_block_a_exterior_border(boulder,x,y,z) == False:
                if is_block_in_an_air_pocket(boulder,x,y,z) == True:
                    # if the block is in an air buble within the boulder, do not consider the surface area that it covers. This surface has to be subtracted from the total
                    surface_area += (-N_FACES_OF_A_CUBE + check_surface_of_boulder_block(boulder,x,y,z))

    print("The exterior surface area is", surface_area)


def main(file_name):    
    with open(file_name) as file:
        lines = file.read().splitlines()
    while lines[-1] == "": # remove last empty lines, if any. They do not add information and can cause confusion
        lines.pop()

    boulder = parse_puzzle_file(lines)
    solve_first_part(boulder)
    solve_second_part(boulder)


if __name__ == "__main__":
    main(parse_file_name())