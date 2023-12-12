import argparse
import numpy as np

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day8.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day8_example.txt"

def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 8: Treetop Tree House")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]


def parse_puzzle_file(lines):
    n_rows = len(lines)
    n_cols = len(lines[0])

    tree_grid = np.zeros([n_rows,n_cols])
    for idx, line in enumerate(lines):
        tree_grid[idx,:] = [int(character) for character in line]

    return tree_grid


def solve_first_part(tree_grid):
    n_rows, n_cols = tree_grid.shape

    visible_trees = n_rows*2 + (n_cols-2)*2 # trees in the borders
    for col_idx in range(1,n_cols-1):
        for row_idx in range(1,n_rows-1):
            tree_size = tree_grid[row_idx,col_idx]
            
            upper_trees = tree_grid[:row_idx,col_idx]
            if np.max(upper_trees) < tree_size:
                visible_trees += 1
                continue
            lower_trees = tree_grid[row_idx+1:,col_idx]
            if np.max(lower_trees) < tree_size:
                visible_trees += 1
                continue
            left_trees = tree_grid[row_idx,:col_idx]
            if np.max(left_trees) < tree_size:
                visible_trees += 1
                continue
            right_trees = tree_grid[row_idx,col_idx+1:]
            if np.max(right_trees) < tree_size:
                visible_trees += 1
                continue
        
    print("The are", visible_trees, "visible trees")
 

def solve_second_part(tree_grid):
    ''' Note that the trees in the borders/edges are ignored, as at least one of their scenic scores is 0 (no trees to be seen), making their total scenic score 0 '''

    n_rows, n_cols = tree_grid.shape
    highest_scenic_score = 0
    for col_idx in range(1,n_cols-1):
        for row_idx in range(1,n_rows-1):
            tree_size = tree_grid[row_idx,col_idx]
            
            upper_trees = np.flip(tree_grid[:row_idx,col_idx])
            upper_limit = np.max(upper_trees) >= tree_size
            if upper_limit:
                current_scenic_score = np.argwhere(upper_trees >= tree_size)[0]+1
            else:
                current_scenic_score = len(upper_trees)
                
            lower_trees = tree_grid[row_idx+1:,col_idx]
            lower_limit = np.max(lower_trees) >= tree_size
            if lower_limit:
                current_scenic_score *= np.argwhere(lower_trees >= tree_size)[0]+1
            else:
                current_scenic_score *= len(lower_trees)
                
            left_trees = np.flip(tree_grid[row_idx,:col_idx])
            left_limit = np.max(left_trees) >= tree_size
            if left_limit:
                current_scenic_score *= np.argwhere(left_trees >= tree_size)[0]+1
            else:
                current_scenic_score *= len(left_trees)
                
            right_trees = tree_grid[row_idx,col_idx+1:]
            right_limit = np.max(right_trees) >= tree_size
            if right_limit:
                current_scenic_score *= np.argwhere(right_trees >= tree_size)[0]+1
            else:
                current_scenic_score *= len(right_trees)
        
            if highest_scenic_score < current_scenic_score:
                highest_scenic_score = current_scenic_score[0]
            
    print("The highest scenic score is", highest_scenic_score)
        

def main(file_name): 
    with open(file_name) as file:
        lines = file.read().splitlines()
    while lines[-1] == "": # remove last empty lines, if any. They do not add information and can cause confusion
        lines.pop()

    tree_grid = parse_puzzle_file(lines)
    solve_first_part(tree_grid)
    solve_second_part(tree_grid)


if __name__ == "__main__":
    main(parse_file_name())
