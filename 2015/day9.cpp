/** 
 * The implemented solution iterates over all possible route permutations until finding the minimum and maximum distance between cities. The calculations are done in the function compute_maximum_and_minimum_city_distances, while solve_first_part and solve_second_part simply plot the results.
 * Currently, the distances are calculated also for symmetric routes (e.g. the distance between 'a' and 'b' is computed as well as the distance between 'b' and 'a'). This is unnecessary. However, as the program is fast enough, it is not extremmely necessary to avoid these calculations.
 * 
 * TODO: Avoid computing distances between cities for symmetric routes
 * 
 * An unordered map is used to store the distances between cities, storing their names as keys. However, their names are added (concatenated) together, as storing them separately would require to use a std::pair and implementing a hash function or using an ordered map. This solution is not very elegant.
*/

#include <fstream>
#include <iostream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <algorithm>


#define PUZZLE_INPUT_FILE_NAME "puzzle_inputs/day9.txt"
#define PUZZLE_EXAMPLE_INPUT_FILE_NAME "puzzle_inputs/day9_example.txt"


void parse_puzzle_file(std::vector<std::string> &city_names_vector, std::unordered_map<std::string, uint> &distances_between_cities, std::ifstream &puzzle_file)
{
    std::unordered_set<std::string> city_names_set; // a set is not strictly necessary, but it is helpful to avoid checking if a city is already in city_names_vector, in order to not repeat it

    std::string line;
    while (std::getline(puzzle_file, line))
    {
        if (line == "")
        {
            // trailing newline
            break;
        }

        std::size_t previous_delimiter_position = line.find(" ");
        const std::string beginning_city_name = line.substr(0, previous_delimiter_position);

        previous_delimiter_position += 1;
        previous_delimiter_position = line.find(" ", previous_delimiter_position) + 1;
        std::size_t next_delimiter_position = line.find(" ", previous_delimiter_position);


        const std::string ending_city_name = line.substr(previous_delimiter_position, next_delimiter_position-previous_delimiter_position);

        previous_delimiter_position = line.rfind(" ");
        const uint distance = std::stoi( line.substr(previous_delimiter_position+1) );

        city_names_set.insert(beginning_city_name);
        city_names_set.insert(ending_city_name);
        

        distances_between_cities.insert( {beginning_city_name+ending_city_name, distance} );
        distances_between_cities.insert( {ending_city_name+beginning_city_name, distance} );
    }

    city_names_vector.insert(city_names_vector.end(), city_names_set.begin(), city_names_set.end());
}


/** 
 * This function calculates also distances between symmetric paths, without needing to do so
*/
void compute_maximum_and_minimum_city_distances(uint &minimum_distance_between_cities, uint &maximum_distance_between_cities, std::vector<std::string> &route_with_minimum_distance_between_cities, std::vector<std::string> &route_with_maximum_distance_between_cities, std::vector<std::string> &city_names_vector, std::unordered_map<std::string, uint> const &distances_between_cities)
{
    std::sort(city_names_vector.begin(), city_names_vector.end()); // required to cover all permutations with std::next_permutation

    minimum_distance_between_cities = std::numeric_limits<uint>::max(); // temporarily assign the maximum possible value for an unsigned integer
    maximum_distance_between_cities = 0; // temporarily assign the minimum possible value for an unsigned integer
    do 
    {
        uint current_accumulated_distance = 0;
        std::string current_start_city = city_names_vector.at(0);
        for (auto current_end_city_it = city_names_vector.cbegin()+1; current_end_city_it != city_names_vector.cend(); ++current_end_city_it)
        {
            current_accumulated_distance += distances_between_cities.at(current_start_city+*current_end_city_it);
            current_start_city = *current_end_city_it;
        }

        if (current_accumulated_distance < minimum_distance_between_cities)
        {
            minimum_distance_between_cities = current_accumulated_distance;
            route_with_minimum_distance_between_cities = city_names_vector;
        }

        if (current_accumulated_distance > maximum_distance_between_cities)
        {
            maximum_distance_between_cities = current_accumulated_distance;
            route_with_maximum_distance_between_cities = city_names_vector;
        }
        
    } while(std::next_permutation(city_names_vector.begin(), city_names_vector.end()));
}


void solve_first_part(const uint minimum_distance_between_cities, const std::vector<std::string> &route_with_minimum_distance_between_cities) 
{
    std::cout << "The minimum distance between cities is " << minimum_distance_between_cities <<". The route is " << route_with_minimum_distance_between_cities.at(0);

    for (auto current_city_it = route_with_minimum_distance_between_cities.cbegin()+1; current_city_it != route_with_minimum_distance_between_cities.cend(); ++current_city_it)
    {
        std::cout << " -> " << *current_city_it;
    }
    std::cout <<  std::endl;
}


void solve_second_part(const uint maximum_distance_between_cities, const std::vector<std::string> &route_with_maximum_distance_between_cities) 
{
    std::cout << "The maximum distance between cities is " << maximum_distance_between_cities <<". The route is " << route_with_maximum_distance_between_cities.at(0);

    for (auto current_city_it = route_with_maximum_distance_between_cities.cbegin()+1; current_city_it != route_with_maximum_distance_between_cities.cend(); ++current_city_it)
    {
        std::cout << " -> " << *current_city_it;
    }
    std::cout <<  std::endl;
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
    
    std::vector<std::string> city_names_vector;
    std::unordered_map<std::string, uint> distances_between_cities; // the key string is the adition (concatenation) of the two involved city
    parse_puzzle_file(city_names_vector, distances_between_cities, puzzle_file);
    

    uint minimum_distance_between_cities;
    uint maximum_distance_between_cities;
    std::vector<std::string> route_with_minimum_distance_between_cities;
    std::vector<std::string> route_with_maximum_distance_between_cities;
    compute_maximum_and_minimum_city_distances(minimum_distance_between_cities, maximum_distance_between_cities, route_with_minimum_distance_between_cities, route_with_maximum_distance_between_cities, city_names_vector, distances_between_cities);

    solve_first_part(minimum_distance_between_cities, route_with_minimum_distance_between_cities);
    solve_second_part(maximum_distance_between_cities, route_with_maximum_distance_between_cities);

    return EXIT_SUCCESS;
}