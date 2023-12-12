package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"unicode"
)

const (
	puzzleInputFileName        = "day3.txt"
	puzzleExampleInputFileName = "day3_example.txt"

	notASymbolCharacter                                = '.'
	numberOfPartNumbersAGearHasToBeSurroundedWith uint = 2
)

type scannedNumberParameters struct {
	initialXPositionMinusOne int
	endingXPositionPlusOne   int
	value                    uint
}

func parsePuzzleFile(file *os.File) ([][]scannedNumberParameters, [][]int, error) {
	var listOfScannedNumbers [][]scannedNumberParameters
	listOfScannedNumbers = append(listOfScannedNumbers, nil) // add an initial empty row. This eases processing the list as a filter, avoiding the border cases
	var listOfSymbolsXPositions [][]int

	var fileScanner = bufio.NewScanner(file)
	for fileScanner.Scan() {
		var fileline = fileScanner.Text()

		var symbolsXPositionsInCurrentlyLine []int
		var scannedNumbersInCurrentLine []scannedNumberParameters
		var numberCurrentlyBeingScanned *scannedNumberParameters = nil

		for characterRuneIdx, currentCharacterRune := range fileline {
			if unicode.IsDigit(currentCharacterRune) {
				if numberCurrentlyBeingScanned == nil {
					numberCurrentlyBeingScanned = new(scannedNumberParameters)
					numberCurrentlyBeingScanned.initialXPositionMinusOne = characterRuneIdx - 1
					numberCurrentlyBeingScanned.value = uint(currentCharacterRune - '0')
				} else {
					numberCurrentlyBeingScanned.value = numberCurrentlyBeingScanned.value*10 + uint(currentCharacterRune-'0')
				}
			} else {
				if numberCurrentlyBeingScanned != nil {
					numberCurrentlyBeingScanned.endingXPositionPlusOne = characterRuneIdx
					scannedNumbersInCurrentLine = append(scannedNumbersInCurrentLine, *numberCurrentlyBeingScanned)
					numberCurrentlyBeingScanned = nil
				}

				if currentCharacterRune != notASymbolCharacter {
					symbolsXPositionsInCurrentlyLine = append(symbolsXPositionsInCurrentlyLine, characterRuneIdx)
				}
			}
		}

		if numberCurrentlyBeingScanned != nil {
			numberCurrentlyBeingScanned.endingXPositionPlusOne = len(fileline)
			scannedNumbersInCurrentLine = append(scannedNumbersInCurrentLine, *numberCurrentlyBeingScanned)
			numberCurrentlyBeingScanned = nil
		}

		listOfScannedNumbers = append(listOfScannedNumbers, scannedNumbersInCurrentLine)
		listOfSymbolsXPositions = append(listOfSymbolsXPositions, symbolsXPositionsInCurrentlyLine)
	}

	var err = fileScanner.Err()
	if err != nil {
		return nil, nil, err
	}

	listOfScannedNumbers = append(listOfScannedNumbers, nil) // add a final empty row. This eases processing the list as a filter, avoiding the border cases

	return listOfScannedNumbers, listOfSymbolsXPositions, nil
}

func getPartNumberSumFromNearNumbers(symbolXPosition int, scannedNumbers *[]scannedNumberParameters, checkIfNumberIsAdjacent func(int, scannedNumberParameters) bool) uint {
	var sumOfPartNumbers uint = 0
	var remadeSliceLength uint = 0 // the slice will be rewritten eliminating the already counted part numbers, so these are not counted again in another situation
	for _, scannedNumber := range *scannedNumbers {
		if checkIfNumberIsAdjacent(symbolXPosition, scannedNumber) == true {
			sumOfPartNumbers += scannedNumber.value
		} else {
			(*scannedNumbers)[remadeSliceLength] = scannedNumber
			remadeSliceLength += 1
		}
	}
	(*scannedNumbers) = (*scannedNumbers)[:remadeSliceLength] // remove already counted part numbers

	return sumOfPartNumbers
}

func checkIfUpperOrLowerNumberIsAdjacent(symbolXPosition int, scannedNumber scannedNumberParameters) bool {
	return symbolXPosition >= scannedNumber.initialXPositionMinusOne && symbolXPosition <= scannedNumber.endingXPositionPlusOne
}

func checkIfNeighbourNumberIsAdjacent(symbolXPosition int, scannedNumber scannedNumberParameters) bool {
	return symbolXPosition == scannedNumber.initialXPositionMinusOne || symbolXPosition == scannedNumber.endingXPositionPlusOne
}

func solveFirstPart(listOfScannedNumbers [][]scannedNumberParameters, listOfSymbolsXPositions [][]int) {
	var sumOfPartNumbers uint = 0

	for idx, symbolsXPositionsInCurrentRow := range listOfSymbolsXPositions {
		// for each symbol in the current row, check if the upper, central or lower contain a part number
		for _, symbolXPosition := range symbolsXPositionsInCurrentRow {
			sumOfPartNumbers += getPartNumberSumFromNearNumbers(symbolXPosition, &(listOfScannedNumbers[idx]), checkIfUpperOrLowerNumberIsAdjacent)   // check the upper row
			sumOfPartNumbers += getPartNumberSumFromNearNumbers(symbolXPosition, &(listOfScannedNumbers[idx+1]), checkIfUpperOrLowerNumberIsAdjacent) // check the current row
			sumOfPartNumbers += getPartNumberSumFromNearNumbers(symbolXPosition, &(listOfScannedNumbers[idx+2]), checkIfUpperOrLowerNumberIsAdjacent) // check the lower row
		}
	}

	fmt.Println("The sum of all part numbers is:", sumOfPartNumbers)
}

func getGearRatioFromNearNumbers(symbolXPosition int, scannedNumbers []scannedNumberParameters, checkIfNumberIsAdjacent func(int, scannedNumberParameters) bool) (uint, uint) {
	var gearRatio uint = 1
	var NumberOfAdjacentNumbers uint = 0
	for _, scannedNumber := range scannedNumbers {
		if checkIfNumberIsAdjacent(symbolXPosition, scannedNumber) == true {
			gearRatio *= scannedNumber.value
			NumberOfAdjacentNumbers += 1
		}
	}
	return gearRatio, NumberOfAdjacentNumbers
}

func solveSecondPart(listOfScannedNumbers [][]scannedNumberParameters, listOfSymbolsXPositions [][]int) {
	var sumOfGearRatios uint = 0

	for idx, symbolsXPositionsInCurrentRow := range listOfSymbolsXPositions {
		// for each symbol in the current row, check if the upper, central or lower contain a part number
		for _, symbolXPosition := range symbolsXPositionsInCurrentRow {
			var upperRowGearRatio, NumberOfUpperRowAdjacentNumbers = getGearRatioFromNearNumbers(symbolXPosition, listOfScannedNumbers[idx], checkIfUpperOrLowerNumberIsAdjacent)    // check the upper row
			var centralRowGearRatio, NumberOfCentralRowAdjacentNumbers = getGearRatioFromNearNumbers(symbolXPosition, listOfScannedNumbers[idx+1], checkIfNeighbourNumberIsAdjacent) // check the current row
			var lowerrRowGearRatio, NumberOfLowerRowAdjacentNumbers = getGearRatioFromNearNumbers(symbolXPosition, listOfScannedNumbers[idx+2], checkIfUpperOrLowerNumberIsAdjacent) // check the lower row

			if (NumberOfUpperRowAdjacentNumbers + NumberOfCentralRowAdjacentNumbers + NumberOfLowerRowAdjacentNumbers) == numberOfPartNumbersAGearHasToBeSurroundedWith {
				sumOfGearRatios += upperRowGearRatio * centralRowGearRatio * lowerrRowGearRatio
			}
		}
	}

	fmt.Println("The sum of all gear ratios is:", sumOfGearRatios)
}

func main() {
	var filePath string
	switch len(os.Args) {
	case 1:
		filePath = puzzleInputFileName
	case 2:
		filePath = puzzleExampleInputFileName
	default:
		filePath = os.Args[2]
	}

	var puzzleFile, err = os.Open(filePath)
	if err != nil {
		log.Fatal(err)
	}
	defer func() {
		if closing_error := puzzleFile.Close(); closing_error != nil {
			log.Panicln(closing_error)
		}
	}()

	listOfScannedNumbers, listOfSymbolsXPositions, err := parsePuzzleFile(puzzleFile)
	if err != nil {
		log.Fatal(err)
	}

	// solveFirstPart modifies listOfScannedNumbers, so making a copy of it is necessary. A smarter alternative would be just to execute the solveSecondPart before, but for meticulous organization reasons, an alternative is used.
	copyOfListOfScannedNumbers := make([][]scannedNumberParameters, len(listOfScannedNumbers))
	for idx, scannedNumbers := range listOfScannedNumbers {
		copyOfListOfScannedNumbers[idx] = make([]scannedNumberParameters, len(scannedNumbers))
		copy(copyOfListOfScannedNumbers[idx], scannedNumbers) // copy the contents of the inner slice to the new inner slice
	}

	solveFirstPart(copyOfListOfScannedNumbers, listOfSymbolsXPositions)
	solveSecondPart(listOfScannedNumbers, listOfSymbolsXPositions)
}
