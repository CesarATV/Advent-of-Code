package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"strings"
)

const (
	puzzleInputFileName        = "day4.txt"
	puzzleExampleInputFileName = "day4_example.txt"
)

func parsePuzzleFile(puzzleFilePath string) ([]map[string]bool, [][]string, error) {
	var puzzleFile, err = os.Open(puzzleFilePath)
	if err != nil {
		return nil, nil, err
	}
	defer func() {
		if err = puzzleFile.Close(); err != nil {
			log.Println(err)
		}
	}()

	var listOfScratchedNumbers []map[string]bool
	var listOfWinningNumbers [][]string

	var fileScanner = bufio.NewScanner(puzzleFile)
	for fileScanner.Scan() {
		var fileLine = fileScanner.Text()

		var scratchcard = strings.Split(fileLine, ": ")[1]
		var scratchedNumbersAndWinningNumbers = strings.Split(scratchcard, "| ")

		var scratchedNumbersSplit = strings.Fields(scratchedNumbersAndWinningNumbers[0])
		var scratchedNumbers = make(map[string]bool, len(scratchedNumbersSplit))

		for _, scratchedNumber := range scratchedNumbersSplit {
			scratchedNumbers[scratchedNumber] = true
		}
		listOfScratchedNumbers = append(listOfScratchedNumbers, scratchedNumbers)

		var winningNumbersSplit = strings.Fields(scratchedNumbersAndWinningNumbers[1])
		var winningNumbers = make([]string, len(winningNumbersSplit))
		for idx, winningNumber := range winningNumbersSplit {
			winningNumbers[idx] = winningNumber
		}
		listOfWinningNumbers = append(listOfWinningNumbers, winningNumbers)
	}

	err = fileScanner.Err()
	if err != nil {
		return nil, nil, err
	}

	return listOfScratchedNumbers, listOfWinningNumbers, nil
}

func solveFirstPart(listOfScratchedNumbers []map[string]bool, listOfWinningNumbers [][]string) {
	var nPoints uint = 0
	for idx, scratchedNumbers := range listOfScratchedNumbers {
		var nMatchingNumbers = 0
		for _, winningNumber := range listOfWinningNumbers[idx] {
			var _, isWinningNumberAScratchedOne = scratchedNumbers[winningNumber]
			if isWinningNumberAScratchedOne == true {
				nMatchingNumbers++
			}
		}

		if nMatchingNumbers > 0 {
			nPoints += uint(math.Pow(2, float64(nMatchingNumbers-1)))
		}
	}

	fmt.Println("The cards are worth a total of", nPoints, "points")
}

func solveSecondPart(listOfScratchedNumbers []map[string]bool, listOfWinningNumbers [][]string) {
	var totalNumberOfScratchcards uint = 0

	var sliceOfNumberOfScratchcards = make([]uint, len(listOfScratchedNumbers)) // the slice keeps track of the total number of scratchcards
	for idx := range sliceOfNumberOfScratchcards {
		sliceOfNumberOfScratchcards[idx] = 1 // at the beginning there is a coppy
	}

	for currentCardIdx, scratchedNumbers := range listOfScratchedNumbers {
		var nMatchingNumbers = 0
		for _, winningNumber := range listOfWinningNumbers[currentCardIdx] {
			var _, isWinningNumberAScratchedOne = scratchedNumbers[winningNumber]
			if isWinningNumberAScratchedOne == true {
				nMatchingNumbers++
			}
		}

		// In order to avoid writting out of the slice sliceOfNumberOfScratchcards, make sure to cut the value of nMatchingNumbers. This is because it is assumemed that there are no more scratchcards than the ones one begins with, as it would be impossible to play with them. It does seem that the puzzle input was designed so this case would not happen, making the following lines unnecessary in practice
		if (currentCardIdx + nMatchingNumbers + 1) > len(sliceOfNumberOfScratchcards) {
			nMatchingNumbers = len(sliceOfNumberOfScratchcards) - currentCardIdx
		}

		var nCopiesOfCurrentScratchcard = sliceOfNumberOfScratchcards[currentCardIdx]
		// add the won scratchcards to sliceOfNumberOfScratchcards. One scratchcard is won for each copy of the current scratchcard
		for wonExtraCopyIdx := 1; wonExtraCopyIdx < (nMatchingNumbers + 1); wonExtraCopyIdx++ {
			sliceOfNumberOfScratchcards[currentCardIdx+wonExtraCopyIdx] += nCopiesOfCurrentScratchcard
		}

		totalNumberOfScratchcards += nCopiesOfCurrentScratchcard
	}

	fmt.Println("One ends up with a total of", totalNumberOfScratchcards, "scratchcards")
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

	listOfScratchedNumbers, listOfWinningNumbers, err := parsePuzzleFile(puzzleFilePath)
	if err != nil {
		log.Fatal(err)
	}

	solveFirstPart(listOfScratchedNumbers, listOfWinningNumbers)
	solveSecondPart(listOfScratchedNumbers, listOfWinningNumbers)
}
