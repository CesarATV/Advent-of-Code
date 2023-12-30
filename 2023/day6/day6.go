/*
Both parts of the puzzle are extremmely similar. Both can be solved by simulating checking how much the boat will travel for each possible millisecond in which the boat button has been pressed. This procedure is reflected in the function getNumberOfWaysToBeatRecordByBruteForce. Despite its really small execution time, it was decided to implement another procedure, creating getNumberOfWaysToBeatRecordAnalytically (able to save around 20 ms in execution time with respect to the brute force solution). This function does not obtain the procedure by brute force, but by finding an an analytic solution:
Naming t the total duration of the race, r the remaining time after holding the button v the velocity of the boat and d the record distance to beat, the condition that allows to beat the other boats is
(t-r)*v > d
where the velocity matches in value the time after holding the button, so it can be rewritten as
(t-r)*r > d <--> tr-r^2 > d <--> -r^2 - tr - d > 0
This is a quadratic equation, and the solutions for r can be expressed as
r = (t +-(t^2 - 4d)^0.5)/2
Naming r1 the bigger root of r and r2 the smaller, the equation could also be expressed as
(-r-r1)*(-r-r2) > 0 <--> -(r-r1)*(r-r2) > 0
For this equality to hold true, r has to be in the interval
r1 <= r <= r2
Therefore, the number of ways to beat the race is the difference between r2 and r1, as long as both are real positive numbers or zero. If only r2 is real positive or zero, the desired number will be just r2
*/

package main

import (
	"bufio"
	"errors"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

const (
	puzzleInputFileName        = "day6.txt"
	puzzleExampleInputFileName = "day6_example.txt"
)

func parsePuzzleFile(puzzleFilePath string) ([]int, []int, int, int, error) {
	var puzzleFile, err = os.Open(puzzleFilePath)
	if err != nil {
		return nil, nil, 0, 0, err
	}
	defer func() {
		if err = puzzleFile.Close(); err != nil {
			log.Println(err)
		}
	}()

	var fileScanner = bufio.NewScanner(puzzleFile)
	if fileScanner.Scan() == false {
		return nil, nil, 0, 0, errors.New("The puzzle file is empty")
	}

	var raceDurationLine = strings.Split(fileScanner.Text(), ": ")[1]
	var raceDurations []int
	for _, raceDurationAsString := range strings.Fields(raceDurationLine) {
		var raceDuration, err = strconv.Atoi(raceDurationAsString)
		if err != nil {
			return nil, nil, 0, 0, err
		}
		raceDurations = append(raceDurations, raceDuration)
	}

	var raceDurationWithGoodKerningString = strings.Replace(raceDurationLine, " ", "", -1)
	raceDurationWithGoodKerning, err := strconv.Atoi(raceDurationWithGoodKerningString)
	if err != nil {
		return nil, nil, 0, 0, err
	}

	if fileScanner.Scan() == false {
		// file is emtpy
		return nil, nil, 0, 0, errors.New("The puzzle file only has one line")
	}

	err = fileScanner.Err()
	if err != nil {
		return nil, nil, 0, 0, err
	}

	var recordDistancesLine = strings.Split(fileScanner.Text(), ": ")[1]
	var recordDistances []int
	for _, recordDistanceAsString := range strings.Fields(recordDistancesLine) {
		// Convert string to integer
		recordDistance, err := strconv.Atoi(recordDistanceAsString)
		if err != nil {
			return nil, nil, 0, 0, err
		}
		recordDistances = append(recordDistances, recordDistance)
	}

	var recordDistancesWithGoodKerningString = strings.Replace(recordDistancesLine, " ", "", -1)
	recordDistancesWithGoodKerning, err := strconv.Atoi(recordDistancesWithGoodKerningString)
	if err != nil {
		return nil, nil, 0, 0, err
	}

	return raceDurations, recordDistances, raceDurationWithGoodKerning, recordDistancesWithGoodKerning, nil

}

func getNumberOfWaysToBeatRecordByBruteForce(raceDuration int, recordDistance int) uint {
	// raceDuration is in the same units as nMillisecondsHoldingButton, milliseconds
	var nMillisecondsHoldingButton = 1
	for ; nMillisecondsHoldingButton < (raceDuration - 1); nMillisecondsHoldingButton++ {
		var velocity = nMillisecondsHoldingButton
		var remainingTimeAfterHoldingButton = raceDuration - nMillisecondsHoldingButton
		var traveledDistance = velocity * remainingTimeAfterHoldingButton
		if traveledDistance > recordDistance {
			break // progress to the following loop
		}
	}

	var numberOfWaysToBeatRecord uint = 0
	for ; nMillisecondsHoldingButton < (raceDuration - 1); nMillisecondsHoldingButton++ {
		var velocity = nMillisecondsHoldingButton
		var remainingTimeAfterHoldingButton = raceDuration - nMillisecondsHoldingButton
		var traveledDistance = velocity * remainingTimeAfterHoldingButton
		if traveledDistance > recordDistance {
			numberOfWaysToBeatRecord++
		} else {
			break // Once the condition traveledDistance > recordDistance has been proven true (in the top loop of this function) and then false (in this loop), it will not be true again.
		}
	}

	return numberOfWaysToBeatRecord
}

// The explanations that show why this function work are at the beginning of the program
func getNumberOfWaysToBeatRecordAnalytically(raceDuration int, recordDistance int) uint {
	var squaredRootTermOfTheEquation = math.Pow(float64(raceDuration*raceDuration-4*recordDistance), 0.5)
	var lowerBoundOfRemainingTimeAfterHoldingButton = (float64(raceDuration) - squaredRootTermOfTheEquation) / 2
	var upperBoundOfRemainingTimeAfterHoldingButton = (float64(raceDuration) + squaredRootTermOfTheEquation) / 2

	var numberOfWaysToBeatTheRecord uint
	if lowerBoundOfRemainingTimeAfterHoldingButton > 0 {
		numberOfWaysToBeatTheRecord = uint(upperBoundOfRemainingTimeAfterHoldingButton) - uint(math.Ceil(lowerBoundOfRemainingTimeAfterHoldingButton)) + 1
	} else {
		numberOfWaysToBeatTheRecord = uint(upperBoundOfRemainingTimeAfterHoldingButton)
	}
	return numberOfWaysToBeatTheRecord
}

func solveFirstPart(raceDurations []int, recordDistances []int, getNumberOfWaysToBeatRecord func(int, int) uint) {
	var multiplicationBetweenNumberOfWaysToBeatRecord uint = 1
	for naceNumber := range raceDurations {
		var numberOfWaysToBeatRecord uint = getNumberOfWaysToBeatRecord(raceDurations[naceNumber], recordDistances[naceNumber])
		multiplicationBetweenNumberOfWaysToBeatRecord *= numberOfWaysToBeatRecord
	}

	fmt.Println("Multiplicating the number of ways to beat the record in every race gives a value of", multiplicationBetweenNumberOfWaysToBeatRecord)
}

func solveSecondPart(raceDuration int, recordDistance int, getNumberOfWaysToBeatRecord func(int, int) uint) {
	var numberOfWaysToBeatTheRecord = getNumberOfWaysToBeatRecord(raceDuration, recordDistance)

	fmt.Println("After correcting for bad kerning, the number of ways to beat the record is", numberOfWaysToBeatTheRecord)
}

func main() {
	var getNumberOfWaysToBeatRecord = getNumberOfWaysToBeatRecordAnalytically
	var puzzleFilePath string
	switch len(os.Args) {
	case 1:
		puzzleFilePath = puzzleInputFileName
	case 2:
		puzzleFilePath = puzzleExampleInputFileName
	case 4:
		getNumberOfWaysToBeatRecord = getNumberOfWaysToBeatRecordByBruteForce
		fmt.Println("It has been selected to solve the problem by brute force instead of analytically")
		fallthrough
	default:
		puzzleFilePath = os.Args[2]
	}

	raceDurations, recordDistances, raceDurationWithGoodKerning, recordDistancesWithGoodKerning, err := parsePuzzleFile(puzzleFilePath)
	if err != nil {
		log.Fatal(err)
	}

	solveFirstPart(raceDurations, recordDistances, getNumberOfWaysToBeatRecord)
	solveSecondPart(raceDurationWithGoodKerning, recordDistancesWithGoodKerning, getNumberOfWaysToBeatRecord)
}
