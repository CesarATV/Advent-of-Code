/*
The first part is solved in a straightforward way, just implementing the HASH algorithm as described.
The second part can be also solved in a very straightforward way using a sorted map to keep track of the given operations. However, Go does not offer a sorted map in the standard library, so an quickly-made unorthodox implementation was used instead
*/

package main

import (
	"bufio"
	"cmp"
	"errors"
	"fmt"
	"log"
	"os"
	"slices"
	"strconv"
	"strings"
)

const (
	puzzleInputFileName        = "day15.txt"
	puzzleExampleInputFileName = "day15_example.txt"
)

type valueAndOrderIdx struct {
	mapValue    int
	mapOrderIdx int // value used to keep track of the order of the keys in an unordered map. The value does not reflect the actual number element in the map, just its order with respect to other elements
}

type sortableMap struct {
	mapOfValuesAndOrderIdx              map[string]valueAndOrderIdx
	numberOfTimesAnElementsHasBeenAdded int // will be used to keep a track of the order of the keys in the maps
}

func (sortableMapInstance *sortableMap) deleteKey(keyToDelete string) {
	delete(sortableMapInstance.mapOfValuesAndOrderIdx, keyToDelete)
}

func (sortableMapInstance *sortableMap) addElement(keyToAdd string, valueToAdd int) {
	if _, doesKeyExist := sortableMapInstance.mapOfValuesAndOrderIdx[keyToAdd]; doesKeyExist == false {
		sortableMapInstance.mapOfValuesAndOrderIdx[keyToAdd] = valueAndOrderIdx{valueToAdd, sortableMapInstance.numberOfTimesAnElementsHasBeenAdded}
		sortableMapInstance.numberOfTimesAnElementsHasBeenAdded++ // this ensures that two elements will never have the same index showing when the element was added
	} else {
		sortableMapInstance.mapOfValuesAndOrderIdx[keyToAdd] = valueAndOrderIdx{valueToAdd, sortableMapInstance.mapOfValuesAndOrderIdx[keyToAdd].mapOrderIdx}
	}
}

func (sortableMapInstance *sortableMap) getOrderIdxAndValues() ([]int, map[int]int) {
	var orderIdxSlice = []int{}
	var idxToValuesMap = map[int]int{}

	for _, value := range sortableMapInstance.mapOfValuesAndOrderIdx {
		orderIdxSlice = append(orderIdxSlice, value.mapOrderIdx)
		idxToValuesMap[value.mapOrderIdx] = value.mapValue
	}

	slices.SortFunc[[]int](orderIdxSlice, cmp.Compare)

	return orderIdxSlice, idxToValuesMap
}

func parsePuzzleFile(puzzleFilePath string) (string, error) {
	puzzleFile, err := os.Open(puzzleFilePath)
	if err != nil {
		return "", err
	}
	defer func() {
		if err = puzzleFile.Close(); err != nil {
			log.Println(err)
		}
	}()

	var fileScanner = bufio.NewScanner(puzzleFile)
	if fileScanner.Scan() == false {
		return "", errors.New("The puzzle file is empty")
	}

	var initializationSequence = fileScanner.Text()

	err = fileScanner.Err()
	if err != nil {
		return "", err
	}

	return initializationSequence, nil
}

func runHASHAlgorithm(inputString string) uint {
	var HASHAlgorithmResult uint = 0
	for _, currentCharacter := range inputString {
		HASHAlgorithmResult += uint(currentCharacter)
		HASHAlgorithmResult *= 17
		HASHAlgorithmResult %= 256
	}
	return HASHAlgorithmResult
}

func solveFirstPart(initializationSequence string) {

	var sumOfHASHAlgorithmResults uint = 0
	for _, currentString := range strings.Split(initializationSequence, ",") {
		sumOfHASHAlgorithmResults += runHASHAlgorithm(currentString)
	}
	fmt.Println("The sum of the results from applying the HASH algorithm is", sumOfHASHAlgorithmResults)
}

func solveSecondPart(initializationSequence string) error {

	var boxSeries = map[int]*sortableMap{}
	for _, currentStepString := range strings.Split(initializationSequence, ",") {

		var labelAndFocalLength = strings.FieldsFunc(currentStepString, func(r rune) bool {
			return r == '=' || r == '-'
		})

		var label = labelAndFocalLength[0]
		var boxNumber = int(runHASHAlgorithm(label))

		if len(labelAndFocalLength) == 1 {
			// operation was to remove an element
			if _, doesKeyExist := boxSeries[boxNumber]; doesKeyExist == true {
				boxSeries[boxNumber].deleteKey(label)
			}

		} else {
			// operation was to add an element
			if _, doesKeyExist := boxSeries[boxNumber]; doesKeyExist == false {
				boxSeries[boxNumber] = &sortableMap{map[string]valueAndOrderIdx{}, 0}
			}

			focalLength, err := strconv.Atoi(labelAndFocalLength[1])
			if err != nil {
				return err
			}

			boxSeries[boxNumber].addElement(label, focalLength)
		}
	}

	var totalFocusingPower int = 0
	for boxNumber, currentBox := range boxSeries {
		var orderIdxSlice, idxToValuesMap = currentBox.getOrderIdxAndValues()
		for slotIdx, orderIdx := range orderIdxSlice {
			var focalLength = idxToValuesMap[orderIdx]
			totalFocusingPower += (boxNumber + 1) * (slotIdx + 1) * focalLength
		}
	}

	fmt.Println("The focusing power of the resulting lens configuration is", totalFocusingPower)
	return nil
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

	initializationSequence, err := parsePuzzleFile(puzzleFilePath)
	if err != nil {
		log.Fatal(err)
	}

	solveFirstPart(initializationSequence)
	err = solveSecondPart(initializationSequence)
	if err != nil {
		log.Fatal(err)
	}
}
