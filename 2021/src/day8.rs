const PUZZLE_INPUT_FILE_NAME: &str = "puzzle_inputs/day8.txt";
const PUZZLE_EXAMPLE_INPUT_FILE_NAME: &str = "puzzle_inputs/day8_example.txt";


const N_WHITESPACES_BEFORE_DIGIT_OUTPUT: usize = 11;
const N_SEGMENTS_OF_NUMBER_1: usize = 2;
const N_SEGMENTS_OF_NUMBER_4: usize = 4;
const N_SEGMENTS_OF_NUMBER_7: usize = 3;
const N_SEGMENTS_OF_NUMBER_8: usize = 7;

const N_SEGMENTS_OF_NUMBER_0_6_OR_9: usize = 6;
const N_SEGMENTS_OF_NUMBER_2_3_OR_5: usize = 5;
const N_SEGMENTS_OF_NUMBER_2_IN_NUMBER_4: usize = 2;
const N_DIGITS_IN_OUTPUT: usize = 4;


fn solve_first_part(lines: core::str::Lines) {
    let mut n_unique_segment_number_numbers: usize = 0;
    lines.for_each(|line: &str| {
        n_unique_segment_number_numbers += line.split_whitespace().skip(N_WHITESPACES_BEFORE_DIGIT_OUTPUT).filter(|x: &&str| matches!(x.len(), N_SEGMENTS_OF_NUMBER_1 | N_SEGMENTS_OF_NUMBER_4 | N_SEGMENTS_OF_NUMBER_7 | N_SEGMENTS_OF_NUMBER_8) ).count(); // if any of the output segments has a length of 2, 3, 4 or 7, it will be a number with a unique number of segments
    });
    
    println!("Digits 1, 4, 7 or 8 appear a total of {n_unique_segment_number_numbers} times");
}


fn solve_second_part(lines: core::str::Lines) {
    let mut output_values_addition: u32 = 0;
    lines.for_each(|line: &str| {

        // all possible digits in the output can be deduced knowing the amount of segments they have, and knowing the segments of digits 1, 4 and 7. The output digits will contain all or only part of these three digits with unique number of segments
        let segments_of_digit_1: &str = line.split_whitespace().find(|x: &&str| x.len() == N_SEGMENTS_OF_NUMBER_1).unwrap();
        let segments_of_digit_4: &str = line.split_whitespace().find(|x: &&str| x.len() == N_SEGMENTS_OF_NUMBER_4).unwrap();
        let segments_of_digit_7: &str = line.split_whitespace().find(|x: &&str| x.len() == N_SEGMENTS_OF_NUMBER_7).unwrap();

        line.split_whitespace().skip(N_WHITESPACES_BEFORE_DIGIT_OUTPUT).enumerate().for_each(|(digit_index, output_digit): (usize, &str)| {

            let individual_output_digit: u32 = match output_digit.len() {
                N_SEGMENTS_OF_NUMBER_1 => 1,
                N_SEGMENTS_OF_NUMBER_4 => 4,
                N_SEGMENTS_OF_NUMBER_7 => 7,
                N_SEGMENTS_OF_NUMBER_8 => 8,

                N_SEGMENTS_OF_NUMBER_0_6_OR_9 => {
                    if segments_of_digit_1.chars().all(|x: char| output_digit.contains(x)) == false {
                        6
                    } else if segments_of_digit_4.chars().all(|x: char| output_digit.contains(x)) == false { // as it cannot be 6 due to the previous if expression, if all segments of 4 are not in the output digit, it has to be a 0 
                        0
                    } else {
                        9
                    }
                },

                N_SEGMENTS_OF_NUMBER_2_3_OR_5 => {
                    if segments_of_digit_4.chars().filter(|x: &char| output_digit.contains(*x)).count() == N_SEGMENTS_OF_NUMBER_2_IN_NUMBER_4 {
                        2
                    } else if segments_of_digit_7.chars().all(|x: char| output_digit.contains(x)) == true { 
                        3
                    } else {
                        5
                    }
                },

                _ => unreachable!("Output digit has an impossible number of segments")
            };
            
            // the variable individual_output_digit is made just for clarity. The result of the match expression could be added directly to output_values_addition
            output_values_addition += individual_output_digit * 10_u32.pow((N_DIGITS_IN_OUTPUT-1-digit_index).try_into().unwrap())
        });
    });
    
    println!("All output values add up to {output_values_addition}");
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