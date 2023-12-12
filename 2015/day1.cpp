#include <fstream>
#include <iostream>
#include <algorithm>


#define PUZZLE_INPUT_FILE_NAME "puzzle_inputs/day1.txt"
#define PUZZLE_EXAMPLE_INPUT_FILE_NAME "puzzle_inputs/day1_example.txt"

#define FLOOR_UP_CHARACTER '('
#define FLOOR_DOWN_CHARACTER ')'


void solve_first_part(const std::string &file_contents) 
{
    int n_floors_up = std::count(file_contents.cbegin(), file_contents.cend(), FLOOR_UP_CHARACTER);
    int n_floors_down = std::count(file_contents.cbegin(), file_contents.cend(), FLOOR_DOWN_CHARACTER);
    int destination_floor_number = n_floors_up - n_floors_down;

    std::cout << "The instructions take to floor " << destination_floor_number << std::endl;
}


void solve_second_part(const std::string &file_contents) 
{
    int current_floor = 0;
    uint current_character_position;
    for (current_character_position=0; current_character_position < file_contents.length(); current_character_position++)
    {
        if (file_contents.at(current_character_position) == FLOOR_UP_CHARACTER)
        {
            current_floor += 1;
        }
        else
        {
            current_floor -= 1;
        }

        if (current_floor == -1)
        {
            break;
        }
    }

    if (current_floor != -1)
    {
        std::cout << "No character causes to enter the basement" << std::endl; // the instructions do not contemplate this posibility, but may happen with the examples
    }
    else
    {
        current_character_position += 1; // the characters for the solution begin at 1
        std::cout << "The character that causes to enter the basement first is in position " << current_character_position << std::endl;
    }
}


int main(int argc, char* argv[]) 
{   
    const std::string puzzle_file_name( argc==1 ? PUZZLE_INPUT_FILE_NAME : (argc==2 ? PUZZLE_EXAMPLE_INPUT_FILE_NAME : argv[2]) ); // give one argument to use the example file instead of the default one. Give a second argument and that file will be used instead 

    std::ifstream puzzle_file(puzzle_file_name);
    if (puzzle_file.is_open() == false)
    {
        std::cerr << "Could not open file \"" << puzzle_file_name << "\"" << std::endl;
        return EXIT_FAILURE;
    }

    std::string file_contents( std::istreambuf_iterator<char>(puzzle_file), (std::istreambuf_iterator<char>()) );
    while (file_contents.back() == '\n')
    {
        file_contents.pop_back(); // remove last empty lines, if any. They do not add information and can cause confusion
    }

    solve_first_part(file_contents);
    solve_second_part(file_contents);
    
    return EXIT_SUCCESS;
}