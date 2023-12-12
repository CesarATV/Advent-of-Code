const PUZZLE_INPUT_FILE_NAME: &str = "puzzle_inputs/day1.txt";
const PUZZLE_EXAMPLE_INPUT_FILE_NAME: &str = "puzzle_inputs/day1_example.txt";

const SLIDING_WINDOW_SIZE: usize = 3;

fn solve_first_part(mut lines: core::str::Lines) {
    let mut n_depth_increases: i32 = 0;
    let mut past_number: u32 = lines.next().expect("Empty input file").parse::<u32>().expect("The lines contain a non-number character");

    lines.for_each(|line: &str| {   
        let current_number: u32 = line.parse::<u32>().expect("Not a number");
        if past_number < current_number {
            n_depth_increases += 1;
        }
        
        past_number = current_number;
    });
    println!("The deep increases {n_depth_increases} times");
}


fn solve_second_part(lines: core::str::Lines) {
    let lines_vector: Vec<u32> = lines.map(|x: &str| x.parse::<u32>().expect("The lines contain a non-number character")).collect();

    let mut n_depth_increases: i32 = 0;
    ( 0..(lines_vector.len()-SLIDING_WINDOW_SIZE) ).for_each(|idx: usize| {
        if lines_vector[idx] < lines_vector[idx+SLIDING_WINDOW_SIZE] {
            n_depth_increases += 1;
        }
    });

    println!("The deep increases {n_depth_increases} times when considering a sliding window of size {SLIDING_WINDOW_SIZE}");
}


fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file_contents: String = match std::env::args().count() {
        1 => std::fs::read_to_string(PUZZLE_INPUT_FILE_NAME)?,
        2 => std::fs::read_to_string(PUZZLE_EXAMPLE_INPUT_FILE_NAME)?,
        _ => std::fs::read_to_string(std::env::args().nth(2).unwrap())?
    };
    let file_contents: &str = file_contents.trim_end(); // remove last empty lines, if any. They do not add information and can cause confusion
    
    solve_first_part(file_contents.lines());
    solve_second_part(file_contents.lines());

    Ok(())
}
