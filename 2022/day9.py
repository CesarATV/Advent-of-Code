import argparse
import numpy as np

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day9.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day9_example.txt"

ROPE_BODY_LENGTH = 10

def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 9: Rope Bridge")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]


def solve_first_part(lines):
    base_positions = set()
    base_positions.add((0,0))
    current_head = [0,0]
    current_tail = [0,0]
    for line in lines:
        movement = line[0]
        distance = int(line[2:])
        
        if movement == "R":
            current_head[0] += distance
        elif movement == "L":
            current_head[0] -= distance
        elif movement == "U":
            current_head[1] += distance
        elif movement == "D":
            current_head[1] -= distance
        
        x_distance = current_head[0] - current_tail[0]
        y_distance = current_head[1] - current_tail[1]

        x_distance_abs = abs(x_distance)
        y_distance_abs = abs(y_distance)
        if x_distance == 0:
            pass
        elif y_distance == 0:
            pass
        elif x_distance_abs != y_distance_abs:
            if x_distance_abs > y_distance_abs and y_distance != 0:
                current_tail[1] = current_head[1]
            elif x_distance_abs < y_distance_abs and x_distance != 0:
                current_tail[0] = current_head[0]

        for _x_steps in range( abs(x_distance -1*np.sign(x_distance)) ):
            current_tail[0] += 1*np.sign(x_distance)
            base_positions.add(tuple(current_tail))  

        for _y_steps in range( abs(y_distance -1*np.sign(y_distance)) ):
            current_tail[1] += 1*np.sign(y_distance)
            base_positions.add(tuple(current_tail))
            
    print("The tail visits", len(base_positions), "positions at least once")
 

def tail_step(temp_head, temp_tail, track_positions, base_positions):
    x_distance = temp_head[0] - temp_tail[0]
    y_distance = temp_head[1] - temp_tail[1]
    x_distance_abs = abs(x_distance)
    y_distance_abs = abs(y_distance)

    if not (x_distance_abs <= 1 and y_distance_abs <= 1):
        if x_distance_abs > y_distance_abs and y_distance != 0:
            temp_tail[0] += x_distance + -1*np.sign(x_distance)
            temp_tail[1] = temp_head[1]
        elif x_distance_abs < y_distance_abs and x_distance != 0:
            temp_tail[0] = temp_head[0]
            temp_tail[1] += y_distance + -1*np.sign(y_distance)

        else:
            temp_tail[0] += x_distance + -1*np.sign(x_distance)
            temp_tail[1] += y_distance + -1*np.sign(y_distance)
    
        if track_positions:
            base_positions.add(tuple(temp_tail))

    return temp_tail
    

def solve_second_part(lines):
    '''
    The code was slightly changed from the past part. It predicted the movement of the tail without looking at the individual steps of the head in each cell, just at its final position for each movement direction. When adding more knots to the rope, it seems that it is no longer possible to predict the movement of each subsequent knot just by looking at the final position of each knot head (in many cases, as with the example given in the page, it is still possible). As a result, the code was changed to move each knot head and its subsecuent knot tail one cell at a time
    '''

    base_positions = set()
    base_positions.add((0,0))
    count = 0
    rope_body = [[0,0] for _ in range(ROPE_BODY_LENGTH)]
    for line in lines:
        direction = line[0]
        distance = int(line[2:])
        
        if direction == "R":
            movement_distance = [1,0]  
        elif direction == "L":
            movement_distance = [-1,0]
        elif direction == "U":
            movement_distance = [0,1]
        elif direction == "D":
            movement_distance = [0,-1]
        
        for _ in range(abs(distance)):
            rope_body[0][0] +=  movement_distance[0]
            rope_body[0][1] +=  movement_distance[1]
            for idx in range(1,ROPE_BODY_LENGTH):
                rope_body[idx] = tail_step(rope_body[idx-1],rope_body[idx], idx == (ROPE_BODY_LENGTH-1), base_positions)
        count +=1
            
    print("With a rope length of", ROPE_BODY_LENGTH, "the tail visits", len(base_positions), "positions at least once")
        

def main(file_name): 
    with open(file_name) as file:
        lines = file.read().splitlines()
    while lines[-1] == "": # remove last empty lines, if any. They do not add information and can cause confusion
        lines.pop()

    solve_first_part(lines)
    solve_second_part(lines)


if __name__ == "__main__":
    main(parse_file_name())