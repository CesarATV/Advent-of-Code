/** 
 * For the second part, a solution that checks recursively all internal parentheses of an input string, adding all numbers in it. These numbers are then added to a total if the double counted string is not present within object parentheses
*/

#include <fstream>
#include <iostream>


#define PUZZLE_INPUT_FILE_NAME "puzzle_inputs/day12.txt"
#define PUZZLE_EXAMPLE_INPUT_FILE_NAME "puzzle_inputs/day12_example.txt"


#define POTENTIAL_NUMBER_CHARACTERS "-0123456789"

#define RELEVANT_CHARACTERS_STRING "{[]}"
#define DOUBLE_COUNTED_STRING "red"

#define OBJECT_OPENER_CHARACTER '{'
#define OBJECT_CLOSING_CHARACTER '}'
#define ARRAY_OPENER_CHARACTER '['
#define ARRAY_CLOSING_CHARACTER ']'


int sum_all_numbers_in_string(const std::string &input_string)
{   
    int number_sum = 0;
    std::size_t number_begin_position = input_string.find_first_of(POTENTIAL_NUMBER_CHARACTERS);
    while (number_begin_position != std::string::npos)
    {
        std::size_t const number_end_position = input_string.find_first_not_of(POTENTIAL_NUMBER_CHARACTERS, number_begin_position);
        number_sum += std::stoi(input_string.substr(number_begin_position,number_end_position-number_begin_position));

        number_begin_position = input_string.find_first_of(POTENTIAL_NUMBER_CHARACTERS, number_end_position);
    }

    return number_sum;
}


void solve_first_part(const std::string &file_contents)
{
    int sum_all_numbers = 0;
    sum_all_numbers += sum_all_numbers_in_string(file_contents);
    std::cout << "The sum of all numbers in the document is " << sum_all_numbers << std::endl;
}


/** 
 * Previously used function solve_first_part, before knowing the instructions of the second part, which revealed that a regex to solve the puzzle would not be straightforward to create. This function requires #include <regex>. This function was removed as solve_second_part already created a useful function to solve the first part, without the longer compilation times, the increase in the executable file size, and the (in this case negligible) increased execution time required by regex
*/
// void solve_first_part(const std::string &file_contents)
// {
//     const std::regex regex_any_number(R"regex(-*[0-9]+)regex"); // -* matches negative signs, if any, while [0-9]+ matches any digit at least once
//     int sum_all_numbers = 0;
//     for(std::sregex_iterator regex_it = std::sregex_iterator(file_contents.cbegin(), file_contents.cend(), regex_any_number); regex_it != std::sregex_iterator(); ++regex_it )
//     {
//         sum_all_numbers += std::stoi(regex_it->str());
//     }

//     std::cout << "The sum of all numbers in the document is " << sum_all_numbers << std::endl;
// }


/** 
 * This function assummes balanced parenthesis
*/
void count_nonred_numbers(int &superstring_sum, std::size_t &previously_read_character_position, const std::string &file_contents, const bool can_it_be_red, bool is_it_red)
{
    int substring_sum = 0;
    std::size_t previous_closest_read_character_position = previously_read_character_position;
    bool closing_character_detected = false;
    while (closing_character_detected == false)
    {
        std::size_t closest_read_character_position = file_contents.find_first_of(RELEVANT_CHARACTERS_STRING, previous_closest_read_character_position+1);
        
        if (can_it_be_red == true)
        {
            std::size_t red_position = file_contents.find(DOUBLE_COUNTED_STRING, previous_closest_read_character_position+1);
            if(red_position < closest_read_character_position)
            {
                is_it_red = true;
            }
        }

        if (is_it_red == false)
        {
            // there is no need to count the numbers if it is already known that the string is one of the double-counted ones
            substring_sum += sum_all_numbers_in_string(file_contents.substr(previous_closest_read_character_position, closest_read_character_position-previous_closest_read_character_position));
        }


        bool can_substring_be_red;
        switch (file_contents.at(closest_read_character_position))
        {
            case OBJECT_OPENER_CHARACTER:
            {
                can_substring_be_red = true;
                count_nonred_numbers(substring_sum, closest_read_character_position, file_contents, can_substring_be_red, is_it_red);
                break;
            }
            case ARRAY_OPENER_CHARACTER:
            {
                can_substring_be_red = false;
                count_nonred_numbers(substring_sum, closest_read_character_position, file_contents, can_substring_be_red, is_it_red);
                break;
            }

            case OBJECT_CLOSING_CHARACTER:
            case ARRAY_CLOSING_CHARACTER:
            {
                closing_character_detected = true;
                break;
            }
        }

        previous_closest_read_character_position = closest_read_character_position;
    }

    previously_read_character_position = previous_closest_read_character_position; // previous_closest_read_character_position is the same as the closest read character
    if (is_it_red == false)
    {
        superstring_sum += substring_sum;
    }
}


void solve_second_part(const std::string &file_contents)
{
    int sum_nonred_numbers = 0;

    std::size_t previously_read_character_position = file_contents.find_first_of(RELEVANT_CHARACTERS_STRING);
    bool can_it_be_red = file_contents.at(previously_read_character_position) == OBJECT_OPENER_CHARACTER ? true : false;

    count_nonred_numbers(sum_nonred_numbers, previously_read_character_position, file_contents, can_it_be_red, false);

    std::cout << "Ignoring the double-counted red objects, the sum of all numbers in the document is " << sum_nonred_numbers << std::endl;
}


int main(int argc, char* argv[]) 
{   
    const std::string puzzle_file_name( argc==1 ? PUZZLE_INPUT_FILE_NAME : (argc==2 ? PUZZLE_EXAMPLE_INPUT_FILE_NAME : argv[2]) ); // Give one argument to use the example file instead of the default one. Give a second argument and that file will be used instead

    std::ifstream puzzle_file(puzzle_file_name);
    if (puzzle_file.is_open() == false)
    {
        std::cerr << "Could not open file \"" << puzzle_file_name << "\"" << std::endl;
        return EXIT_FAILURE;
    }

    std::string file_contents( std::istreambuf_iterator<char>(puzzle_file), (std::istreambuf_iterator<char>()) );

    solve_first_part(file_contents);
    solve_second_part(file_contents);
    
    return EXIT_SUCCESS;
}