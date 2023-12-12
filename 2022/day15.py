'''
For the second part, the amount of cells in which to search for a beacon is very large, a layout of 4000000 by 4000000.

A solution for the problem could be to see which cells are iluminated by every beacon. However, the given layout requires to create a 4000000 by 4000000 array, which requires an absurd amount of memory (over the terabyte if ignoring possible compression techniques), and an also absurd amount of time to iterate through it.
A more appropiate solution without the need of storage is to check if every cell is iluminated by a beacon, although it also suffers from the problem of absurdly high iteration times.
To avoid such a long iteration and taking advantage of the fact that only one cell in the whole layout is going to be non-iluminated, it is possible to iterate over only a set of cells more likely to have the target beacon. These cells are the cells immediately after the range of a beacon (so, the borders of the area iluminated by the beacon). In such a compressed layout, the target beacon has to be squeezed between two sensors, and therefore in these borders.
'''


import argparse
import numpy as np
from dataclasses import dataclass

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day15.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day15_example.txt"


ROW_OF_INTEREST = 2000000
ROW_OF_INTEREST_EXAMPLE_FILE = 10


@dataclass
class Sensor:
    x: int
    y: int
    range: int
    idx: int


X_TUNING_FREQUENCY = 4000000
MINIMUM_COORDINATE_POSITION = 0
MAXIMUM_COORDINATE_POSITION = 4000000
MAXIMUM_COORDINATE_POSITION_EXAMPLE_FILE = 20


def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 15: Beacon Exclusion Zone")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    parser.add_argument("-e", "--example", dest="using_a_example_file", action="store_true", help="if a file path has been given, use this argument if that file path corresponds to an example file. This puzzle uses different contants (different row of interest and maximum coordinate position) for each file type")
    args = parser.parse_args()
    if args.file_name == []:
        using_a_example_file = False
        return PUZZLE_INPUT_FILE_NAME, using_a_example_file
    elif len(args.file_name) == 1:
        using_a_example_file = True
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME, using_a_example_file
    else:
        return args.file_name[1], args.using_a_example_file


def manhattan_distance(x_pos1,y_pos1,x_pos2,y_pos2):
    x_distance = abs(x_pos1 - x_pos2)
    y_distance = abs(y_pos1 - y_pos2)
    return x_distance + y_distance


def solve_first_part(lines, row_of_interest=ROW_OF_INTEREST):
    x_without_beacon = set()
    x_with_beacon = set()

    for line in lines:
        split_line = line.split(" ")
        sensor_x = int(split_line[2][2:-1])
        sensor_y = int(split_line[3][2:-1])

        beacon_x = int(split_line[8][2:-1])
        beacon_y = int(split_line[9][2:])
        if beacon_y == row_of_interest:
            x_with_beacon.add(beacon_x)

        sensor_range = manhattan_distance(sensor_x, sensor_y, beacon_x, beacon_y)

        if (sensor_y + sensor_range) >= row_of_interest:
            distance_to_interest = abs(sensor_y - row_of_interest)
            lateral_x_extension = sensor_range-distance_to_interest
            for blocked_x in range(sensor_x - lateral_x_extension, sensor_x + lateral_x_extension +1):
                x_without_beacon.add(blocked_x)

    print("Row", row_of_interest, "can contain up to", len(x_without_beacon) - len(x_with_beacon), "beacons")



def check_if_it_can_be_a_beacon(point_x, point_y, subsensor_list):
    can_it_be_a_beacon = True
    for sensor in subsensor_list:
        sensor_to_point_distance = manhattan_distance(point_x,point_y,sensor.x,sensor.y)
        if sensor_to_point_distance <= sensor.range:
            can_it_be_a_beacon = False
            break
    return can_it_be_a_beacon


def check_sensing_borders(sensor_x, sensor_y, sensor_range,sensor_idx, sensor_list, maximum_coordinate_position=MAXIMUM_COORDINATE_POSITION):
    subsensor_list = sensor_list[:sensor_idx] + sensor_list[sensor_idx+1:] # do not iterate over the beacon that generates the borders used in this function
    
    for y_idx in range(-sensor_range,sensor_range+1):
        border_y = sensor_y + y_idx
        if border_y >= MINIMUM_COORDINATE_POSITION and border_y <= maximum_coordinate_position:
            pre_x_idx = sensor_range - y_idx*np.sign(y_idx) + 1

            if pre_x_idx != 0:
                x_idxs = [pre_x_idx, -pre_x_idx]
            else:
                x_idxs = [pre_x_idx]

            for x_idx in x_idxs:
                border_x = sensor_x + x_idx
                if border_x >= MINIMUM_COORDINATE_POSITION and border_x <= maximum_coordinate_position:
                    can_it_be_a_beacon = check_if_it_can_be_a_beacon(border_x, border_y, subsensor_list)
                    if can_it_be_a_beacon == True:
                        return can_it_be_a_beacon, border_x, border_y

    can_it_be_a_beacon = False
    return can_it_be_a_beacon, -1, -1

    
def solve_second_part(lines, maximum_coordinate_position=MAXIMUM_COORDINATE_POSITION):
    sensor_list = []
    for idx, line in enumerate(lines):
        split_line = line.split(" ")
        sensor_x = int(split_line[2][2:-1])
        sensor_y = int(split_line[3][2:-1])

        beacon_x = int(split_line[8][2:-1])
        beacon_y = int(split_line[9][2:])

        sensor_range = manhattan_distance(sensor_x,sensor_y,beacon_x,beacon_y)

        sensor = Sensor(sensor_x,sensor_y,sensor_range,idx)
        sensor_list.append(sensor)


    for sensor in sensor_list:
        beacon_found, target_beacon_x, target_beacon_y = check_sensing_borders(sensor.x, sensor.y, sensor.range, sensor.idx, sensor_list, maximum_coordinate_position)
        if beacon_found == True:
            break

    if beacon_found == True:
        tuning_frequency = target_beacon_x * X_TUNING_FREQUENCY + target_beacon_y
        print("Beacon found at [{},{}] with a tuning frequency of {}".format(target_beacon_x,target_beacon_y,tuning_frequency))

    else:
        print("Beacon not found. This option should never happen...Is the argument parsing option to use the parameters that correspond to example file, or not, correctly set (try --help)?")


def main(file_name, using_example_file=False):    
    with open(file_name) as file:
        lines = file.read().splitlines()
    while lines[-1] == "": # remove last empty lines, if any. They do not add information and can cause confusion
        lines.pop()

    if using_example_file==False:
        row_of_interest = ROW_OF_INTEREST
        maximum_coordinate_position = MAXIMUM_COORDINATE_POSITION
    else:
        row_of_interest = ROW_OF_INTEREST_EXAMPLE_FILE
        maximum_coordinate_position = MAXIMUM_COORDINATE_POSITION_EXAMPLE_FILE

    solve_first_part(lines, row_of_interest)
    solve_second_part(lines, maximum_coordinate_position)


if __name__ == "__main__":
    main(*parse_file_name())

