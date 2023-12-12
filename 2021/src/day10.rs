/// 
/// To keep track of the open and closed brackets, a stack is used. An open bracket is pushed to the stack while a closing bracket pops from it. If the popped bracket does not correspond to the closing bracket, the line is considered corrupted.
/// 
/// The functions to solve the first and the second part of the puzzle could be easily merged together as they share the same structure. They are left separated for clarity and because the program is fast enough.
/// 

const PUZZLE_INPUT_FILE_NAME: &str = "puzzle_inputs/day10.txt";
const PUZZLE_EXAMPLE_INPUT_FILE_NAME: &str = "puzzle_inputs/day10_example.txt";


const ROUND_BRACKETS_CORRUPTION_SCORE: u32 = 3;
const SQUARE_BRACKETS_CORRUPTION_SCORE: u32 = 57;
const CURLY_BRACKETS_CORRUPTION_SCORE: u32 = 1197;
const ANGLE_BRACKETS_CORRUPTION_SCORE: u32 = 25137;

const ROUND_BRACKETS_INCOMPLETION_SCORE: u64 = 1;
const SQUARE_BRACKETS_INCOMPLETION_SCORE: u64 = 2;
const CURLY_BRACKETS_INCOMPLETION_SCORE: u64 = 3;
const ANGLE_BRACKETS_INCOMPLETION_SCORE: u64 = 4;

const INCOMPLETION_SCORE_MULTIPLICATION_VALUE: u64 = 5;


const WRONG_FILE_CONTENTS_ERROR_MESSAGE: &str = "Wrong file contents: there are more closing than opening brackets";


fn solve_first_part(lines: core::str::Lines) {
    let mut n_illegal_round_brackets: u32 = 0;
    let mut n_illegal_square_brackets: u32 = 0;
    let mut n_illegal_curly_brackets: u32 = 0;
    let mut n_illegal_angle_brackets: u32 = 0;

    let mut bracket_stack: Vec<char> = Vec::new();
    lines.for_each(|line: &str| {
        
        bracket_stack.clear();

        let mut line_chars: std::str::Chars = line.chars();
        while let Some(bracket_character) = line_chars.find(|c: &char| "([{<>}])".contains(*c)) {
            match bracket_character {
                '(' | '[' | '{' | '<' =>  bracket_stack.push(bracket_character),

                ')' => if bracket_stack.pop().expect(WRONG_FILE_CONTENTS_ERROR_MESSAGE) != '(' {
                    n_illegal_round_brackets += 1;
                    break;
                },

                ']' => if bracket_stack.pop().expect(WRONG_FILE_CONTENTS_ERROR_MESSAGE) != '[' {
                    n_illegal_square_brackets += 1;
                    break;
                },

                '}' => if bracket_stack.pop().expect(WRONG_FILE_CONTENTS_ERROR_MESSAGE) != '{' {
                    n_illegal_curly_brackets += 1;
                    break;
                },

                '>' => if bracket_stack.pop().expect(WRONG_FILE_CONTENTS_ERROR_MESSAGE) != '<' {
                    n_illegal_angle_brackets += 1;
                    break;
                },

                _ => unreachable!()
            };
        }
    });
    
    let total_syntax_error_score: u32 = n_illegal_round_brackets*ROUND_BRACKETS_CORRUPTION_SCORE + n_illegal_square_brackets*SQUARE_BRACKETS_CORRUPTION_SCORE + n_illegal_curly_brackets*CURLY_BRACKETS_CORRUPTION_SCORE + n_illegal_angle_brackets*ANGLE_BRACKETS_CORRUPTION_SCORE;

    println!("The total syntax error score for the corrupted lines is {total_syntax_error_score}");
}


/// This function works very similarly to solve_first_part, but instead of counting the corrupted lines, counts the score for the incomplete ones. With very little modifications, this function could give the results asked by solve_first_part
/// The incomplete line score can be calculated just by checking the contents of the stack of brackets after finishing analyzing the line 
fn solve_second_part(lines: core::str::Lines) {
    let mut incomplete_lines_scores : Vec<u64> = Vec::new();
    let mut bracket_stack: Vec<char> = Vec::new();
    lines.for_each(|line: &str| {
        
        bracket_stack.clear();

        let mut line_chars: std::str::Chars = line.chars();
        loop {
            if let Some(bracket_character) = line_chars.find(|c: &char| "([{<>}])".contains(*c)) {
                match bracket_character {
                    '(' | '[' | '{' | '<' =>  bracket_stack.push(bracket_character),

                    ')' => if bracket_stack.pop().expect(WRONG_FILE_CONTENTS_ERROR_MESSAGE) != '(' {
                        break;
                    },

                    ']' => if bracket_stack.pop().expect(WRONG_FILE_CONTENTS_ERROR_MESSAGE) != '[' {
                        break;
                    },

                    '}' => if bracket_stack.pop().expect(WRONG_FILE_CONTENTS_ERROR_MESSAGE) != '{' {
                        break;
                    },

                    '>' => if bracket_stack.pop().expect(WRONG_FILE_CONTENTS_ERROR_MESSAGE) != '<' {
                        break;
                    },

                    _ => unreachable!()
                };
            } else { 
                // there are no more chars in the line and the line is not corrupted, so its incomplete line score can be calculated
                let mut line_score: u64 = 0;
                bracket_stack.iter().rev().for_each(|c: &char| match c {
                    '(' => line_score = line_score*INCOMPLETION_SCORE_MULTIPLICATION_VALUE + ROUND_BRACKETS_INCOMPLETION_SCORE,
                    '[' => line_score = line_score*INCOMPLETION_SCORE_MULTIPLICATION_VALUE + SQUARE_BRACKETS_INCOMPLETION_SCORE,
                    '{' => line_score = line_score*INCOMPLETION_SCORE_MULTIPLICATION_VALUE + CURLY_BRACKETS_INCOMPLETION_SCORE,
                    '<' => line_score = line_score*INCOMPLETION_SCORE_MULTIPLICATION_VALUE + ANGLE_BRACKETS_INCOMPLETION_SCORE,
                    _ => unreachable!() 
                });

                incomplete_lines_scores.push(line_score);
                break;
            }
        }

    });

    incomplete_lines_scores.sort_unstable();
    let middle_score: u64 = incomplete_lines_scores[incomplete_lines_scores.len()/2]; // the puzzle instructions assures that there is always an odd number of incomplete lines, so this will always take the middle value 
    
    println!("The middle score of the incomplete lines is {middle_score}");
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