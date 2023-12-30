/*
The first part is solved checking the corresponding location number to each seed by looking into the mappings of each element
The second part can be solved similarly to the first part, iterating for every seed. This, however, would take too much time, so a probably faster solution would be to iterate in the opposite order, looking for a seed number from a location number, beginning at the lowest possible location, 0. and stopping once a seed is found. This solution, while faster, is still too slow, taking more than 1 minute to compute
The implemented solution for the second part looks through all possible location-number ranges, processing the ranges instead of each number individually. This procudes also possible seed-number ranges, and once one of these matches a seed, it is possible to find again the location number corresponding to it. The location-number ranges start at the lowest possible location, 0.
*/
package main

import (
	"bufio"
	"errors"
	"fmt"
	"log"
	"math"
	"os"
	"slices"
	"strconv"
	"strings"
)

const (
	puzzleInputFileName        = "day5.txt"
	puzzleExampleInputFileName = "day5_example.txt"

	numberOfDifferentMappingsBetweenObjects = 7
)

type relationshipBetweenElementsStruct struct {
	destinationRangeStart int
	destinationRangeEnd   int // non-inclusive range
	sourceRangeStart      int
	sourceRangeEnd        int // non-inclusive range
}

type limitStruct struct {
	begins int
	ends   int // non-inclusive range
}

func parsePuzzleFile(puzzleFilePath string) ([]int, []limitStruct, [numberOfDifferentMappingsBetweenObjects][]relationshipBetweenElementsStruct, error) {
	var puzzleFile, err = os.Open(puzzleFilePath)
	if err != nil {
		return nil, nil, [numberOfDifferentMappingsBetweenObjects][]relationshipBetweenElementsStruct{}, err
	}
	defer func() {
		if err = puzzleFile.Close(); err != nil {
			log.Println(err)
		}
	}()

	var fileScanner = bufio.NewScanner(puzzleFile)
	if fileScanner.Scan() == false {
		return nil, nil, [numberOfDifferentMappingsBetweenObjects][]relationshipBetweenElementsStruct{}, errors.New("The puzzle file is empty")
	}

	var seedsSplit = strings.Split(fileScanner.Text(), ": ")[1]
	var seeds []int
	for _, seedString := range strings.Fields(seedsSplit) {
		seed_int, err := strconv.Atoi(seedString)
		if err != nil {
			return nil, nil, [numberOfDifferentMappingsBetweenObjects][]relationshipBetweenElementsStruct{}, err
		}
		seeds = append(seeds, seed_int)
	}

	var seedLimits = make([]limitStruct, len(seeds)/2)
	for idx := 0; idx < len(seeds)/2; idx++ {
		seedLimits[idx].begins = seeds[idx*2]
		seedLimits[idx].ends = seedLimits[idx].begins + seeds[idx*2+1]
	}

	var elementToElementMappings = [numberOfDifferentMappingsBetweenObjects][]relationshipBetweenElementsStruct{}
	var currentElementMappingIdx uint
	for fileScanner.Scan() {
		var puzzleLine = fileScanner.Text()

		switch puzzleLine {
		case "", "seed-to-soil map:":
			continue
		case "soil-to-fertilizer map:", "fertilizer-to-water map:", "water-to-light map:", "light-to-temperature map:", "temperature-to-humidity map:", "humidity-to-location map:":
			currentElementMappingIdx++
		default:
			var sliceOfRelationshipBetweenElements = strings.Fields(puzzleLine)

			destinationRangeStart, err := strconv.Atoi(sliceOfRelationshipBetweenElements[0])
			if err != nil {
				return nil, nil, [numberOfDifferentMappingsBetweenObjects][]relationshipBetweenElementsStruct{}, err
			}
			sourceRangeStart, err := strconv.Atoi(sliceOfRelationshipBetweenElements[1])
			if err != nil {
				return nil, nil, [numberOfDifferentMappingsBetweenObjects][]relationshipBetweenElementsStruct{}, err
			}
			rangeLength, err := strconv.Atoi(sliceOfRelationshipBetweenElements[2])
			if err != nil {
				return nil, nil, [numberOfDifferentMappingsBetweenObjects][]relationshipBetweenElementsStruct{}, err
			}
			var sourceRangeEnd = sourceRangeStart + rangeLength
			var destinationRangeEnd = destinationRangeStart + rangeLength

			var lineRelationshipBetweenElements = relationshipBetweenElementsStruct{destinationRangeStart, destinationRangeEnd, sourceRangeStart, sourceRangeEnd}
			elementToElementMappings[currentElementMappingIdx] = append(elementToElementMappings[currentElementMappingIdx], lineRelationshipBetweenElements)
		}
	}

	err = fileScanner.Err()
	if err != nil {
		return nil, nil, [numberOfDifferentMappingsBetweenObjects][]relationshipBetweenElementsStruct{}, err
	}

	return seeds, seedLimits, elementToElementMappings, nil
}

func findDestinationFromSourceInMapping(source int, relationshipMapping relationshipBetweenElementsStruct) (int, bool) {
	if source >= relationshipMapping.sourceRangeStart && source < relationshipMapping.sourceRangeEnd {
		var destination = relationshipMapping.destinationRangeStart + (source - relationshipMapping.sourceRangeStart)
		return destination, true
	}
	return 0, false
}

func findDestinationFromSourceInAllMappings(source int, elementToElementMappings [numberOfDifferentMappingsBetweenObjects][]relationshipBetweenElementsStruct) int {
	for _, elementToElementMapping := range elementToElementMappings {
		for _, partOfElementToElementMapping := range elementToElementMapping {
			var destination, wasDestinationFound = findDestinationFromSourceInMapping(source, partOfElementToElementMapping)
			if wasDestinationFound == true {
				source = destination
				break
			}
		}
		// there is no need to consider the case in which no destination was found in the mappings. When that happens, the source is equal to the destination, so there is no need to modify the value of the variable source again
	}

	return source
}

func solveFirstPart(seeds []int, elementToElementMappings [numberOfDifferentMappingsBetweenObjects][]relationshipBetweenElementsStruct) {
	var lowestLocation = math.MaxInt
	for _, source := range seeds {
		var destination = findDestinationFromSourceInAllMappings(source, elementToElementMappings)

		// After finishing all iterations in the different elementToElementMappings, the source becomes the desired location
		if destination < lowestLocation {
			lowestLocation = destination
		}
	}

	fmt.Println("The lowest location number corresponding to any initial seed number is", lowestLocation)
}

// if the first range-start is bigger rank than the second, 1 is returned. If it is smaller, -1 is returned. 0 if both are equal (something that should not happen)
func compareAccordingToDestinationRangeStart(firstrelationshipBetweenElementsStruct relationshipBetweenElementsStruct, secondrelationshipBetweenElementsStruct relationshipBetweenElementsStruct) int {
	if firstrelationshipBetweenElementsStruct.destinationRangeStart > secondrelationshipBetweenElementsStruct.destinationRangeStart {
		return 1
	} else if firstrelationshipBetweenElementsStruct.destinationRangeStart < secondrelationshipBetweenElementsStruct.destinationRangeStart {
		return -1
	} else {
		return 0
	}
}

func fillGapsBetweenElementMappings(elementToElementMappings [numberOfDifferentMappingsBetweenObjects][]relationshipBetweenElementsStruct) [numberOfDifferentMappingsBetweenObjects][]relationshipBetweenElementsStruct {
	var extendedElementToElementMappings = [numberOfDifferentMappingsBetweenObjects][]relationshipBetweenElementsStruct{}
	for elementMappingIdx, elementMapping := range elementToElementMappings {
		slices.SortFunc[[]relationshipBetweenElementsStruct](elementMapping, compareAccordingToDestinationRangeStart)

		var previous = 0
		for _, partOfElementToElementMapping := range elementToElementMappings[elementMappingIdx] {
			if partOfElementToElementMapping.destinationRangeStart != previous {
				var newrelationshipBetweenElementsStruct = relationshipBetweenElementsStruct{destinationRangeStart: previous, destinationRangeEnd: partOfElementToElementMapping.destinationRangeStart, sourceRangeStart: previous, sourceRangeEnd: partOfElementToElementMapping.destinationRangeStart}
				extendedElementToElementMappings[elementMappingIdx] = append(extendedElementToElementMappings[elementMappingIdx], newrelationshipBetweenElementsStruct)
			}

			extendedElementToElementMappings[elementMappingIdx] = append(extendedElementToElementMappings[elementMappingIdx], partOfElementToElementMapping)

			previous = partOfElementToElementMapping.destinationRangeEnd
		}

		extendedElementToElementMappings[elementMappingIdx] = append(extendedElementToElementMappings[elementMappingIdx], relationshipBetweenElementsStruct{destinationRangeStart: previous, destinationRangeEnd: math.MaxInt, sourceRangeStart: previous, sourceRangeEnd: math.MaxInt})
	}
	return extendedElementToElementMappings
}

/*
Note that because this function looks for the seeds (the first source element) from the location number (the final destination element), the name of the structs are reversed. That means that a destination element tries to look for its source element
*/
func solveSecondPart(seedLimits []limitStruct, elementToElementMappings [numberOfDifferentMappingsBetweenObjects][]relationshipBetweenElementsStruct) {
	var extendedElementToElementMappings = fillGapsBetweenElementMappings(elementToElementMappings) // as given in the input file, the ranges do not contain explicetely all the numbers, from 0 to infinite (or, more technically, math.MaxInt), for its destination and source elements. This function makes sures to  add them, in order to ease processing them

	var hasLocationNumberBeenFound bool
	var smallestLocationNumber = math.MaxInt
	for _, locationNumberMappingElement := range extendedElementToElementMappings[numberOfDifferentMappingsBetweenObjects-1] {
		var currentLimitToCheck = limitStruct{begins: locationNumberMappingElement.destinationRangeStart, ends: locationNumberMappingElement.destinationRangeEnd}

		var limitsToCheckInThisElement = []limitStruct{}
		var limitsToCheckInNextElement = []limitStruct{currentLimitToCheck}
		for idx := numberOfDifferentMappingsBetweenObjects - 1; idx >= 0; idx-- {
			limitsToCheckInThisElement, limitsToCheckInNextElement = limitsToCheckInNextElement, limitsToCheckInThisElement

			var partOfElementMappingIdx = 0
			for len(limitsToCheckInThisElement) > 0 {
				var currentLimitToCheck = &limitsToCheckInThisElement[len(limitsToCheckInThisElement)-1]
				var partOfElementToElementMapping = extendedElementToElementMappings[idx][partOfElementMappingIdx]
				partOfElementMappingIdx++

				if currentLimitToCheck.begins < partOfElementToElementMapping.destinationRangeStart || currentLimitToCheck.begins >= partOfElementToElementMapping.destinationRangeEnd {
					continue
				}

				limitsToCheckInThisElement = limitsToCheckInThisElement[:len(limitsToCheckInThisElement)-1] // pop element
				partOfElementMappingIdx = 0

				var inputLimitForParent limitStruct
				if currentLimitToCheck.ends <= partOfElementToElementMapping.destinationRangeEnd {
					inputLimitForParent.begins = partOfElementToElementMapping.sourceRangeStart + (currentLimitToCheck.begins - partOfElementToElementMapping.destinationRangeStart)
					inputLimitForParent.ends = inputLimitForParent.begins + (currentLimitToCheck.ends - currentLimitToCheck.begins)

				} else {
					inputLimitForParent.begins = partOfElementToElementMapping.sourceRangeStart + (currentLimitToCheck.begins - partOfElementToElementMapping.destinationRangeStart)
					inputLimitForParent.ends = partOfElementToElementMapping.sourceRangeEnd
					limitsToCheckInThisElement = append(limitsToCheckInThisElement, limitStruct{begins: partOfElementToElementMapping.destinationRangeEnd, ends: currentLimitToCheck.ends})
				}
				limitsToCheckInNextElement = append(limitsToCheckInNextElement, inputLimitForParent)
			}
		}

		for _, possibleSeedLimits := range limitsToCheckInNextElement {
			for _, seedLimit := range seedLimits {
				if seedLimit.begins <= possibleSeedLimits.ends && seedLimit.ends >= possibleSeedLimits.begins {
					hasLocationNumberBeenFound = true
					var locationNumber = findDestinationFromSourceInAllMappings(possibleSeedLimits.begins, elementToElementMappings)
					if locationNumber < smallestLocationNumber {
						smallestLocationNumber = locationNumber
					}
				}
			}

		}
		if hasLocationNumberBeenFound == true {
			break
		}
	}

	if hasLocationNumberBeenFound == false {
		fmt.Println("Could not find corresponding seed. This should not happen")
	} else {
		fmt.Println("Consdering ranges of seed numbers, the lowest location number corresponding to any initial seed number is", smallestLocationNumber)
	}
}

func main() {
	var puzzleFilePath string
	switch len(os.Args) {
	case 1:
		puzzleFilePath = puzzleInputFileName
	case 2:
		puzzleFilePath = puzzleExampleInputFileName
	default:
		puzzleFilePath = os.Args[2]
	}

	seeds, seedLimits, elementToElementMappings, err := parsePuzzleFile(puzzleFilePath)
	if err != nil {
		log.Fatal(err)
	}

	solveFirstPart(seeds, elementToElementMappings)
	solveSecondPart(seedLimits, elementToElementMappings)
}
