/** 
 * The implemented solution checks every aunt until finding one that fulfills the given conditions
*/

#include <fstream>
#include <iostream>
#include <unordered_map>


#define PUZZLE_INPUT_FILE_NAME "puzzle_inputs/day16.txt"
#define PUZZLE_EXAMPLE_INPUT_FILE_NAME "puzzle_inputs/day16_example.txt"

enum CharacteristicCondition {
    EqualThan,
    GreatherThan,
    FewerThan
}; // Condition imposed by the respective aunt characteristic


void solve_first_part(std::ifstream &puzzle_file) 
{
    const std::unordered_map<std::string, const uint> target_aunt_characteristics = {
        { "children", 3 },
        { "cats", 7 },
        { "samoyeds", 2 },
        { "pomeranians", 3 },
        { "akitas", 0 },
        { "vizslas", 0 },
        { "goldfish", 5 },
        { "trees", 3 },
        { "cars", 2 },
        { "perfumes", 1 }
    };


    uint target_aunt_number;
    std::string line;
    while (std::getline(puzzle_file, line))
    {
        std::size_t last_delimiter;
        std::size_t next_delimiter = line.find(":") + 1;

        bool target_aunt_detected = true;
        while (next_delimiter != std::string::npos)
        {
            last_delimiter = next_delimiter + 1;
            next_delimiter = line.find(" ", last_delimiter);

            std::string characteristic_name = line.substr(last_delimiter, next_delimiter-last_delimiter-1);
                
            last_delimiter = next_delimiter + 1;
            next_delimiter = line.find(" ", last_delimiter);
            
            
            auto target_aunt_characteristic = target_aunt_characteristics.find(characteristic_name);
            if (target_aunt_characteristic != target_aunt_characteristics.cend()) 
            {
                uint characteristic_number = std::stoi(line.substr(last_delimiter, next_delimiter-last_delimiter)); // in many cases the substring includes a comma. It is ignored by std::stoi, so there is no need to filter it out
                if (characteristic_number != target_aunt_characteristic->second)
                {
                    target_aunt_detected = false;
                    break;
                }
            }
        }

        if (target_aunt_detected == true)
        {
            next_delimiter = line.find(" ");
            last_delimiter = next_delimiter + 1;
            next_delimiter = line.find(" ", next_delimiter-last_delimiter);
            target_aunt_number = std::stoi(line.substr(last_delimiter, next_delimiter-last_delimiter));

            break;
        }
        
    }

    std::cout << "The aunt that got the gift is the number " << target_aunt_number <<  std::endl;
}


/** 
 * This function is really similar to solve_first_part, except because the aunt characteristics are checked in a way or another depending on the CharacteristicCondition value.
 * A goto is used to avoid having the previously used (in the first part) boolean target_aunt_detected that needed to be checked every time a line was over. goto is used here for convenience and clarity because it also lets use a switch statement (which could have been a series of if conditions) that allows to break the loop that iterates over the contents of a line without needing another variable or more if statements
*/
void solve_second_part(std::ifstream &puzzle_file) 
{   
    const std::unordered_map<std::string, const std::pair<uint,CharacteristicCondition>> target_aunt_characteristics_solve_second_part = {
        { "children", std::pair<uint,CharacteristicCondition>(3,EqualThan) },
        { "cats", std::pair<uint,CharacteristicCondition>(7,GreatherThan) },
        { "samoyeds", std::pair<uint,CharacteristicCondition>(2,EqualThan) },
        { "pomeranians", std::pair<uint,CharacteristicCondition>(3,FewerThan) },
        { "akitas", std::pair<uint,CharacteristicCondition>(0,EqualThan) },
        { "vizslas", std::pair<uint,CharacteristicCondition>(0,EqualThan) },
        { "goldfish", std::pair<uint,CharacteristicCondition>(5,FewerThan) },
        { "trees", std::pair<uint,CharacteristicCondition>(3,GreatherThan) },
        { "cars", std::pair<uint,CharacteristicCondition>(2,EqualThan) },
        { "perfumes", std::pair<uint,CharacteristicCondition>(1,EqualThan) }
    }; // this variable could have been the same as the one used in part 1, target_aunt_characteristics, just by ignoring the enum value. Two separate variables are made just for clarity


    uint target_aunt_number;
    std::string line;
    while (std::getline(puzzle_file, line))
    {
        std::size_t last_delimiter;
        std::size_t next_delimiter = line.find(":") + 1;

        while (next_delimiter != std::string::npos)
        {
            last_delimiter = next_delimiter + 1;
            next_delimiter = line.find(" ", last_delimiter);

            std::string characteristic_name = line.substr(last_delimiter, next_delimiter-last_delimiter-1);
                
            last_delimiter = next_delimiter + 1;
            next_delimiter = line.find(" ", last_delimiter);
            
            auto target_aunt_characteristic = target_aunt_characteristics_solve_second_part.find(characteristic_name);
            if (target_aunt_characteristic != target_aunt_characteristics_solve_second_part.cend()) 
            {
                uint characteristic_number = std::stoi(line.substr(last_delimiter, next_delimiter-last_delimiter)); // in many cases the substring includes a comma. It is ignored by std::stoi, so there is no need to filter it out
        
                switch(target_aunt_characteristic->second.second)
                {
                    case CharacteristicCondition::EqualThan:
                    {
                        if (characteristic_number != target_aunt_characteristic->second.first)
                        {
                            goto continue_searching_next_line;
                        }
                        break;
                    }

                    case CharacteristicCondition::GreatherThan:
                    {
                        if (not (characteristic_number > target_aunt_characteristic->second.first))
                        {
                            goto continue_searching_next_line;
                        }
                        break;
                    }

                    case CharacteristicCondition::FewerThan:
                    {
                        if (not (characteristic_number < target_aunt_characteristic->second.first))
                        {
                            goto continue_searching_next_line;
                        }
                        break;
                    }
                }
            }
        }

        // when this point is reached, it means that the target aunt has been detected
        next_delimiter = line.find(" ");
        last_delimiter = next_delimiter + 1;
        next_delimiter = line.find(" ", next_delimiter-last_delimiter);
        target_aunt_number = std::stoi(line.substr(last_delimiter, next_delimiter-last_delimiter));
        break;

        continue_searching_next_line: ; 
    }

    std::cout << "Considering corrected aunt characteristics, the aunt that got the gift is the number " << target_aunt_number <<  std::endl;
}


int main(int argc, char* argv[]) 
{   
    const std::string puzzle_file_name( argc==1 ? PUZZLE_INPUT_FILE_NAME : (argc==2 ? PUZZLE_EXAMPLE_INPUT_FILE_NAME : argv[2]) ); // give one argument to use the example file instead of the default one. Give a second argument and that file will be used instead. There is actually no given example file for this puzzle, but this behaviour is kept for consistency with the rest of the programs in the project

    std::ifstream puzzle_file(puzzle_file_name);
    if (puzzle_file.is_open() == false)
    {
        std::cerr << "Could not open file \"" << puzzle_file_name << "\"" << std::endl;
        return EXIT_FAILURE;
    }

    solve_first_part(puzzle_file);

    puzzle_file.clear(); // clear eofbit, if ever reached (can happen if the target aunt is the last in the file and the file does not have a trailing newline)
    puzzle_file.seekg(0); // rewind
    solve_second_part(puzzle_file);
    
    return EXIT_SUCCESS;
}