/** 
 * To compute the second part the first part is computed again extending the number of processes it makes. This repetition could be avoided with trivial modifications. The program is left as it is because it is fast enough and it avoids a more verbose solution.
*/

#include <fstream>
#include <iostream>
#include <algorithm>


#define PUZZLE_INPUT_FILE_NAME "puzzle_inputs/day10.txt"
#define PUZZLE_EXAMPLE_INPUT_FILE_NAME "puzzle_inputs/day10_example.txt"

#define N_PROCESSES_PART1 40
#define N_PROCESSES_PART2 50


void solve_first_part(std::string resulting_sequence, uint n_processes) 
{
    for (uint idx=0; idx<n_processes; idx++)
    {
        std::string newest_sequence;

        std::size_t current_number_position = 0;
        while (current_number_position != std::string::npos)
        {
            char current_number = resulting_sequence.at(current_number_position);
        
            std::size_t first_noncurrent_number_position = resulting_sequence.find_first_not_of(current_number, current_number_position+1);

            std::size_t n_current_number;
            if (first_noncurrent_number_position == std::string::npos)
            {
                n_current_number = resulting_sequence.length() - current_number_position;
                current_number_position = std::string::npos;
            }
            else 
            {
                n_current_number = first_noncurrent_number_position - current_number_position;
                current_number_position += n_current_number;
            }

            newest_sequence.push_back(n_current_number + '0'); // the addition of '0' is made to transform the number into the char of that number
            newest_sequence.push_back(current_number);
        }

        resulting_sequence = newest_sequence;
    }

    std::cout << "After " << n_processes << " processes, the resulting sequence has a length of " << resulting_sequence.length() << std::endl;
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
    while(file_contents.back() == '\n')
    {
        file_contents.pop_back(); // remove last empty lines, if any. They do not add information and can cause confusion
    }

    solve_first_part(file_contents, N_PROCESSES_PART1);

    auto solve_second_part = solve_first_part;
    solve_second_part(file_contents, N_PROCESSES_PART2);
    
    return EXIT_SUCCESS;
}