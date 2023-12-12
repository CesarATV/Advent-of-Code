import argparse

PUZZLE_INPUT_FILE_NAME = "puzzle_inputs/day7.txt"
PUZZLE_EXAMPLE_INPUT_FILE_NAME = "puzzle_inputs/day7_example.txt"

MAXIMUM_ALLOWED_SIZE = 100000

NECESSARY_SPACE = 30000000
MAXIMUM_SPACE = 70000000


def parse_file_name():
    parser = argparse.ArgumentParser(description="Advent of Code Day 7: No Space Left On Device")
    parser.add_argument("file_name", type=str, nargs='*', help="if no arguments are given, use default (hardcoded) file path. If one argument is given, use default example path. If at least 2 arguments are given, use second as path")
    args = parser.parse_args()
    if args.file_name == []:
        return PUZZLE_INPUT_FILE_NAME
    elif len(args.file_name) == 1:
        return PUZZLE_EXAMPLE_INPUT_FILE_NAME
    else:
        return args.file_name[1]



class DeviceDirectory():
    def __init__(self, lines):
        self.lines = lines
        self.used_space = None
    
    def prepare_subfolder_size_count(self):
        self.current_path = "" # variable currently not used for anything practical in the code, except for debugging
        self.line_idx = 0
        self.accumulated_sizes = 0


    # As this function is recursive, it benefits from using variables from inside the class, to avoid copying them continuously
    def subfolder_size_count(self):
        current_size = 0
        while True:
            line = self.lines[self.line_idx]
            self.line_idx += 1 
            if "$ cd" in line:
                if "$ cd .." in line:
                    if(current_size <= MAXIMUM_ALLOWED_SIZE):
                        self.accumulated_sizes += current_size
                    self.current_path = self.current_path[:self.current_path.rfind("/")]
                    return current_size
                else:
                    if line[len("$ cd "):] != "/":
                        self.current_path = self.current_path + "/" + line[len("$ cd "):]
                    subfolder_size = self.subfolder_size_count()
                    current_size += subfolder_size
            elif "dir " not in line and "$ ls" not in line:
                current_size += int(line.split(" ")[0])

            if self.line_idx >= len(self.lines):
                if current_size <= MAXIMUM_ALLOWED_SIZE:
                    self.accumulated_sizes += current_size
                self.current_path = self.current_path[:self.current_path.rfind("/")]
                return current_size


    def prepare_subfolder_search_for_space(self, space_to_delete, proposed_size_to_delete):
        self.current_path = "" # variable currently not used for anything practical in the code, except for debugging
        self.line_idx = 0
        self.space_to_delete = space_to_delete
        self.proposed_size_to_delete = proposed_size_to_delete


    def subfolder_search_for_space(self):
        current_size = 0
        while True:
            line = self.lines[self.line_idx]
            self.line_idx += 1 
            if "$ cd" in line:
                if "$ cd .." in line:
                    if current_size >= self.space_to_delete and current_size < self.proposed_size_to_delete:
                        self.proposed_size_to_delete = current_size
                    self.current_path = self.current_path[:self.current_path.rfind("/")]
                    return current_size
                else:
                    if line[len("$ cd "):] != "/":
                        self.current_path = self.current_path + "/" + line[len("$ cd "):]
                    subfolder_size = self.subfolder_search_for_space()
                    current_size += subfolder_size
            elif "dir " not in line and "$ ls" not in line:
                current_size += int(line.split(" ")[0])

            if self.line_idx >= len(self.lines):
                if current_size >= self.space_to_delete and current_size < self.proposed_size_to_delete:
                    self.proposed_size_to_delete = current_size
                self.current_path = self.current_path[:self.current_path.rfind("/")]
                return current_size



def solve_first_part(device_directory):
    device_directory.prepare_subfolder_size_count()
    device_directory.used_space = device_directory.subfolder_size_count()
    print("The added size of the directories with a size of at most", MAXIMUM_ALLOWED_SIZE, "is", device_directory.accumulated_sizes)
 

def solve_second_part(device_directory):
    if device_directory.used_space == None: # this variable should have set already in the first part
        device_directory.prepare_recursive_search()
        device_directory.used_space = device_directory.subfolder_size_count()

    space_to_delete = NECESSARY_SPACE - (MAXIMUM_SPACE - device_directory.used_space)
    if space_to_delete == 0:  
        print("It is not necessary to delete a folder, there is enough space left")

    else:
        device_directory.prepare_subfolder_search_for_space(space_to_delete, MAXIMUM_SPACE)
        device_directory.subfolder_search_for_space()

        if space_to_delete > NECESSARY_SPACE:
            print("No folder big enough to delete was found, at most one with size", device_directory.proposed_size_to_delete)
        else:
            print("It is proposed to delete a folder with size", device_directory.proposed_size_to_delete)
        
        

def main(file_name): 
    with open(file_name) as file:
        lines = file.read().splitlines()
    while lines[-1] == "": # remove last empty lines, if any. They do not add information and can cause confusion
        lines.pop()

    device_directory = DeviceDirectory(lines)

    solve_first_part(device_directory)
    solve_second_part(device_directory)


if __name__ == "__main__":
    main(parse_file_name())


