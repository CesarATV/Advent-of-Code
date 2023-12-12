const PUZZLE_INPUT_FILE_NAME: &str = "puzzle_inputs/day9.txt";
const PUZZLE_EXAMPLE_INPUT_FILE_NAME: &str = "puzzle_inputs/day9_example.txt";


const NON_BASIN_HEIGHT: u32 = 9;
const N_LARGER_BASINS: usize = 3;

fn parse_puzzle_file(file_contents: &str) -> (Vec<u32>, usize, usize) {
    let heightmap: Vec<u32> = file_contents.chars().filter_map(|c: char| c.to_digit(10)).collect();

    let n_cols: usize = file_contents.lines().next().expect("Empty input file").len();
    let n_rows: usize = file_contents.lines().count();

    (heightmap, n_rows, n_cols)
}


fn solve_first_part(heightmap: &Vec<u32>, n_rows: usize, n_cols: usize) {
    // this function will visit every single point in the heightmap and check its heigh in comparison to its neighbours. If a neighbour is considered taller or equal in size, this will be added to a hashmap in order to not be visited again, as this neighbour cannot be a lowerpoint. If all neighbours are taller, the current point is consiered a low point and its risk level is counted

    let mut visited_positions: std::collections::HashSet<usize> = std::collections::HashSet::new();
    let mut sum_of_risk_levels: u32 = 0;
    for heigthmap_position in 0..heightmap.len() {

        if visited_positions.insert(heigthmap_position) == false {
            continue;
        }

        let row_n: usize = heigthmap_position / n_cols;
        let column_n: usize = heigthmap_position % n_cols;

        // check up, down, left and right positions of every point. If the point is in a border, only visit its available neighbour points 
        
        if row_n > 0 {
            let up_position: usize = heigthmap_position - n_cols;
            if heightmap[heigthmap_position] >= heightmap[up_position] {
                continue;
            } else {
                visited_positions.insert(up_position);
            }
        }

        if row_n < (n_rows-1) {
            let down_position: usize = heigthmap_position + n_cols;
            if heightmap[heigthmap_position] >= heightmap[down_position] {
                continue;
            } else {
                visited_positions.insert(down_position);
            }
        }

        if column_n > 0 {
            let left_position: usize = heigthmap_position - 1;
            if heightmap[heigthmap_position] >= heightmap[left_position] {
                continue;
            } else {
                visited_positions.insert(left_position);
            }
        }

        if column_n < (n_cols-1) {
            let right_position: usize = heigthmap_position + 1;
            if heightmap[heigthmap_position] >= heightmap[right_position] {
                continue;
            } else {
                visited_positions.insert(right_position);
            }
        }

        sum_of_risk_levels += heightmap[heigthmap_position] + 1;
    }

    println!("The sum of the risk levels of all low points is {sum_of_risk_levels}")
}


fn solve_second_part(heightmap: Vec<u32>, n_rows: usize, n_cols: usize) {
    // this function will visit every single point in the heightmap as long as its height is not NON_BASIN_HEIGHT. It will visit also its neighbours that do not have NON_BASIN_HEIGHT, and the neighbours without NON_BASIN_HEIGHT of these. All these not NON_BASIN_HEIGHT neighbours will be counted to compute the basin size. Once a basin runs out of neighbours, the function keeps continues checking every remaining point in the heightmap trying to find other basins. Once a position has been checked, it is added to visited_positions in order to not be checked again.

    let mut larger_basins: [u32; N_LARGER_BASINS] = [0; N_LARGER_BASINS];
    let mut visited_positions: std::collections::HashSet<usize> = std::collections::HashSet::new();
    let mut current_basin: Vec<usize> = Vec::new();
    for heigthmap_position in 0..heightmap.len() {

        if visited_positions.insert(heigthmap_position) == false || heightmap[heigthmap_position] == NON_BASIN_HEIGHT {
            continue;
        }

        let mut current_basin_size: u32 = 0;
        current_basin.push(heigthmap_position);
        while current_basin.len() != 0 {
            let current_position: usize = current_basin.pop().unwrap();
            current_basin_size += 1;

            let row_n: usize = current_position / n_cols;
            let column_n: usize = current_position % n_cols;
            
            // check up, down, left and right positions of every point. If the point is in a border, only visit its available neighbour points 

            if row_n > 0 {
                let up_position: usize = current_position - n_cols;
                if visited_positions.insert(up_position) == true {
                    if heightmap[up_position] != NON_BASIN_HEIGHT  {
                        current_basin.push(up_position);
                    }
                }
            }
    
            if row_n < (n_rows-1) {
                let down_position: usize = current_position + n_cols;
                if visited_positions.insert(down_position) == true {
                    if heightmap[down_position] != NON_BASIN_HEIGHT  {
                        current_basin.push(down_position);
                    }
                }
            }
    
            if column_n > 0 {
                let left_position: usize = current_position - 1;
                if visited_positions.insert(left_position) == true {
                    if heightmap[left_position] != NON_BASIN_HEIGHT  {
                        current_basin.push(left_position);
                    }
                }
            }
    
            if column_n < (n_cols-1) {
                let right_position: usize = current_position + 1;
                if visited_positions.insert(right_position) == true {
                    if heightmap[right_position] != NON_BASIN_HEIGHT  {
                        current_basin.push(right_position);
                    }
                }
            }
        }

        if larger_basins[0] < current_basin_size {
            larger_basins[0] = current_basin_size;
            larger_basins.sort(); // place smallest size at the first position of the array
        }
    }

    let multiplication_of_larger_basins: u32 = larger_basins.iter().product();
    
    print!("The multiplication of the {N_LARGER_BASINS} larger basins is {multiplication_of_larger_basins}. Their sizes are {}", larger_basins[0]);
    (1..(N_LARGER_BASINS-1)).for_each(|idx: usize| {
        print!(", {}", larger_basins[idx]);
    });
    println!(" and {}", larger_basins.last().unwrap());
}


fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file_contents: String = match std::env::args().count() {
        1 => std::fs::read_to_string(PUZZLE_INPUT_FILE_NAME)?,
        2 => std::fs::read_to_string(PUZZLE_EXAMPLE_INPUT_FILE_NAME)?,
        _ => std::fs::read_to_string(std::env::args().nth(2).unwrap())?
    };
    let file_contents: &str = file_contents.trim_end(); // remove last empty lines, if any. They do not add information and can cause confusion
    
    let (heightmap, n_rows, n_cols): (Vec<u32>, usize, usize) = parse_puzzle_file(file_contents);
    
    solve_first_part(&heightmap, n_rows, n_cols);
    solve_second_part(heightmap, n_rows, n_cols);

    Ok(())
}