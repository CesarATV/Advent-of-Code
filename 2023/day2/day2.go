package main

import (
	"bufio"
	"errors"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

const (
	puzzleInputFileName        = "day2.txt"
	puzzleExampleInputFileName = "day2_example.txt"

	maximumNumberOfRedCubes   = 12
	maximumNumberOfGreenCubes = 13
	maximumNumberOfBlueCubes  = 14
)

type cubedColor struct {
	nRedCubes   int
	nGreenCubes int
	nBlueCubes  int
}

func parsePuzzleFile(puzzleFile *os.File) ([]cubedColor, error) {
	var highestNCubesPerGame []cubedColor

	var fileScanner = bufio.NewScanner(puzzleFile)
	for fileScanner.Scan() {
		var lineIdx = len(highestNCubesPerGame)
		highestNCubesPerGame = append(highestNCubesPerGame, cubedColor{})

		var fileLine = fileScanner.Text()
		var gameIdAndColors = strings.Split(fileLine, ": ")
		for _, allRollsInAGame := range strings.Split(gameIdAndColors[1], "; ") {
			for _, currentRoll := range strings.Split(allRollsInAGame, ", ") {
				numberAndColor := strings.Fields(currentRoll)

				var numberOfCubes, err = strconv.Atoi(numberAndColor[0])
				if err != nil {
					return nil, err
				}

				var cubeColor = numberAndColor[1]
				switch cubeColor {
				case "red":
					if highestNCubesPerGame[lineIdx].nRedCubes < numberOfCubes {
						highestNCubesPerGame[lineIdx].nRedCubes = numberOfCubes
					}
				case "green":
					if highestNCubesPerGame[lineIdx].nGreenCubes < numberOfCubes {
						highestNCubesPerGame[lineIdx].nGreenCubes = numberOfCubes
					}
				case "blue":
					if highestNCubesPerGame[lineIdx].nBlueCubes < numberOfCubes {
						highestNCubesPerGame[lineIdx].nBlueCubes = numberOfCubes
					}
				default:
					return nil, errors.New(fmt.Sprintf("Cube color different than red, green or blue found: %s", numberAndColor[1]))
				}
			}

		}
	}

	var err = fileScanner.Err()
	if err != nil {
		return nil, err
	}

	return highestNCubesPerGame, nil
}

func solveFirstPart(highestNCubesPerGame []cubedColor) {

	var sumIdsOfPossibleGames = 0
	for gameIdx, highestNCubesInCurrentGame := range highestNCubesPerGame {
		if highestNCubesInCurrentGame.nRedCubes <= maximumNumberOfRedCubes && highestNCubesInCurrentGame.nGreenCubes <= maximumNumberOfGreenCubes && highestNCubesInCurrentGame.nBlueCubes <= maximumNumberOfBlueCubes {
			var gameId = gameIdx + 1
			sumIdsOfPossibleGames += gameId
		}
	}
	fmt.Println("The sum of the IDs of the games that could have been possible is", sumIdsOfPossibleGames)
}

func solveSecondPart(highestNCubesPerGame []cubedColor) {

	var sumOfCubePowers = 0
	for _, highestNCubesInCurrentGame := range highestNCubesPerGame {
		sumOfCubePowers += highestNCubesInCurrentGame.nRedCubes * highestNCubesInCurrentGame.nGreenCubes * highestNCubesInCurrentGame.nBlueCubes
	}
	fmt.Println("The sum of the power of the cubes is", sumOfCubePowers)
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
		if err := puzzleFile.Close(); err != nil {
			log.Panicln(err)
		}
	}()

	highestNCubesPerGame, err := parsePuzzleFile(puzzleFile)
	if err != nil {
		log.Fatal(err)
	}

	solveFirstPart(highestNCubesPerGame)
	solveSecondPart(highestNCubesPerGame)
}
