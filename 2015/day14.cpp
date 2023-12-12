/** 
 * The implemented solution calculates the distance traveled by each reindeer. The second part calculates this distance in every minute of the competition, while the first part only does it for the end of it
*/

#include <fstream>
#include <iostream>
#include <vector>
#include <algorithm>


#define PUZZLE_INPUT_FILE_NAME "puzzle_inputs/day14.txt"
#define PUZZLE_EXAMPLE_INPUT_FILE_NAME "puzzle_inputs/day14_example.txt"


#define TIME_LIMIT 2503
#define TIME_LIMIT_EXAMPLE_FILE 1000

#define SPEED_DELIMITER_KEYWORD_BEGIN "fly"
#define SPEED_DELIMITER_KEYWORD_END "km"
#define TIME_DELIMITER_KEYWORD_BEGIN "for"
#define TIME_DELIMITER_KEYWORD_END "seconds"


struct Reindeer {
    std::string name; // not necessary to solve the puzzle, but used to print the name of the winning reindeer to stdout
    uint flight_speed;
    uint flight_time;
    uint rest_time;

    uint flight_and_rest_period; // only used in the second part to avoid calculating the sum of flight_speed and flight_time multiple times
};


void parse_puzzle_file(std::vector<Reindeer> &reindeers, std::ifstream &puzzle_file)
{
    std::string line;
    while (std::getline(puzzle_file, line))
    {
        if (line == "")
        {
            // trailing newline
            break;
        }

        Reindeer reindeer;

        // note: all sizeof operations on the strings do take into account the null terminator

        std::size_t next_delimiter = line.find(" ");
        reindeer.name = line.substr(0, next_delimiter);

        std::size_t last_delimiter = line.find(SPEED_DELIMITER_KEYWORD_BEGIN) + sizeof(SPEED_DELIMITER_KEYWORD_BEGIN);
        next_delimiter = line.find(SPEED_DELIMITER_KEYWORD_END) - 1;
        reindeer.flight_speed = std::stoi(line.substr(last_delimiter, next_delimiter-last_delimiter));

        last_delimiter = line.find(TIME_DELIMITER_KEYWORD_BEGIN) + sizeof(TIME_DELIMITER_KEYWORD_BEGIN);
        next_delimiter = line.find(TIME_DELIMITER_KEYWORD_END) - 1;
        reindeer.flight_time = std::stoi(line.substr(last_delimiter, next_delimiter-last_delimiter));

        last_delimiter = line.find(TIME_DELIMITER_KEYWORD_BEGIN, next_delimiter) + sizeof(TIME_DELIMITER_KEYWORD_BEGIN);
        next_delimiter = line.find(TIME_DELIMITER_KEYWORD_END, last_delimiter) - 1;
        reindeer.rest_time = std::stoi(line.substr(last_delimiter, next_delimiter-last_delimiter));

        reindeer.flight_and_rest_period = reindeer.flight_time + reindeer.rest_time;

        reindeers.push_back(reindeer);
    }
}


void solve_first_part(const std::vector<Reindeer> &reindeers, const uint time_limit) 
{
    uint current_maximum_traveled_distance = 0;
    const std::string *winner_reindeer_name; // not necessary to solve the puzzle, but used to print the name of the winning reindeer to stdout
    for (const Reindeer &reindeer : reindeers)
    {
        const uint n_complete_flights = time_limit / reindeer.flight_and_rest_period;
        uint n_minutes_in_incomplete_flight = time_limit % reindeer.flight_and_rest_period;
        if (n_minutes_in_incomplete_flight > reindeer.flight_time)
        {
            n_minutes_in_incomplete_flight = reindeer.flight_time;
        }

        const uint traveled_distance = reindeer.flight_speed * (n_complete_flights * reindeer.flight_time + n_minutes_in_incomplete_flight);
        if (traveled_distance > current_maximum_traveled_distance)
        {
            current_maximum_traveled_distance = traveled_distance;
            winner_reindeer_name = &reindeer.name;
        }
    }

    std::cout << "The winner reindeer is " << *winner_reindeer_name << ". It traveled " << current_maximum_traveled_distance << " km after " << time_limit << " minutes" <<  std::endl;
}


/** 
 * The function does not only solve the second part of the puzzle as it also calculates all the traveled distance of each reindeer, allowing to solve also the first part of the puzzle
*/
void solve_second_part(const std::vector<Reindeer> &reindeers, const uint time_limit) 
{
    std::vector<uint> reindeer_scores(reindeers.size(), 0);
    std::vector<uint> traveled_kms_by_reender(reindeers.size(), 0);
    for (uint current_minute=0; current_minute<=time_limit; current_minute++)
    {
        uint reindeer_idx = 0;
        for (const Reindeer &reindeer : reindeers)
        {
            const bool is_reindeer_flying = (current_minute % reindeer.flight_and_rest_period) < reindeer.flight_time;
            if (is_reindeer_flying == true)
            {
                traveled_kms_by_reender.at(reindeer_idx) += reindeer.flight_speed;
            }
            reindeer_idx++;
        }

        const uint current_farthest_distance = *std::max_element(traveled_kms_by_reender.cbegin(), traveled_kms_by_reender.cend());

        for (reindeer_idx=0; reindeer_idx<traveled_kms_by_reender.size(); reindeer_idx++)
        {
            if (traveled_kms_by_reender.at(reindeer_idx) == current_farthest_distance)
            {
                reindeer_scores.at(reindeer_idx) += 1;
            }
        }        
    }

    const uint highest_score_idx = std::distance(reindeer_scores.cbegin(), std::max_element(reindeer_scores.cbegin(), reindeer_scores.cend()));

    std::cout << "With the new scoring system, the winner reindeer is " << reindeers.at(highest_score_idx).name << ". It got a score of " << reindeer_scores.at(highest_score_idx) << " having traveled " << traveled_kms_by_reender.at(highest_score_idx) << " km after " << time_limit << " minutes" <<  std::endl;
}


int main(int argc, char* argv[]) 
{   
    const std::string puzzle_file_name( argc==1 ? PUZZLE_INPUT_FILE_NAME : (argc==2 ? PUZZLE_EXAMPLE_INPUT_FILE_NAME : argv[2]) ); // Give one argument to use the example file instead of the default one. Give a second argument and that file will be used instead
    const uint time_limit = ((argc==2) or (argc>=4)) ? TIME_LIMIT_EXAMPLE_FILE : TIME_LIMIT; // Give one or at least a third argument and the file will be considered an example file

    std::ifstream puzzle_file(puzzle_file_name);
    if (puzzle_file.is_open() == false)
    {
        std::cerr << "Could not open file \"" << puzzle_file_name << "\"" << std::endl;
        return EXIT_FAILURE;
    }

    std::vector<Reindeer> reindeers;
    parse_puzzle_file(reindeers, puzzle_file);

    solve_first_part(reindeers, time_limit);
    solve_second_part(reindeers, time_limit);
    
    return EXIT_SUCCESS;
}