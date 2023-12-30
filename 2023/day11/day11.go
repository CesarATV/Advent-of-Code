package main

import (
	"bufio"
	"errors"
	"fmt"
	"log"
	"math"
	"os"
)

const (
	puzzleInputFileName        = "day11.txt"
	puzzleExampleInputFileName = "day11_example.txt"

	cosmicExpansionValueFirstPart  = 2
	cosmicExpansionValueSecondPart = 1000000
)

type coordinatesStruct struct {
	x, y int
}

func parsePuzzleFile(puzzleFilePath string) ([]coordinatesStruct, []int, []int, error) {
	var puzzleFile, err = os.Open(puzzleFilePath)
	if err != nil {
		return nil, nil, nil, err
	}
	defer func() {
		if err = puzzleFile.Close(); err != nil {
			log.Println(err)
		}
	}()

	var galaxyPositions = []coordinatesStruct{}

	var fileScanner = bufio.NewScanner(puzzleFile)
	if fileScanner.Scan() == false {
		return nil, nil, nil, errors.New("The puzzle file is empty")
	}
	var fileLine = fileScanner.Text()
	var expandedColumnsMap = map[int]bool{}
	for idx := 0; idx < len(fileLine); idx++ {
		expandedColumnsMap[idx] = true
	}

	var rowIdx = 0
	var doesRowContainAGalaxy = false
	for columnIdx, spaceElement := range fileLine {
		if spaceElement == '#' {
			galaxyPositions = append(galaxyPositions, coordinatesStruct{columnIdx, rowIdx})
			delete(expandedColumnsMap, columnIdx)
			doesRowContainAGalaxy = true
		}
	}

	var expandedRows = []int{}
	if doesRowContainAGalaxy == false {
		expandedRows = append(expandedRows, rowIdx)
	}
	rowIdx++

	for fileScanner.Scan() {
		fileLine = fileScanner.Text()
		if fileLine == "" {
			continue
		}

		doesRowContainAGalaxy = false
		for columnIdx, spaceElement := range fileLine {
			if spaceElement == '#' {
				galaxyPositions = append(galaxyPositions, coordinatesStruct{columnIdx, rowIdx})
				delete(expandedColumnsMap, columnIdx)
				doesRowContainAGalaxy = true
			}
		}

		if doesRowContainAGalaxy == false {
			expandedRows = append(expandedRows, rowIdx)
		}
		rowIdx++
	}

	err = fileScanner.Err()
	if err != nil {
		return nil, nil, nil, err
	}

	var expandedColumns = make([]int, len(expandedColumnsMap))
	var idx = 0
	for expandedColumn := range expandedColumnsMap {
		expandedColumns[idx] = expandedColumn
		idx++
	}

	return galaxyPositions, expandedRows, expandedColumns, nil
}

func getManhattanDistance(firstCoordinate coordinatesStruct, secondCoordinate coordinatesStruct) int {
	var manhattanDistance = math.Abs(float64(firstCoordinate.x)-float64(secondCoordinate.x)) + math.Abs(float64(firstCoordinate.y)-float64(secondCoordinate.y))
	return int(manhattanDistance)
}

func getExtraTraveledLengthDueToCosmicExpansion(firstGalaxyCoordinate int, secondGalaxyCoordinate int, expansionCoordinates []int, extraGalaxyExpansionValue int) int {
	var smallerCoordinate int
	var biggerCoordinate int

	if firstGalaxyCoordinate < secondGalaxyCoordinate {
		smallerCoordinate = firstGalaxyCoordinate
		biggerCoordinate = secondGalaxyCoordinate
	} else {
		smallerCoordinate = secondGalaxyCoordinate
		biggerCoordinate = firstGalaxyCoordinate
	}

	var extraTraveledLength = 0
	for _, expansionCoordinate := range expansionCoordinates {
		if expansionCoordinate > smallerCoordinate && expansionCoordinate < biggerCoordinate {
			// the expanded coordinates are between the concerned galaxies
			extraTraveledLength += extraGalaxyExpansionValue
		}
	}
	return extraTraveledLength
}

func calculateSumOfShortestPathLengthBetweenGalaxies(galaxyPositions []coordinatesStruct, expandedRows []int, expandedColumns []int, totalCosmicExpansion int) {
	var extraGalaxyExpansionValue = totalCosmicExpansion - 1 // the Manhattan distance considers travelling the cosmic expansion as a normal unexpanded length, so once this distance is calculated only the extra expanded length has to be considered
	var sumOfShortestPathLengths = 0
	for firstGalaxyToCompareIdx := range galaxyPositions {
		var firstGalaxyPositionToCompare = galaxyPositions[firstGalaxyToCompareIdx]
		for _, secondGalaxyPositionToCompare := range galaxyPositions[firstGalaxyToCompareIdx+1:] {
			sumOfShortestPathLengths += getManhattanDistance(firstGalaxyPositionToCompare, secondGalaxyPositionToCompare)
			sumOfShortestPathLengths += getExtraTraveledLengthDueToCosmicExpansion(firstGalaxyPositionToCompare.x, secondGalaxyPositionToCompare.x, expandedColumns, extraGalaxyExpansionValue)
			sumOfShortestPathLengths += getExtraTraveledLengthDueToCosmicExpansion(firstGalaxyPositionToCompare.y, secondGalaxyPositionToCompare.y, expandedRows, extraGalaxyExpansionValue)
		}
	}

	fmt.Println("Considering a cosmic expansion value of", totalCosmicExpansion, "the sum of the shortest path lengths between the galaxies is", sumOfShortestPathLengths)
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

	var galaxyPositions, expandedRows, expandedColumns, err = parsePuzzleFile(puzzleFilePath)
	if err != nil {
		log.Fatal(err)
	}

	var solveFirstPart = calculateSumOfShortestPathLengthBetweenGalaxies
	solveFirstPart(galaxyPositions, expandedRows, expandedColumns, cosmicExpansionValueFirstPart)

	var solveSecondPart = calculateSumOfShortestPathLengthBetweenGalaxies
	solveSecondPart(galaxyPositions, expandedRows, expandedColumns, cosmicExpansionValueSecondPart)
}
