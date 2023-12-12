/// 
/// The implement solution works so in each step there is an iteration over all octopuses, increasing their energy and checking if they have flashed. If they have flashed, their adjacent octopuses indexes will be revisited, increasing their energy and checking if they have flashed, repeating the process until the step is over.
/// 
/// The functions to solve the first and the second part of the puzzle could be easily merged together as they share the same ure. They are left separated for clarity and because the program is fast enough.
/// 

const PUZZLE_INPUT_FILE_NAME: &str = "puzzle_inputs/day11.txt";
const PUZZLE_EXAMPLE_INPUT_FILE_NAME: &str = "puzzle_inputs/day11_example.txt";


const N_STEPS: u32 = 100;

const N_ROWS: usize = 10;
const N_COLUMNS: usize = 10;
const N_OCTOPUSES: usize = N_ROWS * N_COLUMNS;

const ENERGY_LEVEL_FOR_FLASHING: u8 = 9;


fn flash_adjacent_octopuses(idxs_octopuses_to_increase_energy: &mut Vec<usize>, octopus_idx: usize) {
    let row_idx: usize = octopus_idx / N_COLUMNS;
    let column_idx: usize = octopus_idx % N_COLUMNS;

    let is_it_a_uppmost_octopus: bool = row_idx == 0;
    let is_it_a_downmost_octopus: bool = row_idx == N_ROWS-1;
    let is_it_a_lefmost_octopus: bool = column_idx == 0;
    let is_it_a_rightmost_octopus: bool = column_idx == N_COLUMNS-1;
    
    // check if the current octopus is in any border of the grid. This is to avoid trying to flash over an octopus out of the grid

    if is_it_a_uppmost_octopus == false {
        idxs_octopuses_to_increase_energy.push(octopus_idx - N_COLUMNS); // octopus above
        if is_it_a_lefmost_octopus == false {
            idxs_octopuses_to_increase_energy.push(octopus_idx - N_COLUMNS - 1); // octopus in the up-left diagonal
        }
        if is_it_a_rightmost_octopus == false {
            idxs_octopuses_to_increase_energy.push(octopus_idx - N_COLUMNS + 1); // octopus in the up-right diagonal
        }
    }

    if is_it_a_downmost_octopus == false {
        idxs_octopuses_to_increase_energy.push(octopus_idx + N_COLUMNS); // octopus bellow
        if is_it_a_lefmost_octopus == false {
            idxs_octopuses_to_increase_energy.push(octopus_idx + N_COLUMNS - 1); // octopus in the down-left diagonal
        }
        if is_it_a_rightmost_octopus == false {
            idxs_octopuses_to_increase_energy.push(octopus_idx + N_COLUMNS + 1); // octopus in the down-right diagonal
        }
    }

    if is_it_a_lefmost_octopus == false {
        idxs_octopuses_to_increase_energy.push(octopus_idx - 1); // octopus to the left
    }

    if is_it_a_rightmost_octopus == false {
        idxs_octopuses_to_increase_energy.push(octopus_idx + 1); // octopus to the right
    }
}


fn solve_first_part(mut octopus_grid: [u8; N_OCTOPUSES])
{
    let mut idxs_octopuses_to_increase_energy: Vec<usize> = Vec::with_capacity(N_OCTOPUSES*2); // indexes of octopuses whose energy has to be increased in the current step. As every octopus can be visited at least 8 times (if all its neighbours flash), this capacity can become bigger
    let mut idxs_octopuses_to_restart_energy: Vec<usize> = Vec::with_capacity(N_OCTOPUSES); // indexes of octopuses that have flashed in a step 

    let mut n_flashes: usize = 0;
    (0..N_STEPS).for_each(|_step_n: u32| {

        idxs_octopuses_to_restart_energy.clear();
        idxs_octopuses_to_increase_energy.clear();
        idxs_octopuses_to_increase_energy.extend(0..N_OCTOPUSES);

        while let Some(octopus_idx) = idxs_octopuses_to_increase_energy.pop() {
            
            if octopus_grid[octopus_idx] <= ENERGY_LEVEL_FOR_FLASHING { // it is not strictly necessary to do this check, it only avoids to keep increasing the energy of octopuses whose energy level will anyway be set to 0 as they have flashed

                if octopus_grid[octopus_idx] == ENERGY_LEVEL_FOR_FLASHING {
                    flash_adjacent_octopuses(&mut idxs_octopuses_to_increase_energy, octopus_idx);
                    idxs_octopuses_to_restart_energy.push(octopus_idx);
                }

                octopus_grid[octopus_idx] += 1; // increase energy level
            }
        }

        n_flashes += idxs_octopuses_to_restart_energy.len();
        idxs_octopuses_to_restart_energy.iter().for_each(|idx: &usize| octopus_grid[*idx] = 0); // set to 0 the energy of all octopuses that have flashed
    });

    println!("After {N_STEPS} steps there have been {n_flashes} flashes");
}


/// This function works very similarly to solve_first_part but, instead of iterating a defined amount of steps, it loops until all octopuses have flashed at the same time
fn solve_second_part(mut octopus_grid: [u8; N_OCTOPUSES]) {
    let mut idxs_octopuses_to_increase_energy: Vec<usize> = Vec::with_capacity(N_OCTOPUSES*2); // indexes of octopuses whose energy has to be increased in the current step. As every octopus can be visited at least 8 times (if all its neighbours flash), this capacity can become bigger
    let mut idxs_octopuses_to_restart_energy: Vec<usize> = Vec::with_capacity(N_OCTOPUSES); // indexes of octopuses that have flashed in a step 

    let mut current_step_n: u32 = 0;
    loop {
        current_step_n += 1;

        idxs_octopuses_to_restart_energy.clear();
        idxs_octopuses_to_increase_energy.clear();
        idxs_octopuses_to_increase_energy.extend(0..N_OCTOPUSES);

        while let Some(octopus_idx) = idxs_octopuses_to_increase_energy.pop() {
            
            if octopus_grid[octopus_idx] <= ENERGY_LEVEL_FOR_FLASHING { // it is not strictly necessary to do this check, it only avoids to keep increasing the energy of octopuses whose energy level will be set to 0 as they have flashed

                if octopus_grid[octopus_idx] == ENERGY_LEVEL_FOR_FLASHING {
                    flash_adjacent_octopuses(&mut idxs_octopuses_to_increase_energy, octopus_idx);
                    idxs_octopuses_to_restart_energy.push(octopus_idx);
                }

                octopus_grid[octopus_idx] += 1; // increase energy level
            }
        }

        if idxs_octopuses_to_restart_energy.len() == N_OCTOPUSES {
            // all octopuses have flashed in this step
            break;
        }
        idxs_octopuses_to_restart_energy.iter().for_each(|idx: &usize| octopus_grid[*idx] = 0);
    };

    println!("All octopuses flash simultaneously in step number {current_step_n}");
}


fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file_contents: String = match std::env::args().count() {
        1 => std::fs::read_to_string(PUZZLE_INPUT_FILE_NAME)?,
        2 => std::fs::read_to_string(PUZZLE_EXAMPLE_INPUT_FILE_NAME)?,
        _ => std::fs::read_to_string(std::env::args().nth(2).unwrap())?
    };
    let file_contents: &str = file_contents.trim_end(); // remove last empty lines, if any. They do not add information and can cause confusion
    
    let octopus_grid: [u8; N_OCTOPUSES] = file_contents.chars().filter_map(|c: char| c.to_digit(10)).map(|x: u32| x.try_into().expect("An octopus in the input file has too high energy level")).collect::<Vec<u8>>().try_into().expect("Input file has a wrong number of octopuses"); // it is not really necessary for it to convert from u32 into u8, but it saves memory
    
    solve_first_part(octopus_grid);
    solve_second_part(octopus_grid);

    Ok(())
}