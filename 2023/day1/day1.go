package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"strings"
	"unicode"
)

const (
	puzzleInputFileName        = "day1.txt"
	puzzleExampleInputFileName = "day1_example.txt"
)

func solveFirstPart(fileLines []string) {
	var sumOfCalibrationValues uint = 0
	for _, fileLine := range fileLines {
		var firstDigit uint
		for _, lineRune := range fileLine {
			if unicode.IsDigit(lineRune) {
				firstDigit = uint(lineRune - '0')
				break
			}
		}

		var lastDigit uint
		for idx := len(fileLine) - 1; idx >= 0; idx-- { // iterate in reverse order
			if unicode.IsDigit(rune(fileLine[idx])) {
				lastDigit = uint(fileLine[idx] - '0')
				break
			}
		}

		var calibrationValue = firstDigit*10 + lastDigit
		sumOfCalibrationValues += calibrationValue

	}
	fmt.Println("The sum of the calibration values is", sumOfCalibrationValues)
}

func solveSecondPart(fileLines []string) {
	var sumOfCalibrationValues = 0

	var desiredDigitStrings = []string{"1", "2", "3", "4", "5", "6", "7", "8", "9", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"} // zero is not considered in the inputs
	var desiredDigitStringsToInt = map[string]int{
		"1":     1,
		"2":     2,
		"3":     3,
		"4":     4,
		"5":     5,
		"6":     6,
		"7":     7,
		"8":     8,
		"9":     9,
		"one":   1,
		"two":   2,
		"three": 3,
		"four":  4,
		"five":  5,
		"six":   6,
		"seven": 7,
		"eight": 8,
		"nine":  9,
	}

	for _, fileLine := range fileLines {
		var smallestFirstDigitPosition = math.MaxInt
		var firstDigit int
		for _, possibleDigitString := range desiredDigitStrings {
			var substringMatchPosition = strings.Index(fileLine, possibleDigitString)
			if substringMatchPosition == -1 {
				continue
			} else if substringMatchPosition < smallestFirstDigitPosition {
				smallestFirstDigitPosition = substringMatchPosition
				firstDigit = desiredDigitStringsToInt[possibleDigitString]
			}
		}

		var biggestLastDigitPosition = -1
		var lastDigit int
		for _, possibleDigitString := range desiredDigitStrings {
			var substringMatchPosition = strings.LastIndex(fileLine, possibleDigitString)
			if substringMatchPosition > biggestLastDigitPosition {
				biggestLastDigitPosition = substringMatchPosition
				lastDigit = desiredDigitStringsToInt[possibleDigitString]
			}
		}

		var calibrationValue = firstDigit*10 + lastDigit
		sumOfCalibrationValues += calibrationValue

	}
	fmt.Println("Considering spelled-out letters, the sum of the calibration values is", sumOfCalibrationValues)
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

	var puzzleFile, err = os.Open(puzzleFilePath)
	if err != nil {
		log.Fatal(err)
	}
	defer func() {
		if err = puzzleFile.Close(); err != nil {
			log.Fatal(err)
		}
	}()

	var fileScanner = bufio.NewScanner(puzzleFile)
	var fileLines []string
	for fileScanner.Scan() {
		var fileLine = fileScanner.Text()
		if fileLine == "" {
			continue
		}
		fileLines = append(fileLines, fileLine)
	}

	err = fileScanner.Err()
	if err != nil {
		log.Fatal(err)
	}

	solveFirstPart(fileLines)
	solveSecondPart(fileLines)
}
