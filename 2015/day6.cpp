/**
 * TODO: improve solve_first_part, for example by making it more similar to solve_second_part. solve_first_part takes more seconds than it should
 */

#include <fstream>
#include <iostream>
#include <vector>
#include <set> // unordered sets could have been used, but a set was preferred to avoid implementing a hash function to allow using std::pair<int, int> as keys. Similar requiremments were also the reason why std::pair was used instead of a structure containing 2D coordinates
#include <array>


#define PUZZLE_INPUT_FILE_NAME "puzzle_inputs/day6.txt"
#define PUZZLE_EXAMPLE_INPUT_FILE_NAME "puzzle_inputs/day6_example.txt"

#define N_ROWS 1000
#define N_COLS 1000


enum LightInstruction { 
    TurnOn, 
    TurnOff, 
    Switch 
};


void parse_puzzle_line(LightInstruction &light_instruction, uint &beginning_row, uint &beginning_col, uint &ending_row, uint &ending_col, std::string const &line)
{
    std::size_t last_delimiter = 0;
    std::size_t next_delimiter = line.find(" ");
    std::string light_instruction_string = line.substr(last_delimiter, next_delimiter);
    if(light_instruction_string == "toggle")
    {
        light_instruction = LightInstruction::Switch;
    }
    else
    {
        last_delimiter = next_delimiter + 1;
        next_delimiter = line.find(" ", last_delimiter);
        std::string on_or_off_string = line.substr(last_delimiter, next_delimiter-last_delimiter);
        if(on_or_off_string == "on")
        {
            light_instruction = LightInstruction::TurnOn;
        }
        else
        {
            light_instruction = LightInstruction::TurnOff;
        }
    }

    last_delimiter = next_delimiter + 1;
    next_delimiter = line.find(",", last_delimiter);
    beginning_row = std::stoi(line.substr(last_delimiter, next_delimiter-last_delimiter));
    
    last_delimiter = next_delimiter + 1;
    next_delimiter = line.find(" ", last_delimiter);
    beginning_col = std::stoi(line.substr(last_delimiter, next_delimiter-last_delimiter));

    last_delimiter = next_delimiter + 1;
    next_delimiter = line.find(" ", last_delimiter);
    last_delimiter = next_delimiter + 1;
    next_delimiter = line.find(",", last_delimiter);
    ending_row = std::stoi(line.substr(last_delimiter, next_delimiter-last_delimiter));

    last_delimiter = next_delimiter + 1;
    ending_col = std::stoi(line.substr(last_delimiter));
}


/**
 * The solution implemented in this function is an overkill, it could have been implemented in a more simple and (maybe) more efficient way followign the structure of the function solve_second_part: Iterating over every light in the grid altering its status according to the line instructions, and then just reading the final status
 * This function iterates over the lines of the file from the end to the beginning. This is to save some time processing more lights than necessary: As soon as one light is declared on or off, it will remain in the corresponding fixed status, independently of previous (from the beginning of the file) lines. Therefore, once a light reaches a fixed status there is no need to process that light anymore.
 * The switch statements only matter for the non-explicitely-turned-on-or-off lights  
 */
void solve_first_part(std::vector<std::string> const &lines) 
{
    std::set<std::pair<uint, uint>> light_grid_indexes_yet_to_process;
    for (uint row_idx=0; row_idx<N_ROWS; row_idx++)
    {
        for (uint col_idx=0; col_idx<N_COLS; col_idx++)
        {
            light_grid_indexes_yet_to_process.insert(light_grid_indexes_yet_to_process.end(), std::pair<uint, uint>(row_idx,col_idx));
        }
    }

    std::array<bool, N_ROWS*N_COLS> light_grid_indexes_switched = {false};

    uint n_lights_on = 0;
    for (auto line_it = lines.crbegin(); line_it != lines.crend(); ++line_it)
    {
        LightInstruction light_instruction;
        uint beginning_row, beginning_col, ending_row, ending_col;
        parse_puzzle_line(light_instruction, beginning_row, beginning_col, ending_row, ending_col, *line_it);
        for (uint row_idx = beginning_row; row_idx <= ending_row; row_idx++)
        {
            for (uint col_idx = beginning_col; col_idx <= ending_col; col_idx++)
            {
                if (light_instruction == LightInstruction::Switch)
                {
                    light_grid_indexes_switched[row_idx*N_COLS + col_idx] = !light_grid_indexes_switched[row_idx*N_COLS + col_idx];
                }
                else
                {
                    uint light_removed_from_list = light_grid_indexes_yet_to_process.erase( std::pair<uint, uint>(row_idx, col_idx) );

                    if ( (light_instruction == LightInstruction::TurnOn and light_grid_indexes_switched[row_idx*N_COLS + col_idx] == false) or (light_instruction == LightInstruction::TurnOff and light_grid_indexes_switched[row_idx*N_COLS + col_idx] == true) )
                    {
                        n_lights_on += light_removed_from_list;
                    }
                }
            }
        }
    }

    // process the non-explicitely mentioned lights in the grid
    for (const std::pair<uint, uint> &light_position : light_grid_indexes_yet_to_process)
    {
        const uint row_idx = light_position.first;
        const uint col_idx = light_position.second;

        if (light_grid_indexes_switched[row_idx*N_COLS + col_idx] == true)
        {
            n_lights_on++; // all lights start turned off by default, so if they where switched, they end up on
        }
    }
    std::cout << "After following the instructions " << n_lights_on << " lights were turned on" <<  std::endl;
}


void solve_second_part(std::vector<std::string> const &lines)
{
    std::array<uint, N_ROWS*N_COLS> light_grid_brightness = {0};

    for (const std::string &line : lines)
    {
        LightInstruction light_instruction;
        uint beginning_row, beginning_col, ending_row, ending_col;
        parse_puzzle_line(light_instruction, beginning_row, beginning_col, ending_row, ending_col, line);
        for (uint row_idx = beginning_row; row_idx <= ending_row; row_idx++)
        {
            for (uint col_idx = beginning_col; col_idx <= ending_col; col_idx++)
            {
                switch (light_instruction)
                {
                    case LightInstruction::Switch:
                        light_grid_brightness[row_idx*N_COLS + col_idx] += 2;
                        break;
                    
                    case LightInstruction::TurnOn:
                        light_grid_brightness[row_idx*N_COLS + col_idx] += 1;
                        break;
                
                    case LightInstruction::TurnOff:
                        if (light_grid_brightness[row_idx*N_COLS + col_idx] != 0)
                        {
                            light_grid_brightness[row_idx*N_COLS + col_idx] -= 1;
                        }
                }
            }
        }
    }

    uint total_brightness = 0;
    for (const uint &light_brightness : light_grid_brightness)
    {
        total_brightness += light_brightness;
    }

    std::cout << "After following the correct instructions there will be a total brightness of " << total_brightness <<  std::endl;
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

    std::vector<std::string> lines;
    std::string line;
    while (std::getline(puzzle_file, line))
    {
        lines.push_back(line);
    }
    while (lines.back() == "")
    {
        lines.pop_back();  // remove last empty lines, if any. They do not add information and can cause confusion
    }
    
    solve_first_part(lines);
    solve_second_part(lines);
    
    return EXIT_SUCCESS;
}