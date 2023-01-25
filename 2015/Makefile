CXX=g++
CXXFLAGS= -Wall -Wextra

all: day1 day2 day3 day5 day6

day1: day1.cpp
	$(CXX) $< -o $@ $(CXXFLAGS)

day2: day2.cpp
	$(CXX) $< -o $@ $(CXXFLAGS)

day3: day3.cpp
	$(CXX) $< -o $@ $(CXXFLAGS)

# day4: day4.cpp
# 	$(CXX) $< -o $(TARGET_FOLDER)$@ $(CXXFLAGS)

day5: day5.cpp
	$(CXX) $< -o $@ $(CXXFLAGS)

day6: day6.cpp
	$(CXX) $< -o $@ $(CXXFLAGS)

# day7: day7.cpp
# 	$(CXX) $< -o $(TARGET_FOLDER)$@ $(CXXFLAGS)

# day8: day8.cpp
# 	$(CXX) $< -o $(TARGET_FOLDER)$@ $(CXXFLAGS)

# day9: day9.cpp
# 	$(CXX) $< -o $(TARGET_FOLDER)$@ $(CXXFLAGS)

# day10: day10.cpp
# 	$(CXX) $< -o $(TARGET_FOLDER)$@ $(CXXFLAGS)


# $(info $(shell mkdir -p $(DIRS)))

.PHONY: clean

clean:
	rm -f day1 day2 day3 day5 day6 *.o