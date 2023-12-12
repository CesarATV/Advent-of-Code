const PUZZLE_INPUT_FILE_NAME: &str = "puzzle_inputs/day6.txt";
const PUZZLE_EXAMPLE_INPUT_FILE_NAME: &str = "puzzle_inputs/day6_example.txt";

const N_DAYS_PART1: usize = 80;
const N_DAYS_PART2: usize = 256;

const NEW_BORN_TIMER: usize = 8 + 1;
const RESET_TIMER: usize = 6 + 1;
const LONGEST_TIMER: usize = if NEW_BORN_TIMER > RESET_TIMER {NEW_BORN_TIMER} else {RESET_TIMER};
const SMALLEST_TIMER: usize = if NEW_BORN_TIMER > RESET_TIMER {RESET_TIMER} else {NEW_BORN_TIMER};


fn solve_first_part(file_contents: &str, n_days: usize) {
    let fishes_timer_lines: Vec<usize> = file_contents.split(",").map(|x: &str| x.parse::<usize>().expect("Not a number in file lines")).collect();

    let mut fish_array: [usize; LONGEST_TIMER] = [0; LONGEST_TIMER]; // the array contains the number of fish distributed by their reproduction period: The position that a number of fish occupy in the array represent the time they have left to procreate
    (0..LONGEST_TIMER).for_each(|fisht_timer_idx: usize| {
        fish_array[fisht_timer_idx] = fishes_timer_lines.iter().filter(|&x: &&usize| *x == fisht_timer_idx ).count();
    });


    // instead of moving fish_array circularly, representing the timers of the fish passing by, two variables will be used to keep track of the indexes of the array, so the time left to procreate is actually represented by these indexes
    let mut resetted_end_index: usize = SMALLEST_TIMER; // indexes the fish that have just procreated
    let mut resetted_beginning_index: usize = 0; // indexes the fish that are about to procreate
    for _ in 0..n_days
    {
        // Once the fish have reproduced, their offspring will have the timer that corresponds the index that represents the end of the array, while their parents will have a timer that corresponds to the index that represents the resetting of the reproduction
        fish_array[resetted_end_index] += fish_array[resetted_beginning_index]; 
        resetted_end_index += 1;
        resetted_end_index %= LONGEST_TIMER;
        resetted_beginning_index += 1;
        resetted_beginning_index %= LONGEST_TIMER;
    }

    let n_fish: usize = fish_array.iter().sum();
    println!("After {n_days} days there would be {n_fish} lanterfish");
}


fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file_contents: String = match std::env::args().count() {
        1 => std::fs::read_to_string(PUZZLE_INPUT_FILE_NAME)?,
        2 => std::fs::read_to_string(PUZZLE_EXAMPLE_INPUT_FILE_NAME)?,
        _ => std::fs::read_to_string(std::env::args().nth(2).unwrap())?
    };
    let file_contents: &str = file_contents.trim_end(); // remove last empty lines, if any. They do not add information and can cause confusion
    
    solve_first_part(file_contents, N_DAYS_PART1);

    let solve_second_part = solve_first_part;
    solve_second_part(file_contents, N_DAYS_PART2);

    Ok(())
}