const PUZZLE_INPUT_FILE_NAME: &str = "puzzle_inputs/day2.txt";
const PUZZLE_EXAMPLE_INPUT_FILE_NAME: &str = "puzzle_inputs/day2_example.txt";


fn solve_first_part(lines: core::str::Lines) {
    let mut horizontal_position: i32 = 0;
    let mut depth: i32 = 0;
    lines.for_each(|line: &str| {
        let split_line: Vec<&str> = line.split_whitespace().collect::<Vec<_>>();
        match split_line[0] {
            "forward" => horizontal_position += split_line[1].parse::<i32>().expect("Not a number"),
            "down" => depth += split_line[1].parse::<i32>().expect("Not a number"),
            "up" => depth -= split_line[1].parse::<i32>().expect("Not a number"),
            &_ => panic!("File instructions not correct")
        }
    });

    println!("The instructions give an horizontal position of {horizontal_position} and a depth of {depth}, which multiplied together are {}", depth*horizontal_position);
}


fn solve_second_part(lines: core::str::Lines) {
    let mut horizontal_position: i32 = 0;
    let mut depth: i32 = 0;
    let mut aim: i32 = 0;
    lines.for_each(|line: &str| {
        let split_line: Vec<&str> = line.split_whitespace().collect::<Vec<_>>();
        match split_line[0] {
            "forward" => {
                horizontal_position += split_line[1].parse::<i32>().expect("Not a number");
                depth += aim * split_line[1].parse::<i32>().expect("Not a number");
            },
            "down" => aim += split_line[1].parse::<i32>().expect("Not a number"),
            "up" => aim -= split_line[1].parse::<i32>().expect("Not a number"),
            &_ => unreachable!("File instruction not correct")
        }
    });
    
    println!("With the new command interpretation, the instructions give an horizontal position of {horizontal_position} and a depth of {depth}, which multiplied together are {}", depth*horizontal_position);
}


fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file_contents: String = match std::env::args().count() {
        1 => std::fs::read_to_string(PUZZLE_INPUT_FILE_NAME)?,
        2 => std::fs::read_to_string(PUZZLE_EXAMPLE_INPUT_FILE_NAME)?,
        _ => std::fs::read_to_string(std::env::args().nth(2).unwrap())?
    };
    let file_contents: &str = file_contents.trim_end();
    
    solve_first_part(file_contents.lines());
    solve_second_part(file_contents.lines());

    Ok(())
}