'''
The implemented solution is a depth-first search approach that takes into account all posibilities until finding the maximum atteinable number of geodes. The different possibilities (here called paths) that can be done during an iteration (every minute) are building one of any type of robot or not building anything. In order to reduce the computational time:

* No more robots of a type are built if the number of resources of that type that can be spent in one turn is equal to the number of robots. This is because it would be useless to build more to collect more of that type, as there is no time to spend it.
* An ideal number of geodes is calculated every turn. If this ideal number of geodes is smaller than the actual number of geodes already gotten by a path, this first path is not taken anymore in consideration. To complement this idea, the robots in which the different paths are added to the list of path to process, gives priority to paths that create robots, in particular geode robots.
* If nothing was built during a round when a robot could have been built, it will not be possible to build that specific kind of robot until a robot of another kind has been built. This avoids creating redundant paths (e.g. a path that builds an ore robot and then waits 1 minute is always equal or better than a path that waits 1 minute and then builds an ore robot)


Note: The puzzle instructions, although not totally and completely explicitly, say that only one robot can be built in a minute. Therefore, no more than one robot can be built in that minute. Previous versions of this program did not take that into consideration and assummed that two robots could be built at the same time, increasing greatly the complexity of the problem and extending the time to compute it.
'''

import argparse
import copy
import numpy as np
from dataclasses import dataclass

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day19.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day19_example.txt"

N_MINUTES = 24
N_MINUTES_PART2 = 32
N_BLUEPRINTS_TO_CONSIDER_PART2 = 3


def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 19")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]

    
@dataclass 
class BlueprintCosts:
    ore_robot_cost_ore: int

    clay_robot_cost_ore: int

    obsidian_robot_cost_ore: int
    obsidian_robot_cost_clay: int

    geode_robot_cost_ore: int
    geode_robot_cost_obsidian: int



def parse_puzzle_file(lines):
    blueprint_list = []
    for line in lines:
        if line == "":
            continue
        split_line = line.split(" ")

        ore_robot_cost_ore = int(split_line[6])
        clay_robot_cost_ore = int(split_line[12])

        obsidian_robot_cost_ore = int(split_line[18])
        obsidian_robot_cost_clay = int(split_line[21])

        geode_robot_cost_ore = int(split_line[27])
        geode_robot_cost_obsidian = int(split_line[30])


        blueprint_list.append(BlueprintCosts(ore_robot_cost_ore, clay_robot_cost_ore, obsidian_robot_cost_ore, obsidian_robot_cost_clay, geode_robot_cost_ore, geode_robot_cost_obsidian))

    return blueprint_list



class RobotBuildingPath:
    def __init__(self, blueprint, n_minutes_left):
        self.blueprint = blueprint

        self.n_minutes_left = n_minutes_left
        self.n_ore = 0
        self.n_clay = 0
        self.n_obsidian = 0
        self.n_geode = 0

        self.list_of_past_actions = []

        self.n_ore_robots = 1
        self.n_clay_robots = 0
        self.n_obsidian_robots = 0
        self.n_geode_robots = 0


        self.n_max_ore_robots = max(blueprint.ore_robot_cost_ore, blueprint.clay_robot_cost_ore, blueprint.obsidian_robot_cost_ore, blueprint.geode_robot_cost_ore)
        self.n_max_clay_robots = blueprint.obsidian_robot_cost_clay
        self.n_max_obsidian_robots = blueprint.geode_robot_cost_obsidian

        # flags that prevent building a robot if in the previous turn that robot could have been built and instead no robot at all was built
        self.could_have_bought_obsidian_robot_but_did_nothing = False
        self.could_have_bought_ore_robot_but_did_nothing = False
        self.could_have_bought_clay_robot_but_did_nothing = False

    def collect(self):
        self.n_minutes_left -= 1
        self.n_ore += self.n_ore_robots
        self.n_clay += self.n_clay_robots
        self.n_obsidian += self.n_obsidian_robots
        self.n_geode += self.n_geode_robots

    def reset_could_have_bought_flags(self):
        self.could_have_bought_obsidian_robot_but_did_nothing = False
        self.could_have_bought_ore_robot_but_did_nothing = False
        self.could_have_bought_clay_robot_but_did_nothing = False

    def ideal_path_estimation(self):
        '''
        Estimates an ideal number of geodes. For this, it assumes that in all remaining turns, a geode robot could have been built, and then adds that number to the actual number of geode robots multiplied by the remaining time.
        '''
 
        n_geode_ideal = self.n_geode + self.n_geode_robots*self.n_minutes_left
        n_geode_ideal += sum(range(1,self.n_minutes_left+1))
        return n_geode_ideal

    def build_ore_robot(self):
        new_robot_path = copy.deepcopy(self)
        new_robot_path.n_ore -= self.blueprint.ore_robot_cost_ore
        new_robot_path.n_ore_robots += 1
        new_robot_path.reset_could_have_bought_flags()
        return new_robot_path

    def build_clay_robot(self):
        new_robot_path = copy.deepcopy(self)
        new_robot_path.n_ore -= self.blueprint.clay_robot_cost_ore
        new_robot_path.n_clay_robots += 1
        new_robot_path.reset_could_have_bought_flags()
        return new_robot_path

    def build_obsidian_robot(self):
        new_robot_path = copy.deepcopy(self)
        new_robot_path.n_ore -= self.blueprint.obsidian_robot_cost_ore
        new_robot_path.n_clay -= self.blueprint.obsidian_robot_cost_clay
        new_robot_path.n_obsidian_robots += 1
        new_robot_path.reset_could_have_bought_flags()
        return new_robot_path

    def build_geode_robot(self):
        new_robot_path = copy.deepcopy(self)
        new_robot_path.n_ore -= self.blueprint.geode_robot_cost_ore
        new_robot_path.n_obsidian -= self.blueprint.geode_robot_cost_obsidian
        new_robot_path.n_geode_robots += 1
        new_robot_path.reset_could_have_bought_flags()
        return new_robot_path



def solve_first_part(blueprint_list, n_minutes_to_consider=N_MINUTES, print_result=True):
    
    most_geodes_by_blueprint = [None for _ in range(len(blueprint_list))]
    total_quality_level = 0
    for blueprint_id, blueprint in enumerate(blueprint_list, start=1):

        most_geode_number = 0
        robot_path_list = [RobotBuildingPath(blueprint,n_minutes_to_consider)]
        while len(robot_path_list) != 0:
            current_robot_path = robot_path_list.pop()        

            can_buy_ore_robot = current_robot_path.n_ore >= blueprint.ore_robot_cost_ore and current_robot_path.n_ore_robots < current_robot_path.n_max_ore_robots
            can_buy_clay_robot = current_robot_path.n_ore >= blueprint.clay_robot_cost_ore and current_robot_path.n_clay_robots < current_robot_path.n_max_clay_robots
            can_buy_obsidian_robot = current_robot_path.n_ore >= blueprint.obsidian_robot_cost_ore and current_robot_path.n_clay >= blueprint.obsidian_robot_cost_clay and current_robot_path.n_obsidian_robots < current_robot_path.n_max_obsidian_robots
            can_buy_geode_robot = current_robot_path.n_ore >= blueprint.geode_robot_cost_ore and current_robot_path.n_obsidian >= blueprint.geode_robot_cost_obsidian

            current_robot_path.collect()

            n_geode_ideal = current_robot_path.ideal_path_estimation()
            if n_geode_ideal < most_geode_number:
                continue

            if current_robot_path.n_geode > most_geode_number:
                most_geode_number = current_robot_path.n_geode
            
            if current_robot_path.n_minutes_left == 0:
                # it does not matter what is built, there is no time to use it
                continue

            # the nothing_done_robot_path is appended first, as in principle will be less efficient than paths where something is built
            if can_buy_geode_robot == False:
                # it is not possible that not doing anything is better than building a geode robot, so this is only executed if no geode robot can be built
                nothing_done_robot_path = current_robot_path
                robot_path_list.append(nothing_done_robot_path)

            if can_buy_ore_robot and current_robot_path.could_have_bought_ore_robot_but_did_nothing == False:
                robot_path_list.append(current_robot_path.build_ore_robot())
            
            if can_buy_clay_robot and current_robot_path.could_have_bought_clay_robot_but_did_nothing == False:
                robot_path_list.append(current_robot_path.build_clay_robot())
            
            if can_buy_obsidian_robot and current_robot_path.could_have_bought_obsidian_robot_but_did_nothing == False:
                robot_path_list.append(current_robot_path.build_obsidian_robot())

            if can_buy_geode_robot:
                robot_path_list.append(current_robot_path.build_geode_robot())
            
            else:
                # update values of the nothing_done_robot_path. It has been already appended to the robot_path_list
                nothing_done_robot_path.could_have_bought_ore_robot_but_did_nothing = can_buy_ore_robot
                nothing_done_robot_path.could_have_bought_clay_robot_but_did_nothing = can_buy_clay_robot
                nothing_done_robot_path.could_have_bought_obsidian_robot_but_did_nothing = can_buy_obsidian_robot


        most_geodes_by_blueprint[blueprint_id-1] = most_geode_number
        total_quality_level += most_geode_number * blueprint_id
    
     
    if print_result==True:
        print("With {} minutes, the total quality level is {}. The largest number of geodes is {} for Blueprint 1".format(N_MINUTES, total_quality_level, most_geodes_by_blueprint[0]), end="")
        for blueprint_id, most_geode in enumerate(most_geodes_by_blueprint[1:-1], start=2):
            print(", {} for Blueprint {}".format(most_geode, blueprint_id), end="")
        print(" and {} for Blueprint {}".format(most_geodes_by_blueprint[-1], len(most_geodes_by_blueprint)))

    return most_geodes_by_blueprint


def solve_second_part(blueprint_list):
    most_geodes_by_blueprint = solve_first_part(blueprint_list[:N_BLUEPRINTS_TO_CONSIDER_PART2], n_minutes_to_consider=N_MINUTES_PART2, print_result=False)

    geode_multiplication = np.prod(most_geodes_by_blueprint)

    print("Considering only the {} first blueprints and having {} minutes, the product of the maximum attainable number of geodes for each blueprint is {}. The largest number of geodes is {} for Blueprint 1".format(N_BLUEPRINTS_TO_CONSIDER_PART2, N_MINUTES_PART2, geode_multiplication, most_geodes_by_blueprint[0]),end="")
    for blueprint_id, most_geode in enumerate(most_geodes_by_blueprint[1:-1], start=2):
        print(", {} for Blueprint {}".format(most_geode, blueprint_id), end="")
    print(" and {} for Blueprint {}".format(most_geodes_by_blueprint[-1], len(most_geodes_by_blueprint)))
        

def main(file_name): 
    with open(file_name) as file:
        lines = file.read().splitlines()

    blueprint_list = parse_puzzle_file(lines)

    solve_first_part(blueprint_list)
    solve_second_part(blueprint_list)


if __name__ == "__main__":
    main(parse_file_name())