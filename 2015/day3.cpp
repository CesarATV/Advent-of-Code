#include <fstream>
#include <iostream>
#include <algorithm>
#include <set> // unordered sets could have been used, but a set was preferred to avoid implementing a hash function to allow using std::pair<int, int> as keys. For similar reasons std::pair was used instead of a structure containing 2D coordinates
#include <array>


#define PUZZLE_INPUT_FILE_NAME "puzzle_inputs/day3.txt"
#define PUZZLE_EXAMPLE_INPUT_FILE_NAME "puzzle_inputs/day3_example.txt"

#define NORTH_CHARACTER '^'
#define SOUTH_CHARACTER 'v'
#define EAST_CHARACTER '>'
#define WEST_CHARACTER '<'

#define N_SANTA_VISITORS 2


void solve_first_part(const std::string &file_contents) 
{
    std::pair<int, int> santa_position = {0,0}; // x and y positions, in that order. x represents east-west movement and y represents north-south movement
    std::set<std::pair<int, int>> visited_houses({santa_position});
    for (const char &direction_character : file_contents)
    {
        switch (direction_character)
        {
            case NORTH_CHARACTER:
                santa_position.second += 1;
                break;
            
            case SOUTH_CHARACTER:
                santa_position.second -= 1;
                break;

            case EAST_CHARACTER:
                santa_position.first += 1;
                break;

            case WEST_CHARACTER:
                santa_position.first -= 1;
                break;
        }

        visited_houses.insert(santa_position); // the set alredy checks if the position is within the set. If it is, it will not be inserted
    }

    const uint n_unique_visited_houses = visited_houses.size();

    std::cout << n_unique_visited_houses << " houses receive at least 1 present" << std::endl;
}


void solve_second_part(const std::string &file_contents) 
{
    std::array< std::pair<int, int>, N_SANTA_VISITORS > santas_position;
    std::fill(santas_position.begin(), santas_position.end(), std::pair<int, int>(0,0)); // x and y positions, in that order. x represents east-west movement and y represents north-south movement
    std::set<std::pair<int, int>> visited_houses({santas_position.at(0)});
    
    for (uint file_content_idx=0, santa_idx=0; file_content_idx < file_contents.size(); file_content_idx++, santa_idx++)
    {
        santa_idx %= N_SANTA_VISITORS;
        const char direction_character = file_contents.at(file_content_idx);
        switch (direction_character)
        {
            case NORTH_CHARACTER:
                santas_position.at(santa_idx).second += 1;
                break;
            
            case SOUTH_CHARACTER:
                santas_position.at(santa_idx).second -= 1;
                break;

            case EAST_CHARACTER:
                santas_position.at(santa_idx).first += 1;
                break;

            case WEST_CHARACTER:
                santas_position.at(santa_idx).first -= 1;
                break;
        }
        visited_houses.insert(santas_position.at(santa_idx));
    }

    const uint n_unique_visited_houses = visited_houses.size();

    std::cout << n_unique_visited_houses << " houses receive at least 1 present when " << N_SANTA_VISITORS << " Santas work together" << std::endl;
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