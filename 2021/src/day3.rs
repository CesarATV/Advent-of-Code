const PUZZLE_INPUT_FILE_NAME: &str = "puzzle_inputs/day3.txt";
const PUZZLE_EXAMPLE_INPUT_FILE_NAME: &str = "puzzle_inputs/day3_example.txt";

enum BitCriteria {
    MostCommon,
    LeastCommon
}


fn solve_first_part(file_contents: &str) {
    let n_columns: usize = file_contents.find("\n").expect("Input file does not contain breaklines");
    let file_contents: String = file_contents.replace("\n", "");

    let n_rows: usize = file_contents.chars().count() / n_columns;
    let half_n_rows: u32 = u32::try_from(n_rows / 2).unwrap();

    let numbers_vector: Vec<char> = file_contents.chars().collect();
    
    let mut gamma_rate_binary: Vec<char> =  vec![' '; n_columns];
    let mut epsilon_rate_binary: Vec<char> =  vec![' '; n_columns];

    (0..n_columns).for_each(|current_column_idx: usize| {
        let mut n_zeros: u32 = 0;
        numbers_vector.iter().skip(current_column_idx).step_by(n_columns).for_each(|current_number: &char| {
            if *current_number == '0' {
                n_zeros += 1;
            }
        });

        if n_zeros > half_n_rows {
            gamma_rate_binary[current_column_idx] = '0';
            epsilon_rate_binary[current_column_idx] = '1';
        } 
        else if n_zeros < half_n_rows {
            gamma_rate_binary[current_column_idx] = '1';
            epsilon_rate_binary[current_column_idx] = '0';
        }
        else {
            panic!("Equal number of zeros and ones in a row. Posibility not contemplated by the puzzle instructions")
        }
    });

    let gamma_rate_binary: String = gamma_rate_binary.into_iter().collect();
    let gamma_rate: u32 = u32::from_str_radix(&gamma_rate_binary[..], 2).unwrap();

    let epsilon_rate_binary: String = epsilon_rate_binary.into_iter().collect();
    let epsilon_rate: u32 = u32::from_str_radix(&epsilon_rate_binary[..], 2).unwrap();

    let power_consumption: u32 = gamma_rate * epsilon_rate;
    println!("The power consumption of the submarine is {power_consumption}, with a gamma rate of {gamma_rate} and an epsilon rate of {epsilon_rate}");
}


fn solve_second_part(file_contents: &str) {
    let n_columns: usize = file_contents.find("\n").expect("Input file does not contain breaklines");
    let file_contents: String = file_contents.replace("\n", "");
    let numbers_vector: Vec<char> = file_contents.chars().collect();

    let n_rows: usize = file_contents.chars().count() / n_columns;

    let mut oxygen_generator_rating: u32 = 0;
    let mut co2_crubber_rating: u32 = 0;
    [BitCriteria::MostCommon, BitCriteria::LeastCommon].into_iter().for_each(|bit_criteria: BitCriteria| {
        let mut row_indexes_to_consider: Vec<usize> = (0..n_rows).collect();

        for col_idx in 0..n_columns {
            let mut row_indexes_zeros: Vec<usize> = Vec::new();
            let mut row_indexes_ones: Vec<usize> = Vec::new();
    
            row_indexes_to_consider.iter().for_each(|row_idx: &usize| {
                if numbers_vector[row_idx*n_columns + col_idx] == '0' {
                    row_indexes_zeros.push(*row_idx);
                } 
                else {
                    row_indexes_ones.push(*row_idx);
                }
            });
    
  
            match bit_criteria {
                BitCriteria::MostCommon => match row_indexes_zeros.len().cmp(&row_indexes_ones.len()) {
                    std::cmp::Ordering::Less => row_indexes_to_consider = row_indexes_ones,
                    std::cmp::Ordering::Greater => row_indexes_to_consider = row_indexes_zeros,
                    std::cmp::Ordering::Equal => row_indexes_to_consider = row_indexes_ones,
                },

                BitCriteria::LeastCommon => match row_indexes_zeros.len().cmp(&row_indexes_ones.len()) {
                    std::cmp::Ordering::Less => row_indexes_to_consider = row_indexes_zeros,
                    std::cmp::Ordering::Greater => row_indexes_to_consider = row_indexes_ones,
                    std::cmp::Ordering::Equal => row_indexes_to_consider = row_indexes_zeros,
                }
            }
    
            if row_indexes_to_consider.len() == 1 {
                let binary_number_string: String = numbers_vector[row_indexes_to_consider[0]*n_columns..(row_indexes_to_consider[0]+1)*n_columns].into_iter().collect();
                
                let rating: u32 = u32::from_str_radix(&binary_number_string[..], 2).unwrap();
                match bit_criteria {
                    BitCriteria::MostCommon => oxygen_generator_rating = rating,
                    BitCriteria::LeastCommon => co2_crubber_rating = rating
                }
                break;
            }
        }

        assert!(row_indexes_to_consider.len() == 1, "The data columns are over with not only one candidate left");
    });

    let life_support_rating: u32 = oxygen_generator_rating * co2_crubber_rating;
    println!("The life support rating is {life_support_rating}, with an oxygen generator rating of {oxygen_generator_rating} and a CO2 crubber rating of {co2_crubber_rating}");
}



fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file_contents: String = match std::env::args().count() {
        1 => std::fs::read_to_string(PUZZLE_INPUT_FILE_NAME)?,
        2 => std::fs::read_to_string(PUZZLE_EXAMPLE_INPUT_FILE_NAME)?,
        _ => std::fs::read_to_string(std::env::args().nth(2).unwrap())?
    };
    let file_contents: &str = file_contents.trim_end(); // remove last empty lines, if any. They do not add information and can cause confusion
    
    solve_first_part(file_contents);
    solve_second_part(file_contents);

    Ok(())
}