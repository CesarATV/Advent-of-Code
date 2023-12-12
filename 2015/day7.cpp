/** 
 * The implemented solution uses a map of classes. Each class that represent a circuit which is part of the complete circuit. Each class has the possibility to call its input circuits in order to obtain the input values it requires to produce an output. It can call them by knowing their names and having access to the maps where all of them are contained.
 * 
 * The example and the actual puzzle are slightly different, so a separate function is used to solve the puzzle example
*/

#include <fstream>
#include <iostream>
#include <unordered_map>
#include <memory>


#define PUZZLE_INPUT_FILE_NAME "puzzle_inputs/day7.txt"
#define PUZZLE_EXAMPLE_INPUT_FILE_NAME "puzzle_inputs/day7_example.txt"


#define TARGET_WIRE_NAME "a"
#define WIRE_TO_OVERWRITE_NAME "b"


enum OperationType {
    NoOperation,
    NotOperation,
    AndOperation,
    OrOperation,
    LeftShiftOperation,
    RightShiftOperation
};

class CircuitPart {
    
    private:
        std::unordered_map<std::string, std::unique_ptr<CircuitPart>> * const circuit_parts_map;

        const OperationType operation_type;
        const std::string first_input_wire; // name of the first input wire, if any, present in circuit_parts_map
        const std::string second_input_wire; // name of the second input wire, if any, present in circuit_parts_map

        uint16_t first_input_value;
        uint16_t second_input_value;
        uint16_t output_value;
        
        bool is_first_input_available;
        bool is_second_input_available;

        bool is_there_need_to_calculate_first_input;
        bool is_there_need_to_calculate_second_input;

        bool is_output_available; // this variable helps to avoid needing to calculate an output every time

    public:
        void reset_circuit_output()
        {
            is_output_available = false;
        }

        void overwrite_output_value(uint16_t new_output_value)
        {
            output_value = new_output_value;
            is_output_available = true;
        }

        /** 
         * Get the output produced by the current circuit part. This may imply calling input circuits, if there is any
        */
        uint16_t join_circuit()
        {
            if (is_output_available == false)
            {
                if (is_there_need_to_calculate_first_input == true)
                {
                    first_input_value = circuit_parts_map->at(first_input_wire)->join_circuit();
                }
                
                if (is_there_need_to_calculate_second_input == true)
                {
                    second_input_value = circuit_parts_map->at(second_input_wire)->join_circuit();
                }

                switch (operation_type) 
                {
                    case OperationType::NoOperation:
                        output_value = first_input_value;
                        break;

                    case OperationType::NotOperation:
                        output_value = ~ first_input_value;
                        break;

                    case OperationType::AndOperation:
                        output_value = first_input_value & second_input_value;
                        break;

                    case OperationType::OrOperation:
                        output_value = first_input_value | second_input_value;
                        break; 

                    case OperationType::LeftShiftOperation:
                        output_value = first_input_value << second_input_value;
                        break;

                    case OperationType::RightShiftOperation:
                        output_value = first_input_value >> second_input_value;
                        break;
                }
                
                is_output_available = true;
            }

            return output_value;
        }


        CircuitPart(std::unordered_map<std::string, std::unique_ptr<CircuitPart>> * const circuit_parts_map, OperationType operation_type, std::string first_input_wire) : circuit_parts_map(circuit_parts_map), operation_type(operation_type), first_input_wire(first_input_wire), is_output_available(false)
        {
            if (first_input_wire.find_first_of("0123456789") != std::string::npos)
            {
                first_input_value = std::stoi(first_input_wire);
                is_first_input_available = true;
                is_there_need_to_calculate_first_input = false;
            }
            else 
            {
                is_there_need_to_calculate_first_input = true;
            }

            is_there_need_to_calculate_second_input = false;
        }


        CircuitPart(std::unordered_map<std::string, std::unique_ptr<CircuitPart>> * const circuit_parts_map, OperationType operation_type, std::string first_input_wire, std::string second_input_wire) : circuit_parts_map(circuit_parts_map), operation_type(operation_type), first_input_wire(first_input_wire), second_input_wire(second_input_wire), is_output_available(false)
        {
            if (first_input_wire.find_first_of("0123456789") != std::string::npos)
            {
                first_input_value = std::stoi(first_input_wire);
                is_there_need_to_calculate_first_input = false;
            }
            else 
            {
                is_there_need_to_calculate_first_input = true;
            }


            if (second_input_wire.find_first_of("0123456789") != std::string::npos)
            {
                second_input_value = std::stoi(second_input_wire);
                is_there_need_to_calculate_second_input = false;
            }
            else 
            {
                is_there_need_to_calculate_second_input = true;
            }
        }
};


void parse_puzzle_file(std::unordered_map<std::string, std::unique_ptr<CircuitPart>> &circuit_parts_map, std::ifstream &puzzle_file)
{
    std::string line;
    while (std::getline(puzzle_file, line))
    {
        if (line == "")
        {
            // trailing newline
            break;
        }

        std::size_t last_delimiter_position = line.rfind(" ");
        const std::string output_name = line.substr(last_delimiter_position+1);
        
        std::size_t previous_delimiter_position = 0;
        std::size_t next_delimiter_position = line.find(" ");
        const std::string first_word_in_line = line.substr(previous_delimiter_position, next_delimiter_position);
        
        previous_delimiter_position = next_delimiter_position + 1;
        next_delimiter_position = line.find(" ", previous_delimiter_position);

        std::unique_ptr<CircuitPart> circuit_part;

        if (next_delimiter_position == last_delimiter_position)
        {
            // buffer circuit
            const std::string input_wire = first_word_in_line;
            circuit_part = std::make_unique<CircuitPart>(&circuit_parts_map, OperationType::NoOperation, input_wire);
        }
        else if (first_word_in_line == "NOT")
        {
            const std::string input_wire = line.substr(previous_delimiter_position, next_delimiter_position-previous_delimiter_position);
            circuit_part = std::make_unique<CircuitPart>(&circuit_parts_map, OperationType::NotOperation, input_wire);
        }
        else 
        { 
            const std::string operation_type_name = line.substr(previous_delimiter_position, next_delimiter_position-previous_delimiter_position);

            OperationType operation_type;
            if (operation_type_name == "AND")
            {
                operation_type = OperationType::AndOperation;
            }
            else if (operation_type_name == "OR")
            {
                operation_type = OperationType::OrOperation;
            }
            else if (operation_type_name == "LSHIFT")
            {
                operation_type = OperationType::LeftShiftOperation;
            }
            else
            {
                operation_type = OperationType::RightShiftOperation;
            }

            const std::string first_input_wire = first_word_in_line;

            previous_delimiter_position = next_delimiter_position + 1;
            next_delimiter_position = line.find(" ", previous_delimiter_position);
            const std::string second_input_wire = line.substr(previous_delimiter_position, next_delimiter_position-previous_delimiter_position);

            circuit_part = std::make_unique<CircuitPart>(&circuit_parts_map, operation_type, first_input_wire, second_input_wire);

        }
        
        circuit_parts_map.insert({output_name, std::move(circuit_part)});
    }
}


void solve_example_file(std::unordered_map<std::string, std::unique_ptr<CircuitPart>> &circuit_parts_map) 
{
    for (const auto &circuit_part_map : circuit_parts_map)
    {
        uint16_t circuit_signal_output = circuit_part_map.second->join_circuit();
        std::cout << "The signal in wire " << circuit_part_map.first << " is " << circuit_signal_output << std::endl;
    }
}


uint16_t solve_first_part(std::unordered_map<std::string, std::unique_ptr<CircuitPart>> &circuit_parts_map) 
{
    const uint16_t full_circuit_signal_output = circuit_parts_map.at(TARGET_WIRE_NAME)->join_circuit();

    std::cout << "The signal in wire " << TARGET_WIRE_NAME << " is " << full_circuit_signal_output << std::endl;

    return full_circuit_signal_output;
}


void solve_second_part(std::unordered_map<std::string, std::unique_ptr<CircuitPart>> &circuit_parts_map, const uint16_t first_part_output)
{
    for (const auto &circuit_part_map : circuit_parts_map)
    {
        circuit_part_map.second->reset_circuit_output(); // an alternative to resetting could have been to deepcopy circuit_parts_map before solving first part
    }

    circuit_parts_map.at(WIRE_TO_OVERWRITE_NAME)->overwrite_output_value(first_part_output);

    const uint16_t overwritten_full_circuit_signal_output = circuit_parts_map.at(TARGET_WIRE_NAME)->join_circuit();

    std::cout << "The signal in wire " << TARGET_WIRE_NAME << " after overwritting wire " << WIRE_TO_OVERWRITE_NAME << " is " << overwritten_full_circuit_signal_output << std::endl;
}


int main(int argc, char* argv[]) 
{
    const std::string puzzle_file_name( argc==1 ? PUZZLE_INPUT_FILE_NAME : (argc==2 ? PUZZLE_EXAMPLE_INPUT_FILE_NAME : argv[2]) ); // give one argument to use the example file instead of the default one. Give a second argument and that file will be used instead
    const bool is_input_example_file = ((argc==2) or (argc>=4)) ? true : false; // Give one or at least a third argument and the file will be considered an example file

    std::ifstream puzzle_file(puzzle_file_name);
    if (puzzle_file.is_open() == false)
    {
        std::cerr << "Could not open file \"" << puzzle_file_name << "\"" << std::endl;
        return EXIT_FAILURE;
    }

    std::unordered_map<std::string, std::unique_ptr<CircuitPart>> circuit_parts_map;
    parse_puzzle_file(circuit_parts_map, puzzle_file);
    
    if (is_input_example_file == true)
    {
        solve_example_file(circuit_parts_map);
    }
    else
    {
        const uint16_t first_part_output = solve_first_part(circuit_parts_map);

        solve_second_part(circuit_parts_map, first_part_output);
    }

    
    return EXIT_SUCCESS;
}