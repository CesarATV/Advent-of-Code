const PUZZLE_INPUT_FILE_NAME: &str = "puzzle_inputs/day4.txt";
const PUZZLE_EXAMPLE_INPUT_FILE_NAME: &str = "puzzle_inputs/day4_example.txt";

const N_BOARD_ROWS: usize = 5;
const N_BOARD_COLUMNS: usize = 5;


#[derive(Clone)]
struct BingoBoard {
    called_numbers_positions: std::collections::HashMap<u32, (usize,usize,bool)>, // map with the numbers in the bingo board as keys. Each number (acting as key) corresponds to a row and column position; and also a boolean that tells if that key has been drawn or not (these three parameters act as the values of the map)
    n_row_marked_numbers: [usize; N_BOARD_ROWS], // each value in the vector represents the number of numbers that have been marked for a specific row
    n_column_marked_numbers: [usize; N_BOARD_COLUMNS] // each value in the vector represents the number of numbers that have been marked for a specific column
}


fn parse_puzzle_file(mut lines: core::str::Lines) -> (Vec<u32>, Vec<BingoBoard>) {
    let numbers_to_draw: Vec<u32> = lines.next().expect("Empty input file").split(",").map(|number: &str| number.parse::<u32>().expect("Not a number character in file lines")).collect();
    let mut bingo_boards: Vec<BingoBoard> = Vec::new();    
    
    let mut row_idx: usize = 0;
    lines.for_each(|line: &str| {
        if line == "" {
            row_idx = 0;
            bingo_boards.push(BingoBoard{called_numbers_positions: std::collections::HashMap::with_capacity(N_BOARD_ROWS*N_BOARD_COLUMNS), n_row_marked_numbers: [0; N_BOARD_ROWS], n_column_marked_numbers: [0; N_BOARD_COLUMNS]});
        }
        else { 
            line.split_whitespace().map(|number: &str| number.parse::<u32>().expect("Not a number character in file lines")).enumerate().for_each(|(column_idx, number_to_mark): (usize, u32)| {

                bingo_boards.last_mut().unwrap().called_numbers_positions.insert(number_to_mark, (row_idx, column_idx, false));
            });

            row_idx += 1;
        }
        
    });

    (numbers_to_draw, bingo_boards)
}


fn solve_first_part(numbers_to_draw: &Vec<u32>, mut bingo_boards: Vec<BingoBoard>) {

    let mut last_called_number: u32 = 0;
    let mut sum_unmarked_numbers: u32 = 0;
    'outer: for drawn_number in numbers_to_draw {
        for bingo_board in bingo_boards.iter_mut() {

            if let Some((row_n, col_n, has_it_been_drawn_before)) = bingo_board.called_numbers_positions.get_mut(drawn_number) {
                if *has_it_been_drawn_before == false {
                    *has_it_been_drawn_before = true;
                    bingo_board.n_row_marked_numbers[*row_n] += 1;
                    bingo_board.n_column_marked_numbers[*col_n] += 1;
                    
                    if bingo_board.n_row_marked_numbers[*row_n] == N_BOARD_ROWS || bingo_board.n_column_marked_numbers[*col_n] == N_BOARD_COLUMNS {
                        for (number, (_,_,has_it_been_marked)) in bingo_board.called_numbers_positions.iter() {
                            if *has_it_been_marked == false { 
                                sum_unmarked_numbers += number;
                            }
                        }
                        last_called_number = *drawn_number;
                        break 'outer;
                    }                    
                }
            }
        }
    }

    let score: u32 = sum_unmarked_numbers * last_called_number;
    println!("After calling number {last_called_number} and with an unmarked number sum of {sum_unmarked_numbers}, the first winning board will have a score of {score}");
}


fn solve_second_part(numbers_to_draw: &Vec<u32>, mut bingo_boards: Vec<BingoBoard>) {

    let mut boards_to_remove_indexes: Vec<usize> = Vec::new();
    let mut last_called_number: u32 = 0;
    let mut sum_unmarked_numbers: u32 = 0;
    numbers_to_draw.into_iter().for_each(|drawn_number: &u32| {
        bingo_boards.iter_mut().enumerate().for_each(|(board_idx, bingo_board): (usize, &mut BingoBoard)| {

            if let Some((row_n, col_n, has_it_been_drawn_before)) = bingo_board.called_numbers_positions.get_mut(drawn_number) {
                if *has_it_been_drawn_before == false {
                    *has_it_been_drawn_before = true;
                    bingo_board.n_row_marked_numbers[*row_n] += 1;
                    bingo_board.n_column_marked_numbers[*col_n] += 1;
                    
                    if bingo_board.n_row_marked_numbers[*row_n] == N_BOARD_ROWS || bingo_board.n_column_marked_numbers[*col_n] == N_BOARD_COLUMNS {
                        boards_to_remove_indexes.push(board_idx)
                    }
                }
            }
        });
        
        if bingo_boards.len() == 1 && boards_to_remove_indexes.len() == 1
        {
            for (number, (_,_,has_it_been_marked)) in bingo_boards[0].called_numbers_positions.iter() {
                if *has_it_been_marked == false { 
                    sum_unmarked_numbers += number;
                }
            }
            last_called_number = *drawn_number;
        }

        boards_to_remove_indexes.sort_by(|a: &usize, b: &usize| b.cmp(a)); // sort from biggest to smallest value, to be sure to remove the right indexes from the vector in the next line
        boards_to_remove_indexes.iter().for_each(|board_to_remove_idx: &usize| {
            bingo_boards.remove(*board_to_remove_idx);
        });
        boards_to_remove_indexes.clear();
    });
    

    let score: u32 = sum_unmarked_numbers * last_called_number;
    println!("After calling number {last_called_number} and with an unmarked number sum of {sum_unmarked_numbers}, the last winning board will have a score of {score}");
}


fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file_contents: String = match std::env::args().count() {
        1 => std::fs::read_to_string(PUZZLE_INPUT_FILE_NAME)?,
        2 => std::fs::read_to_string(PUZZLE_EXAMPLE_INPUT_FILE_NAME)?,
        _ => std::fs::read_to_string(std::env::args().nth(2).unwrap())?
    };
    let file_contents: &str = file_contents.trim_end(); // remove last empty lines, if any. They do not add information and can cause confusion
    
    let (numbers_to_draw, bingo_boards): (Vec<u32>, Vec<BingoBoard>) = parse_puzzle_file(file_contents.lines());

    solve_first_part(&numbers_to_draw, bingo_boards.clone());
    solve_second_part(&numbers_to_draw, bingo_boards);

    Ok(())
}