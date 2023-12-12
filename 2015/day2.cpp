#include <fstream>
#include <iostream>
#include <vector>
#include <algorithm>
#include <array>
#include <numeric>


#define PUZZLE_INPUT_FILE_NAME "puzzle_inputs/day2.txt"
#define PUZZLE_EXAMPLE_INPUT_FILE_NAME "puzzle_inputs/day2_example.txt"

#define DELIMITER_CHARACTER 'x'


void solve_first_part(std::vector<std::string> const &lines) 
{
    uint total_wrapping_papper = 0;
    std::array<uint,3> areas_array;
    for (const std::string &line : lines)
    {
        std::size_t last_delimiter = 0;
        std::size_t next_delimiter = line.find(DELIMITER_CHARACTER);
        uint length = std::stoi(line.substr(last_delimiter, next_delimiter));

        last_delimiter = next_delimiter + 1;
        next_delimiter = line.find(DELIMITER_CHARACTER, last_delimiter);
        uint width = std::stoi(line.substr(last_delimiter, next_delimiter-last_delimiter));


        last_delimiter = next_delimiter + 1;
        uint height = std::stoi(line.substr(last_delimiter));


        areas_array.at(0) = length*width;
        areas_array.at(1) = width*height;
        areas_array.at(2) = height*length;
        uint slack_area = *std::min_element(areas_array.cbegin(), areas_array.cend());
        total_wrapping_papper += 2*areas_array.at(0) + 2*areas_array.at(1) + 2*areas_array.at(2) + slack_area;
    }

    std::cout << "A total of " << total_wrapping_papper << " square feet of wrapping paper should be ordered" <<  std::endl;
}


void solve_second_part(std::vector<std::string> const &lines) 
{
    uint total_ribons = 0;
    std::array<uint,3> sides_array;
    for (const std::string &line : lines)
    {     
        std::size_t last_delimiter = 0;
        std::size_t next_delimiter = line.find(DELIMITER_CHARACTER);
        sides_array.at(0) = std::stoi(line.substr(last_delimiter, next_delimiter)); // length

        last_delimiter = next_delimiter + 1;
        next_delimiter = line.find(DELIMITER_CHARACTER, last_delimiter);
        sides_array.at(1) = std::stoi(line.substr(last_delimiter, next_delimiter)); // width

        last_delimiter = next_delimiter + 1;
        sides_array.at(2) = std::stoi(line.substr(last_delimiter)); // height


        uint volume = std::accumulate(sides_array.cbegin(), sides_array.cend(), 1, std::multiplies<>());
        std::sort(sides_array.begin(), sides_array.end());
        uint smallest_perimeter = sides_array.at(0)*2 + sides_array.at(1)*2;

        total_ribons += volume + smallest_perimeter;
    }

    std::cout << "A total of " << total_ribons << " feet of ribbon should be ordered" <<  std::endl;
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