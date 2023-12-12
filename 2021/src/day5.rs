const PUZZLE_INPUT_FILE_NAME: &str = "puzzle_inputs/day5.txt";
const PUZZLE_EXAMPLE_INPUT_FILE_NAME: &str = "puzzle_inputs/day5_example.txt";


fn parse_puzzle_line(line: &str) -> (i32, i32, i32, i32) {
    let mut split_line: std::str::SplitWhitespace = line.split_whitespace();

    let mut begin_coordinates: std::str::Split<&str> = split_line.next().expect("Incorrect file format").split(",");
    let x_begin: i32 = begin_coordinates.next().expect("Incorrect file format").parse::<i32>().expect("Not a number");
    let y_begin: i32 = begin_coordinates.next().expect("Incorrect file format").parse::<i32>().expect("Not a number");
        
    let mut end_coordinates: std::str::Split<&str> = split_line.skip(1).next().expect("Incorrect file format").split(",");
    let x_end: i32 = end_coordinates.next().expect("Incorrect file format").parse::<i32>().expect("Not a number");
    let y_end: i32 = end_coordinates.next().expect("Incorrect file format").parse::<i32>().expect("Not a number");

    (x_begin, y_begin, x_end, y_end)
}


fn solve_first_part(lines: core::str::Lines) {
    let mut position_passes: std::collections::HashMap<(i32, i32), u32> = std::collections::HashMap::new(); // the tuple stores (x,y) coordinates in that order

    lines.for_each(|line: &str| {
        
        let (x_begin, y_begin, x_end, y_end): (i32, i32, i32, i32) = parse_puzzle_line(line);

        if x_begin == x_end {
            let y_iter: std::ops::RangeInclusive<i32> = {
                if y_begin > y_end {
                    y_end..=y_begin
                } else {
                    y_begin..=y_end
                }
            };

            y_iter.for_each(|y_idx: i32| {
                let n_passes: &mut u32 = position_passes.entry((x_begin, y_idx)).or_insert(0);
                *n_passes += 1; 
            });
        }
        
        else if y_begin == y_end {
            let x_iter: std::ops::RangeInclusive<i32> = {
                if x_begin > x_end {
                    x_end..=x_begin
                } else {
                    x_begin..=x_end
                }
            };

            x_iter.for_each(|x_idx: i32| {
                let n_passes: &mut u32 = position_passes.entry((x_idx, y_begin)).or_insert(0);
                *n_passes += 1; 
            });
        }
    });

    let n_overlaps: usize = position_passes.values().into_iter().filter(|&n_passes| *n_passes > 1).count();

    println!("Considering only horizontal and vertical lines there are {n_overlaps} overlaps");
}


fn solve_second_part(lines: core::str::Lines) {
    let mut position_passes: std::collections::HashMap<(i32, i32), u32> = std::collections::HashMap::new(); // the tuple stores (x,y) coordinates in that order

    lines.for_each(|line: &str| {
        let (x_begin, y_begin, x_end, y_end): (i32, i32, i32, i32) = parse_puzzle_line(line);

        if x_begin == x_end { // vertical line
            let y_iter: std::ops::RangeInclusive<i32> = {
                if y_begin > y_end {
                    y_end..=y_begin
                } else {
                    y_begin..=y_end
                }
            };

            y_iter.for_each(|y_idx: i32| {
                let n_passes: &mut u32 = position_passes.entry((x_begin, y_idx)).or_insert(0);
                *n_passes += 1; 
            });
        }
        
        else if y_begin == y_end { // horizontal line
            let x_iter: std::ops::RangeInclusive<i32> = {
                if x_begin > x_end {
                    x_end..=x_begin
                } else {
                    x_begin..=x_end
                }
            };

            x_iter.for_each(|x_idx: i32| {
                let n_passes: &mut u32 = position_passes.entry((x_idx, y_begin)).or_insert(0);
                *n_passes += 1; 
            });
        }

        else { // diagonal line
            let (x_step, line_length): (i32, i32) = {
                if x_begin > x_end {
                    (-1, x_begin-x_end)
                } else {
                    (1, x_end-x_begin)
                }
            };

            let y_step: i32 = {
                if y_begin > y_end {
                    -1
                } else {
                    1
                }
            };

            let mut x_idx: i32 = x_begin;
            let mut y_idx: i32 = y_begin;
            for _ in 0..=line_length {
                let n_passes: &mut u32 = position_passes.entry((x_idx, y_idx)).or_insert(0);
                *n_passes += 1;
                x_idx += x_step;
                y_idx += y_step;
            }
        }
    });

    let n_overlaps: usize = position_passes.values().into_iter().filter(|&n_passes| *n_passes > 1).count();

    println!("Considering all lines there are {n_overlaps} overlaps");
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