/*
The first part can be solved iteratively, calculating each substraction between values. Another solution could be to derive the equation that describes the desired value as a function of the given values. As shown in the given instructions, one can form an upside down pyramid with the given values, and the peak (at the bottom) of the pyramid will always be 0 as guaranteed by the instructions. It is then possible to find the equation. Calling p0 the given rightmost value, p1 the one left to it, p2 the one left to the previous, and so on (making the input in the given example [p5, p4, p3, p2, p1, p0]), the function that describes the value for the given example (6 given numbers) is:
4p0 - 6p1 + 4p2 -p3
If the instructions did not guarantee a 0 at the bottom of the pyramid, other terms would need to be added, making this a very different problem.
However, the given non-examples have more than 6 numbers. While it would be possible to find the equation for more numbers, it was decided to find first the equations for less numbers, as these would be easier to calculate and one could potentially find a pattern valid for all equations. It was found that every equation is the sum of p0 plus the previous equation minus the previous equation with the subindixes of p shifted by 1. So, if the previous were p0, the new one would be p0 (initial component) + p0 (the previous) - p1 (the previous with subindex shifted by 1)). Calling the numbber of given numbers n:
For n=2 the result is:
p0
For n=3:
2p0 - p1 = p0 + (p0) - (p1)
For n=4:
3p0 - 3p1 + p2 = p0 + (2p0 - p1) - (2p1 - p2)
For n=6 (already mentioned)
4p0 - 6p1 + 4p2 - p3 = p0 + (3p0 - 3p1 + p2) - (3p1 - 3p2 + p3)
For n=7
5p0 - 10p1 + 10p2 -5p3 + p4 = p0 + (4p0 - 6p1 + 4p2 - p3) - (4p1 - 6p2 + 4p3 - p4)
... And so on.
The pattern is very similar to Pascal's triangle, so the coefficients of the different p_k values can be calculated as binomial coefficients as \binom{n}{k}, as long as one adjusts for the sign, which is negative for odd values of p_k

The second part is similar to the first, and one could derive a formula to calculate the new value. There is a solution that avoids that calculation and allows to reuse the code from the first part, and that would be to process the numbers of the value-history in the opposite order. From this deduction, without doing calculations and just observing the already written formula for n=6, switching the values and shifting them so one can consider p5 in the equation (which is the value inmediately before the new desired value), the new desired value (for n=6) would be:
4p5 - 6p4 + 4p3 - p2
Again, one can extrapolate this, making the new formulas:
For n=2:
p5
For n=3:
2p5 - p4 = p5 + (p5) - (p4)
For n=4:
3p5 - 3p4 + p3 = p5 + (2p5 - p4) - (2p4 - p3)
For n=6 (already mentioned)
4p5 - 6p4 + 4p3 - p2 = p0 + (3p5 - 3p4 + p3) - (3p4 - 3p3 + p2)
For n=7
5p5 - 10p4 + 10p3 -5p2 + p3 = p0 + (4p5 - 6p4 + 4p3 - p2) - (4p4 - 6p3 + 4p2 - p1)
... And so on
*/

package main

import (
	"bufio"
	"fmt"
	"log"
	"math/big"
	"os"
	"slices"
	"strconv"
	"strings"
)

const (
	puzzleInputFileName        = "day9.txt"
	puzzleExampleInputFileName = "day9_example.txt"
)

func parsePuzzleFile(puzzleFilePath string) ([][]*big.Int, error) {
	var puzzleFile, err = os.Open(puzzleFilePath)
	if err != nil {
		return nil, err
	}
	defer func() {
		if err = puzzleFile.Close(); err != nil {
			log.Println(err)
		}
	}()

	var valuesHistories = [][]*big.Int{}
	var fileScanner = bufio.NewScanner(puzzleFile)
	for fileScanner.Scan() {
		var valueHistoryString = strings.Fields(fileScanner.Text())

		var valueHistory = []*big.Int{}
		for _, valueFromHistory := range valueHistoryString {
			value, err := strconv.Atoi(valueFromHistory)
			if err != nil {
				return nil, err
			}
			valueHistory = append(valueHistory, big.NewInt(int64(value)))
		}
		valuesHistories = append(valuesHistories, valueHistory)
	}

	err = fileScanner.Err()
	if err != nil {
		return nil, err
	}

	return valuesHistories, nil
}

func getSumOfExtrapolatedValues(valuesHistories [][]*big.Int) *big.Int {
	var sumOfExtrapolatedValues = new(big.Int).SetInt64(0)

	for _, valueHistory := range valuesHistories {
		var rowN = len(valueHistory) - 1

		var extrapolatedValue = new(big.Int).SetInt64(0)
		for idx, value := range valueHistory {
			var reverseIdx = rowN - idx
			var corretSignOfTheValueFromTheBinomialCoefficient *big.Int
			if reverseIdx%2 == 0 {
				corretSignOfTheValueFromTheBinomialCoefficient = new(big.Int).SetInt64(1)
			} else {
				corretSignOfTheValueFromTheBinomialCoefficient = new(big.Int).SetInt64(-1)
			}
			var valueOfTheBinomialCoefficient = new(big.Int).Mul(value, new(big.Int).Binomial(int64(rowN), int64(rowN-idx+1)))
			extrapolatedValue = new(big.Int).Add(extrapolatedValue, new(big.Int).Mul(valueOfTheBinomialCoefficient, corretSignOfTheValueFromTheBinomialCoefficient))
		}

		sumOfExtrapolatedValues = new(big.Int).Add(sumOfExtrapolatedValues, extrapolatedValue)
	}

	return sumOfExtrapolatedValues
}

func solveFirstPart(valuesHistories [][]*big.Int) {
	var sumOfExtrapolatedValues = getSumOfExtrapolatedValues(valuesHistories)
	fmt.Println("The sum of the extrapolated values is", sumOfExtrapolatedValues.String())
}

func solveSecondPart(valuesHistories [][]*big.Int) {
	for _, valueHistory := range valuesHistories {
		slices.Reverse[[]*big.Int](valueHistory)
	}

	var sumOfReversedExtrapolatedValues = getSumOfExtrapolatedValues(valuesHistories)
	fmt.Println("Considering the previous values in the history, the sum of the extrapolated values is", sumOfReversedExtrapolatedValues.String())
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

	var valuesHistories, err = parsePuzzleFile(puzzleFilePath)
	if err != nil {
		log.Fatal(err)
	}

	solveFirstPart(valuesHistories)
	solveSecondPart(valuesHistories)
}
