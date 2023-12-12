/** 
 * The implemented solution is really similar to the solution implemented in Day 9. It iterates over all possible table permutations until finding maximum happiness change. The calculations are done in the function get_maximum_table_happiness.
 * Currently, the happiness changes are calculated also for symmetric permutations (e.g. the happiness between persons 'a' and 'b' is computed as well as the happiness between persons 'b' and 'a') and in circular permutations (e.g. the happiness between people arranged 'abc' is computed as well as the happiness between people 'bca',depiste it being the same). This is unnecessary. However, as the program is fast enough, it is not extremmely necessary to avoid these calculations.
 * 
 * TODO: Avoid computing happiness changes for symmetric an circular permutations
 * 
 * An unordered map is used to store the relationships between family members, storing their names as keys. However, their names are added (concatenated) together, as storing them separately would require to use a structure or a std::pair and implementing a hash function or using an ordered map. This solution is not very elegant.
*/

#include <fstream>
#include <iostream>
#include <vector>
#include <algorithm>
#include <unordered_map>
#include <unordered_set>


#define PUZZLE_INPUT_FILE_NAME "puzzle_inputs/day13.txt"
#define PUZZLE_EXAMPLE_INPUT_FILE_NAME "puzzle_inputs/day13_example.txt"

#define CHANGE_IN_HAPPINESS_PRODUCED_BY_YOU 0


void parse_puzzle_file(std::vector<std::string> &family_names_vector, std::unordered_map<std::string, int> &happiness_between_family_members, std::ifstream &puzzle_file)
{
    std::unordered_set<std::string> family_names_set; // a set is not strictly necessary, but it is helpful to avoid checking if a name is already in family_names_vector, in order to not repeat it

    std::string line;
    while (std::getline(puzzle_file, line))
    {
        if (line == "")
        {
            // trailing newline
            break;
        }

        std::size_t previous_delimiter_position = line.find(" ");
        const std::string affected_person_name = line.substr(0, previous_delimiter_position);

        previous_delimiter_position += 1;
        previous_delimiter_position = line.find(" ", previous_delimiter_position) + 1;
        std::size_t next_delimiter_position = line.find(" ", previous_delimiter_position);
        const std::string happiness_effect_word = line.substr(previous_delimiter_position, next_delimiter_position-previous_delimiter_position);

        previous_delimiter_position = next_delimiter_position + 1;
        next_delimiter_position = line.find(" ", previous_delimiter_position);
        int happiness_change = std::stoi( line.substr(previous_delimiter_position, next_delimiter_position-previous_delimiter_position) );

        if (happiness_effect_word == "lose")
        {
            happiness_change = -happiness_change;
        }

        previous_delimiter_position = line.rfind(" ") + 1;
        const std::string table_neighbour_name = line.substr(previous_delimiter_position, line.size() - previous_delimiter_position - 1);

        family_names_set.insert(affected_person_name);

        happiness_between_family_members.insert({affected_person_name+table_neighbour_name, happiness_change});
    }

    family_names_vector.insert(family_names_vector.end(), family_names_set.begin(), family_names_set.end());
}


/** 
 * This function calculates also happiness with symmetric and circular permutations, without needing to do so
*/
int get_maximum_table_happiness(std::vector<std::string> &family_names_vector, const std::unordered_map<std::string, int> &happiness_between_family_members)
{
    std::sort(family_names_vector.begin(), family_names_vector.end()); // required to cover all permutations with std::next_permutation

    int maximum_happiness = std::numeric_limits<int>::min();
    do 
    {
        int current_accumulated_happiness = 0;
        std::string current_affected_person = family_names_vector.at(0);
        for (auto current_table_neighbour_it = family_names_vector.cbegin()+1; current_table_neighbour_it != family_names_vector.cend(); ++current_table_neighbour_it)
        {
            current_accumulated_happiness += happiness_between_family_members.at(current_affected_person+*current_table_neighbour_it);
            current_accumulated_happiness += happiness_between_family_members.at(*current_table_neighbour_it+current_affected_person);
            current_affected_person = *current_table_neighbour_it;
        }

        current_accumulated_happiness += happiness_between_family_members.at(current_affected_person+family_names_vector.at(0));
        current_accumulated_happiness += happiness_between_family_members.at(family_names_vector.at(0)+current_affected_person);
        

        if (current_accumulated_happiness > maximum_happiness)
        {
            maximum_happiness = current_accumulated_happiness;
        }
        
    } while (std::next_permutation(family_names_vector.begin(), family_names_vector.end()));

    return maximum_happiness;
}


void solve_first_part(std::vector<std::string> &family_names_vector, const std::unordered_map<std::string,int> &happiness_between_family_members) 
{
    const int maximum_happiness = get_maximum_table_happiness(family_names_vector, happiness_between_family_members);

    std::cout << "The optimal seating arrangement produces a total change in happiness of " << maximum_happiness << std::endl;
}


/** 
 * This function acts like solve_first_part and calls get_maximum_table_happiness, but before doing it adds the extra person (yourself) to the table, by modifying the vector containing the names and the map of the happiness between family members.
 * As the happiness changed produced by yourself is 0, instead of modifying the map, it could have been possible to modify get_maximum_table_happiness so it avoids doing any computation in which yourself is included
*/
void solve_second_part(std::vector<std::string> &family_names_vector, std::unordered_map<std::string, int> &happiness_between_family_members) 
{
    const std::string your_name("you"); // arbitrarily chosen. It should be different from any name already in family_names_vector

    for (const std::string &affected_person : family_names_vector) 
    {
        happiness_between_family_members.insert({affected_person+your_name,CHANGE_IN_HAPPINESS_PRODUCED_BY_YOU});
        happiness_between_family_members.insert({your_name+affected_person,CHANGE_IN_HAPPINESS_PRODUCED_BY_YOU});
    }

    family_names_vector.push_back(your_name);


    const int maximum_happiness = get_maximum_table_happiness(family_names_vector, happiness_between_family_members);

    std::cout << "Considering yourself, the optimal seating arrangement produces a total change in happiness of " << maximum_happiness << std::endl;
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
    
    std::vector<std::string> family_names_vector;
    std::unordered_map<std::string, int> happiness_between_family_members; // the key string is the addition (concatenation) of the two involved family members
    parse_puzzle_file(family_names_vector, happiness_between_family_members, puzzle_file);
    
    solve_first_part(family_names_vector, happiness_between_family_members);
    solve_second_part(family_names_vector, happiness_between_family_members);

    return EXIT_SUCCESS;
}