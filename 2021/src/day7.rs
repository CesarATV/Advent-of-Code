/// 
/// The first part of the puzzle asks to find the position of what would be the median of the positions.
/// 
/// The second part introduces another formula for fuel comsumption. By calling x the position of any crab and p the target position in which the crabs should be moved, and \sum a sumatory over all N crabs, the fuel comsumption can be calculated as \sum( ((x-p)^{2} + abs(x-p)) / 2).
/// Representing the derivative with ′, the derivative of leftmost term of the summatory is  (\sum( (x-p)^{2} / 2))′ =  \sum( x-p ) =  \sum(x) -p*N. Setting it to 0 to find the ideal minimum comsumption, the result is the definition of the mean value: p = \sum(x)/N
/// The derivative of the rightmost term of the original equation, when ignoring the case (x-p) = 0, is (\sum( abs(x-p) / 2 ))′ = \sum( sign(x-p) / 2 ). When setting it to 0, finding the ideal value of p is less simple than with the lefmost equation. Even when the rightmost and lefmost derivatives are added together to find the ideal p shared between then.
/// However, the rightmost derivative can have a minimum value of -0.5 (if all x-p are negative) and a maximum value of 0.5 (if all x-p are positive). Therefore, by using only the lefmost equation it is possible to find the ideal value of p with a marging of error of +-0.5. As the positions are discrete numbers, the ideal position has to be the ceiled or the floored positions around the mean. This reasoning is used to solve the second part
/// 

const PUZZLE_INPUT_FILE_NAME: &str = "puzzle_inputs/day7.txt";
const PUZZLE_EXAMPLE_INPUT_FILE_NAME: &str = "puzzle_inputs/day7_example.txt";


fn solve_first_part(file_contents: &str) {
    let mut positions_vector: Vec<i32> = file_contents.split(",").map(|x: &str| x.parse::<i32>().expect("Not a number in file lines")).collect();
    positions_vector.sort();


    let median_position: i32 = if (positions_vector.len() % 2) == 0 {
        (positions_vector[positions_vector.len()/2-1] + positions_vector[positions_vector.len()/2]) / 2
    }
    else {
        positions_vector[(positions_vector.len()+1)/2-1]
    };

    let fuel_cost: i32 = positions_vector.iter().map(|x: &i32| (x-median_position).abs()).sum();

    println!("The position that allows spending less fuel is {median_position}. It allows to spend only {fuel_cost}")
}


fn solve_second_part(file_contents: &str) {
    // as explained at the top of the file, this function uses the mean value to find the possible ideal positions (either the ceil or floor of that value) that give the minimum amount of fuel

    let positions_vector: Vec<i32> = file_contents.split(",").map(|x: &str| x.parse::<i32>().expect("Not a number in file lines")).collect();

    let mean_position: f32 = (positions_vector.iter().sum::<i32>() as f32) / (positions_vector.len() as f32);
    let mean_position_ceiled: i32 = f32::ceil(mean_position) as i32;
    let mean_position_floored: i32 = f32::floor(mean_position) as i32;

    let fuel_cost_of_ceiled_position: i32 = positions_vector.iter().map(|x: &i32| ( 1..=(x-mean_position_ceiled).abs() ).sum::<i32>()).sum();
    let fuel_cost_of_floored_position: i32 = positions_vector.iter().map(|x: &i32| ( 1..=(x-mean_position_floored).abs() ).sum::<i32>()).sum();
    
    let (fuel_cost, best_position): (i32, i32) = if fuel_cost_of_floored_position < fuel_cost_of_ceiled_position {
        (fuel_cost_of_floored_position, mean_position_floored)
    } else {
        (fuel_cost_of_ceiled_position, mean_position_ceiled)
    };

    println!("With the new considerations, the position that allows spending less fuel is {best_position}. It allows to spend only {fuel_cost}")
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