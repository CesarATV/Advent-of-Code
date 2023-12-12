#include <fstream>
#include <iostream>
#include <vector>


#define PUZZLE_INPUT_FILE_NAME "puzzle_inputs/day8.txt"
#define PUZZLE_EXAMPLE_INPUT_FILE_NAME "puzzle_inputs/day8_example.txt"


#define N_CHARACTERS_USED_TO_DELIMITE_STRING_LINES 2
#define N_CHARACTERS_ESCAPED_WHEN_WRITING_HEXADECIMAL_NUMBER 3
#define N_CHARACTERS_ESCAPED_WHEN_ESCAPING_A_SINGLE_CHARACTER 1
#define N_CHARACTERS_IN_BACKSLASH_CHARACTER 1

#define N_CHARACTERS_USED_TO_CODE_STRING_LINE_DELIMITERS (2*N_CHARACTERS_USED_TO_DELIMITE_STRING_LINES)


void solve_first_part(std::vector<std::string> const &lines) 
{
    std::size_t n_code_characters = 0;
    std::size_t n_escaped_characters = 0;

    std::string line;
    for (const std::string &line : lines)
    {
        n_code_characters += line.length();

        std::size_t backslash_position = line.find("\\");
        while (backslash_position != std::string::npos)
        {
            std::size_t new_position_to_search_backslash = backslash_position + N_CHARACTERS_IN_BACKSLASH_CHARACTER;
            if (line.at(new_position_to_search_backslash) == 'x')
            {
                new_position_to_search_backslash += N_CHARACTERS_ESCAPED_WHEN_WRITING_HEXADECIMAL_NUMBER;
                n_escaped_characters += N_CHARACTERS_ESCAPED_WHEN_WRITING_HEXADECIMAL_NUMBER;
            }
            else 
            {
                new_position_to_search_backslash += N_CHARACTERS_ESCAPED_WHEN_ESCAPING_A_SINGLE_CHARACTER;
                n_escaped_characters += N_CHARACTERS_ESCAPED_WHEN_ESCAPING_A_SINGLE_CHARACTER;
            }

            backslash_position = line.find("\\", new_position_to_search_backslash);
        }
        n_escaped_characters += N_CHARACTERS_USED_TO_DELIMITE_STRING_LINES;
    }

    std::size_t n_memory_characters = n_code_characters - n_escaped_characters;

    std::cout << "There are " << n_code_characters << " code characters for string literals that subtracted to the " << n_memory_characters << " characters in memory becomes " << n_escaped_characters << std::endl;
}


void solve_second_part(std::vector<std::string> const &lines) 
{
    std::size_t n_code_characters = 0;
    std::size_t n_extra_encoded_characters = 0;
    
    std::string line;
    for (const std::string &line : lines)
    {
        n_code_characters += line.length();

        std::size_t backslash_position = line.find("\\");
        while (backslash_position != std::string::npos)
        {
            std::size_t new_position_to_search_backslash = backslash_position + N_CHARACTERS_IN_BACKSLASH_CHARACTER;
            if (line.at(new_position_to_search_backslash) == 'x')
            {
                new_position_to_search_backslash += N_CHARACTERS_ESCAPED_WHEN_WRITING_HEXADECIMAL_NUMBER;
            }
            else 
            {
                new_position_to_search_backslash += N_CHARACTERS_ESCAPED_WHEN_ESCAPING_A_SINGLE_CHARACTER;
                n_extra_encoded_characters += N_CHARACTERS_ESCAPED_WHEN_ESCAPING_A_SINGLE_CHARACTER;
            }
            n_extra_encoded_characters += N_CHARACTERS_IN_BACKSLASH_CHARACTER;

            backslash_position = line.find("\\", new_position_to_search_backslash);
        }

        n_extra_encoded_characters += N_CHARACTERS_USED_TO_CODE_STRING_LINE_DELIMITERS;
    }

    std::size_t n_encoded_characters = n_code_characters + n_extra_encoded_characters;

    std::cout << n_encoded_characters << " characters are necessary to encode " << n_code_characters << " code characters for string literals, being a total of " << n_extra_encoded_characters << " extra characters" << std::endl;
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