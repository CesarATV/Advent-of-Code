'''
The implemented solution is a depth-first search approach that takes into account all paths until finding the shortest. The solution takes advantage of the fact that the blizzards are cyclical. This fact is used to determine when a path has to be cut out because it has already been visited in a previous-looped instant. It is also used to keep all the movements of the blizzard stored into memory as a function of time, avoiding to calculate them for every single time step in each single path.
To reduce the number of paths to visit, the current time that a path is taking to finish is compared to the current minimum time for an already finished path. If the current time is equal or bigger than this minimum, the path can be ignored.
'''

import argparse
import numpy as np

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day24.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day24_example.txt"

N_EXTRA_ROW_BORDERS_CONSIDERED = 2


def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 24: Blizzard Basin")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]



def parse_puzzle_file(lines):
    n_rows = len(lines) + N_EXTRA_ROW_BORDERS_CONSIDERED # N_EXTRA_ROW_BORDERS_CONSIDERED (2) extra rows are considered in order to take into account the borders of the map. These borders will be marked as impossible to access in further functions
    n_cols = len(lines[0])
    starting_position = (1, lines[0].find("."))
    ending_position = (n_rows-2, lines[-1].find("."))

    left_blizzards = []
    right_blizzards = []
    up_blizzards = []
    down_blizzards = []
    for row_idx, line in enumerate(lines[1:-1], start=2):
        for col_idx, character in enumerate(line[1:-1], start=1):
            if character == "<":
                left_blizzards.append((row_idx,col_idx))
            elif character == ">":
                right_blizzards.append((row_idx,col_idx))
            elif character == "^":
                up_blizzards.append((row_idx,col_idx))
            elif character == "v":
                down_blizzards.append((row_idx,col_idx))

    left_blizzards = np.array(left_blizzards)
    right_blizzards = np.array(right_blizzards)
    up_blizzards = np.array(up_blizzards)
    down_blizzards = np.array(down_blizzards)

    return starting_position, ending_position, n_rows, n_cols, left_blizzards, right_blizzards, up_blizzards, down_blizzards


def get_blizzard_map_over_time(starting_position, ending_position, n_rows, n_cols, left_blizzards, right_blizzards, up_blizzards, down_blizzards):
    ''' 
    Create a map representing which cells are covered by a blizzard in each time instant. The maximum time considered is the common multiple of the number of rows and columns, as this number warantees to fully cover all blizzard periods
    '''

    time_until_blizzards_loop = np.lcm(n_rows-2*N_EXTRA_ROW_BORDERS_CONSIDERED,n_cols-2) # the blizzards can move in all the map except on the borders
    covered_by_blizzard_map = np.zeros([time_until_blizzards_loop,n_rows,n_cols], dtype=bool)
    # consider the map borders (unreacheable) also covered
    covered_by_blizzard_map[:,:N_EXTRA_ROW_BORDERS_CONSIDERED,:] = True
    covered_by_blizzard_map[:,n_rows-N_EXTRA_ROW_BORDERS_CONSIDERED:,:] = True 
    covered_by_blizzard_map[:,:,0] = True 
    covered_by_blizzard_map[:,:,n_cols-1] = True

    # the only reachable positions in the borders are the starting and ending ones
    covered_by_blizzard_map[:,starting_position[0],starting_position[1]] = False 
    covered_by_blizzard_map[:,ending_position[0],ending_position[1]] = False

    left_limit = 0
    right_limit = n_cols-1
    up_limit = 1
    down_limit = n_rows-2
    for time_idx in range(time_until_blizzards_loop):

        covered_by_blizzard_map[time_idx][tuple(left_blizzards.T)] = True
        covered_by_blizzard_map[time_idx][tuple(right_blizzards.T)] = True
        covered_by_blizzard_map[time_idx][tuple(up_blizzards.T)] = True
        covered_by_blizzard_map[time_idx][tuple(down_blizzards.T)] = True

        # prepare for next time instant
        left_blizzards += [0,-1]
        right_blizzards += [0,1]
        up_blizzards += [-1,0]
        down_blizzards += [1,0]

        left_blizzards[left_blizzards[:,1] <= left_limit] += [0,right_limit-1]
        right_blizzards[right_blizzards[:,1] >= right_limit] -= [0,right_limit-1] - np.array([0,left_limit])
        up_blizzards[up_blizzards[:,0] <= up_limit] += [down_limit-N_EXTRA_ROW_BORDERS_CONSIDERED,0]
        down_blizzards[down_blizzards[:,0] >= down_limit] -= [down_limit-N_EXTRA_ROW_BORDERS_CONSIDERED,0] - np.array([up_limit-1,0])

    
    return covered_by_blizzard_map


def consider_movement(paths_to_visit, paths_considered_to_visit, covered_by_blizzard_map, current_time_mod, considered_time, considered_position):
    considered_position_mod = (current_time_mod, considered_position[1], considered_position[2])
    '''
    Check if a considered movement is possible. If it is, it will be added to paths_considered_to_visit 
    '''

    if covered_by_blizzard_map[current_time_mod, considered_position[1], considered_position[2]] == False:
        if considered_position_mod in paths_considered_to_visit[current_time_mod]:
            if considered_time < paths_considered_to_visit[current_time_mod][considered_position_mod]: # revisit the path only if there is a chance to get a smaller time
                paths_to_visit.append(considered_position)
                paths_considered_to_visit[current_time_mod][considered_position_mod] = considered_time
        else:
            paths_to_visit.append(considered_position)
            paths_considered_to_visit[current_time_mod][considered_position_mod] = considered_time


def solve_first_part(starting_position, ending_position, covered_by_blizzard_map, starting_time=0, print_result=True):
    time_until_blizzards_loop = covered_by_blizzard_map.shape[0]
    paths_considered_to_visit = [{} for _ in range(time_until_blizzards_loop)] # list of dictionaries that show the paths already visited in each minute, in order to not consider them again. This can happen quite often (for example, going up and then down is equivalent to waiting in the same position two minutes in a row). The dictionaries keep the actual number of minutes in which the path was reached, for the plausible (although unlikely) case in which it may have taken less time to reach the same position. This value of time is different from the time value which is used to index one dictionary or another, as this index time is looped. The dictionaries store variables as a tuple as (time,row,column)
    paths_to_visit = [np.hstack([starting_time,starting_position])] # lists of positions and times from which a movement can be considered
    paths_considered_to_visit[0][ (starting_time%time_until_blizzards_loop,starting_position[0], starting_position[1])] = 0
    
    minimum_arrival_minutes = np.inf
    while len(paths_to_visit) != 0:
        current_time_and_position = paths_to_visit.pop() # the first element is the time (minutes), the second the rows and the third the columns

        current_time = current_time_and_position[0] + 1
        if(current_time >= minimum_arrival_minutes):
            continue # do not consider paths that cannot be faster than an already visited path

        current_time_and_position[0] = current_time
        left_movement = current_time_and_position + [0,0,-1]
        right_movement = current_time_and_position + [0,0,1]
        up_movement = current_time_and_position + [0,-1,0]
        down_movement = current_time_and_position + [0,1,0]

        if np.all(down_movement[1:] == ending_position):
            if current_time < minimum_arrival_minutes:
                minimum_arrival_minutes = current_time 
        else:
            current_time_mod = current_time % time_until_blizzards_loop
            
            # the order in which these functions are executed can affect noticeably the time it takes to the program to finish. As the movement from start to end is from the top left to the bottom right, movements that go to the right and down should be prioritized. To do this, they are considered after the other possible movements, so that they appear as last elements in the stack, therefore being checked before many others
            consider_movement(paths_to_visit, paths_considered_to_visit, covered_by_blizzard_map, current_time_mod, current_time, left_movement)
            consider_movement(paths_to_visit, paths_considered_to_visit, covered_by_blizzard_map, current_time_mod, current_time, up_movement)
            consider_movement(paths_to_visit, paths_considered_to_visit, covered_by_blizzard_map, current_time_mod, current_time, current_time_and_position)
            consider_movement(paths_to_visit, paths_considered_to_visit, covered_by_blizzard_map, current_time_mod, current_time, down_movement)
            consider_movement(paths_to_visit, paths_considered_to_visit, covered_by_blizzard_map, current_time_mod, current_time, right_movement)

    if print_result:
        print("The trip requires a minimum of {} minutes to reach the goal".format(minimum_arrival_minutes))
    
    return minimum_arrival_minutes
        

def goal_to_start(starting_position, ending_position, covered_by_blizzard_map, starting_time=0, print_result=True):
    '''
    This function contains mostly the same code as solve_first_part, varying only in which movement is checked to see if the ending position has been reached (up instead of down is checked), and the order of execution of the movements to consider (higher priority to movements that go left and up)
    '''
    time_until_blizzards_loop = covered_by_blizzard_map.shape[0]
    paths_considered_to_visit = [{} for _ in range(time_until_blizzards_loop)]
    paths_to_visit = [np.hstack([starting_time,starting_position])]
    paths_considered_to_visit[0][(starting_time%time_until_blizzards_loop,starting_position[0], starting_position[1])] = 0
    
    minimum_arrival_minutes = np.inf
    while len(paths_to_visit) != 0:
        current_time_and_position = paths_to_visit.pop()

        current_time = current_time_and_position[0] + 1
        if(current_time >= minimum_arrival_minutes):
            continue # do not consider paths that cannot be faster than an already visited path

        current_time_and_position[0] = current_time
        left_movement = current_time_and_position + [0,0,-1]
        right_movement = current_time_and_position + [0,0,1]
        up_movement = current_time_and_position + [0,-1,0]
        down_movement = current_time_and_position + [0,1,0]
        
        if np.all(up_movement[1:] == ending_position):
            if current_time < minimum_arrival_minutes:
                minimum_arrival_minutes = current_time 
        else:
            current_time_mod = current_time % time_until_blizzards_loop

            consider_movement(paths_to_visit, paths_considered_to_visit, covered_by_blizzard_map, current_time_mod, current_time, right_movement)
            consider_movement(paths_to_visit, paths_considered_to_visit, covered_by_blizzard_map, current_time_mod, current_time, down_movement)
            consider_movement(paths_to_visit, paths_considered_to_visit, covered_by_blizzard_map, current_time_mod, current_time, current_time_and_position)
            consider_movement(paths_to_visit, paths_considered_to_visit, covered_by_blizzard_map, current_time_mod, current_time, up_movement)
            consider_movement(paths_to_visit, paths_considered_to_visit, covered_by_blizzard_map, current_time_mod, current_time, left_movement)
            

    if print_result:
        print("The path requires {}".format(minimum_arrival_minutes))
    
    return minimum_arrival_minutes


def solve_second_part(starting_position, ending_position, covered_by_blizzard_map, n_minutes_first_trip=0):
    # as one of the movements to consider is waiting, and this can be done infinitely in the starting and ending positions (as they do not get hit by blizzards), it is possible to simulate the full trip as three different trips, just by measuring the minimum amount of time in which those trips can be done
    start_to_goal = solve_first_part
    if n_minutes_first_trip == 0:
        n_minutes_first_trip = start_to_goal(starting_position, ending_position, covered_by_blizzard_map, print_result=False)

    n_minutes_back_and_forth = goal_to_start(ending_position, starting_position, covered_by_blizzard_map, starting_time=n_minutes_first_trip, print_result=False)

    n_minutes_full_trip = start_to_goal(starting_position, ending_position, covered_by_blizzard_map, starting_time=n_minutes_back_and_forth, print_result=False)

    n_minutes_back_trip = n_minutes_back_and_forth - n_minutes_first_trip
    n_minutes_final_trip = n_minutes_full_trip - n_minutes_back_and_forth
    print("The full trip requires {} minutes, {} to go to the goal, {} to go from the goal to the start and {} to go from the start to the goal again".format(n_minutes_full_trip, n_minutes_first_trip, n_minutes_back_trip, n_minutes_final_trip))
    


def main(file_name):    
    with open(file_name) as file:
        lines = file.read().splitlines()
    while lines[-1] == "": # remove last empty lines, if any. They do not add information and can cause confusion
        lines.pop()


    starting_position, ending_position, n_rows, n_cols, left_blizzards, right_blizzards, up_blizzards, down_blizzards = parse_puzzle_file(lines)
    
    covered_by_blizzard_map = get_blizzard_map_over_time(starting_position, ending_position, n_rows, n_cols, left_blizzards, right_blizzards, up_blizzards, down_blizzards)

    minimum_arrival_minutes = solve_first_part(starting_position, ending_position, covered_by_blizzard_map)
    solve_second_part(starting_position, ending_position, covered_by_blizzard_map, minimum_arrival_minutes)
    

if __name__ == "__main__":
    main(parse_file_name())


