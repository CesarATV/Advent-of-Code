"""
To solve the first part of the puzzle, a map of the relevant valves is made, so that every valve knows the minimum distance that is has to other relevant valves. The relevant valves are the ones that release pressure different from 0. Once these distances are known, a breadth-first-search algorithm is implemented, starting in the initial position, and coverying every possibility of visiting each remaining valve in every order. 
To reduce the computation (which can take hours), not all nodes are evaluated until their end. To select which nodes are not evaluated, a function estimates an ideal achievable pressure for each path at each given time. If the ideal value is smaller than the currently maximum (non ideal) detected pressure, there is no need to continue visiting that node, so is ignored
The nodes are evaluated in order so that valves with more flow rate are visited first, as in principle these will lead to the path with more pressure

The second part is similar to the first, generating in this case combinations that lead to many pairs of possible paths that are also evaluated by the breadth-first-search function. The used algorithm was not programmed to be greedy, making this part very long to compute: It can take around half an hour to compute (for the non-example input). However, the correct result is known in seconds, as the program visites pairs of pairs that divide the work equally between the two epxlorers, so that one does not visit 1 valve while the other visits 19, as this combination is in principle less effective than dividing the work equally. Although these options are (highly) unlikely to give the ideal result, the program covers them. The current maximum pressure is printed before the end of the program to look at the, very likely to be, correct result
"""

import argparse
import numpy as np
import copy
import itertools
from dataclasses import dataclass

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day16.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day16_example.txt"

STARTING_VALVE = "AA"
N_MINUTES = 30
N_MINUTES_GROUP_EXPLORING = 26
N_GROUP_EXPLORERS = 2

@dataclass
class ValveConnections:
        neighbour_valve_names: list
        valve_routes_dict: dict
        
@dataclass 
class ValvePathParameters:
    path_list: list
    n_minutes_left: int
    accumulated_pressure: int



def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 16: Proboscidea Volcanium")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]


def parse_puzzle_file(lines):
    flow_rate_dict = {}
    valve_dict = {}
    for line in lines:
        split_line = line.split(" ")
        flow_rate = int(split_line[4][5:-1])
        neighbour_valve_names = []
        for idx in range(9,len(split_line)):
            neighbour_valve_names.append(split_line[idx].replace(",",""))

        valve_name = split_line[1]
        if(flow_rate > 0):
            flow_rate_dict[valve_name] = flow_rate

        valve_dict[valve_name] = ValveConnections(neighbour_valve_names, {})
    return flow_rate_dict, valve_dict


def map_valve(parent_valve, current_path_list, flow_rate_dict, valve_dict):
    """ 
    Recursive function that anotates every connection that a given valve has by visiting its neighbours, the neigbhours of their neigbhours, and so on
    The function anotates the minimum distance that every valve has with another
    """ 
    for neighbour_valve_name in parent_valve.neighbour_valve_names:
        if neighbour_valve_name not in current_path_list:
            if(neighbour_valve_name in flow_rate_dict):
                n_elements_before_target = len(current_path_list)
                for idx, valve_in_path in enumerate(current_path_list):
                    distance_to_target = n_elements_before_target - idx

                    if(distance_to_target < valve_dict[valve_in_path].valve_routes_dict[neighbour_valve_name]):
                        valve_dict[valve_in_path].valve_routes_dict[neighbour_valve_name] = distance_to_target # consider only the minimum distance to the target valve

            map_valve(valve_dict[neighbour_valve_name], current_path_list + [neighbour_valve_name], flow_rate_dict, valve_dict)



def map_every_valve(flow_rate_dict, valve_dict):
    for valve in valve_dict.values():
        for target_valve_name in flow_rate_dict:
            valve.valve_routes_dict[target_valve_name] = np.inf

    # make a map of the full valve layout, doing it from every relevant valve (the ones with flow rate bigger than 0 and the starting valve)
    map_valve(valve_dict[STARTING_VALVE], [STARTING_VALVE], flow_rate_dict, valve_dict)
    for flowing_valve_name in flow_rate_dict:
        map_valve(valve_dict[flowing_valve_name], [flowing_valve_name], flow_rate_dict, valve_dict)


def calculate_ideal_pressure(path_to_continue_visiting, valve_to_visit, flow_rate_dict, valve_dict):
    # estimate an ideal pressure, as if it were possible to reach from the reference valve (valve_to_visit) every remaining valve independently
    ideal_pressure = path_to_continue_visiting.accumulated_pressure 
    for flowing_valve_name, flowing_valve_flow_rate in flow_rate_dict.items():
        if(flowing_valve_name not in path_to_continue_visiting.path_list):
            ideal_n_mins_left = path_to_continue_visiting.n_minutes_left - (valve_dict[valve_to_visit].valve_routes_dict[flowing_valve_name] + 1)
            if(ideal_n_mins_left > 0):
                ideal_pressure += ideal_n_mins_left * flowing_valve_flow_rate

    return ideal_pressure


def get_single_explorer_maximum_pressure(potential_paths_to_visit, initial_n_minutes, flow_rate_dict, valve_dict):
    '''
    implements a breadth-first-search over potential_paths_to_visit, which contains al possible initial paths (nodes). The possible path continuations (children nodes) will go to the variable valve_paths_to_visit, which will be reloaded to potential_paths_to_visit until there is no more valve_paths_to_visit.
    To reduce the number of node visits, an ideal pressure value will be continuously calculated for every path. This ideal pressure value will be compared to the current maximum (non-ideal) pressure value. If it is smaller, the no more children nodes from that original node are considered
    '''
    valve_paths_to_visit = [ValvePathParameters([STARTING_VALVE],initial_n_minutes,0)]
    current_maximum_pressure = 0
    while(len(valve_paths_to_visit) != 0):

        visited_valve_path_ref = valve_paths_to_visit.pop(0)
        for valve_to_visit in potential_paths_to_visit:
            if valve_to_visit in visited_valve_path_ref.path_list:
                continue

            path_to_continue_visiting = copy.deepcopy(visited_valve_path_ref)

            path_to_continue_visiting.n_minutes_left = visited_valve_path_ref.n_minutes_left - (valve_dict[path_to_continue_visiting.path_list[-1]].valve_routes_dict[valve_to_visit] + 1)
            if(path_to_continue_visiting.n_minutes_left>0):
                path_to_continue_visiting.accumulated_pressure += path_to_continue_visiting.n_minutes_left * flow_rate_dict[valve_to_visit]

                # estimate an ideal pressure whose value will be compared to the current maximum pressure. If it is smaller, it is impossible that that path will be the optimal, so it can be ignored
                ideal_pressure = calculate_ideal_pressure(path_to_continue_visiting, valve_to_visit, flow_rate_dict, valve_dict)

                if ideal_pressure > current_maximum_pressure:
                    path_to_continue_visiting.path_list.append(valve_to_visit)

                    if (path_to_continue_visiting.accumulated_pressure > current_maximum_pressure):
                        current_maximum_pressure = path_to_continue_visiting.accumulated_pressure
                        current_maximum_pressure_path = path_to_continue_visiting.path_list

                    valve_paths_to_visit.append(path_to_continue_visiting) # keep following this path, as it may be the optimal one
                    
    return current_maximum_pressure, current_maximum_pressure_path



def solve_first_part(flow_rate_dict, valve_dict):
    # sort the valve names by the flow they will release if activated from the starting valve. It can help to process first the valves most likely to be in the best possible path. This in turn will help to avoid processing extra non-optimal paths
    maximum_pressure_per_valve = [(N_MINUTES-1-valve_dict[STARTING_VALVE].valve_routes_dict[path_element])*x for x, path_element in zip(flow_rate_dict.values(),flow_rate_dict.keys())]
    potential_paths_to_visit = [flow_rate_name for _, flow_rate_name in sorted(zip(maximum_pressure_per_valve, flow_rate_dict.keys()),reverse=True)] # sort valves from most to least flow rate

    current_maximum_pressure, current_maximum_pressure_path = get_single_explorer_maximum_pressure(potential_paths_to_visit, N_MINUTES, flow_rate_dict, valve_dict)
            
    print("With {} minutes left the most presure that can be released is {} following the path {}".format(N_MINUTES, current_maximum_pressure, current_maximum_pressure_path[0]), end="")
    for valve_element in current_maximum_pressure_path[1:]:
        print("-{}".format(valve_element), end="")
    print(" (intermediate 0-flow-rate valves ignored for this message)")




def solve_second_part(flow_rate_dict, valve_dict):
    # sort the valve names by the flow they will release if activated from the starting valve. It can help to process first the valves most likely to be in the best possible path. This in turn will help to avoid processing extra non-optimal paths
    maximum_pressure_per_valve = [(N_MINUTES_GROUP_EXPLORING-1-valve_dict[STARTING_VALVE].valve_routes_dict[path_element])*x for x, path_element in zip(flow_rate_dict.values(),flow_rate_dict.keys())]
    potential_paths_to_visit = [flow_rate_name for _, flow_rate_name in sorted(zip(maximum_pressure_per_valve, flow_rate_dict.keys()),reverse=True)] # sort valves from most to least flow rate


    valve_division_team_member_0 = [] # half of this part of the list can be removed, as they will be presented in its complementary list
    for idx in range(round(len(potential_paths_to_visit) /2), len(potential_paths_to_visit)):
        valve_division_team_member_0 += list(itertools.combinations(potential_paths_to_visit, idx)) # half of the ones that take into account half of the list could be removed, as they will be presented in valve_division_team_member_1 list

    # compute the complementary valve paths given the previous paths
    valve_division_team_member_1 = []
    for idx in range(len(valve_division_team_member_0)):
        valve_division_team_member_1 += [tuple(set(flow_rate_dict.keys()).difference(valve_division_team_member_0[idx]))]


    maximum_pressure = 0
    for valve_path_team_member_0, valve_path_team_member_1 in zip(valve_division_team_member_0, valve_division_team_member_1):
        
        valve_per_explorer_list = [valve_path_team_member_0, valve_path_team_member_1]
        current_maximum_pressure = 0
        current_maximum_pressure_path = []
        for idx in range(N_GROUP_EXPLORERS):
            path_pressure, pressure_path = get_single_explorer_maximum_pressure(valve_per_explorer_list[idx], N_MINUTES_GROUP_EXPLORING, flow_rate_dict,valve_dict)
            current_maximum_pressure += path_pressure
            current_maximum_pressure_path.append(pressure_path)
        
        if current_maximum_pressure > maximum_pressure:
            maximum_pressure = current_maximum_pressure
            maximum_pressure_path = current_maximum_pressure_path
            print("Currently, from the visited combinations, the maximum pressure is", maximum_pressure)


    print("With {} explorers working together and {} minutes left the most presure that can be released is {} following the paths {}".format(N_GROUP_EXPLORERS, N_MINUTES_GROUP_EXPLORING, maximum_pressure, maximum_pressure_path[0][0]), end="")
    for valve_element in maximum_pressure_path[0][1:]:
        print("-{}".format(valve_element), end="")
    print(" and {}".format(maximum_pressure_path[1][0]), end="")
    for valve_element in maximum_pressure_path[1][1:]:
        print("-{}".format(valve_element), end="")
    print(" (intermediate 0-flow-rate valves ignored for this message)")




def main(file_name):    
    with open(file_name) as file:
        lines = file.read().splitlines()
    while lines[-1] == "": # remove last empty lines, if any. They do not add information and can cause confusion
        lines.pop()


    flow_rate_dict, valve_dict = parse_puzzle_file(lines)
    map_every_valve(flow_rate_dict, valve_dict)


    solve_first_part(flow_rate_dict, valve_dict)
    solve_second_part(flow_rate_dict, valve_dict)


if __name__ == "__main__":
    main(parse_file_name())


