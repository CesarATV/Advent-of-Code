#include <fstream>
#include <iostream>
#include <regex>


#define PUZZLE_INPUT_FILE_NAME "puzzle_inputs/day5.txt"
#define PUZZLE_EXAMPLE_INPUT_FILE_NAME "puzzle_inputs/day5_example.txt"


void solve_first_part(std::ifstream &puzzle_file) 
{
    const std::regex regex_contains_enough_vowels("(.*[aeiou]){3,}"); // ./ allows matches even when the letters are not together, [aeiou] matches any latin vowel and {3,} does so that the previous match has to appear three times or more 
    const std::regex regex_repeated_letters_in_a_row(R"regex(([a-zA-Z])\1)regex"); // [a-zA-Z] matches any latin letter and \1 makes so that this previous match has to be matched again
    const std::regex regex_uncontainable_strings("ab|cd|pq|xy"); // | allows to match any of the specified strings
    
    uint n_nice_strings = 0;
    std::string current_line;
    while (std::getline(puzzle_file, current_line))
    {
        if (std::regex_search(current_line.cbegin(), current_line.cend(), regex_contains_enough_vowels) == true && std::regex_search(current_line.cbegin(), current_line.cend(), regex_repeated_letters_in_a_row) == true && std::regex_search(current_line.cbegin(), current_line.cend(), regex_uncontainable_strings) == false)
        {
            n_nice_strings += 1; // it fulfills the three conditions, so it is a nice string
        }
    }

    std::cout << "A total of " << n_nice_strings << " strings are nice" << std::endl;
}


void solve_second_part(std::ifstream &puzzle_file) 
{
    const std::regex regex_twice_pair_of_two_letters(R"regex(([a-zA-Z]{2})[a-zA-Z]*\1)regex"); // [a-zA-Z] matches any latin letter, {2} forces to match two of them, * allows any letter after the first group match and \1 makes so that the first group match has to be matched again
    const std::regex regex_repeated_letter_with_one_between_them(R"regex(([a-zA-Z])[a-zA-Z]\1)regex"); // [a-zA-Z] matches any latin letter, the following [a-zA-Z] makes sure that there is a character after the first detected and \1 makes so that this previous match (in a group) has to be matched again

    uint n_nice_strings = 0;
    std::string current_line;
    while (std::getline(puzzle_file, current_line))
    {
        if (std::regex_search(current_line.cbegin(), current_line.cend(), regex_twice_pair_of_two_letters) == true && std::regex_search(current_line.cbegin(), current_line.cend(), regex_repeated_letter_with_one_between_them) == true)
        {
            n_nice_strings += 1; // it fulfills both conditions, so it is a nice string
        }
    }

    std::cout << "Using the updapted model, a total of " << n_nice_strings << " strings are nice" <<  std::endl;
}


int main(int argc, char* argv[]) 
{   
    const std::string puzzle_file_name( argc==1 ? PUZZLE_INPUT_FILE_NAME : (argc==2 ? PUZZLE_EXAMPLE_INPUT_FILE_NAME : argv[2]) ); // give one argument to use the example file instead of the default one. Give a second argument and that file will be used instead

    std::ifstream puzzle_file(puzzle_file_name);
    if(puzzle_file.is_open() == false)
    {
        std::cerr << "Could not open file \"" << puzzle_file_name << "\"" << std::endl;
        return EXIT_FAILURE;
    }

    solve_first_part(puzzle_file);

    puzzle_file.clear(); // clear eofbit
    puzzle_file.seekg(0); // rewind
    solve_second_part(puzzle_file);
    
    return EXIT_SUCCESS;
}