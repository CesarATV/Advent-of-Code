/*
As there are pipe tiles that are not connected to the main loop, so the solution to the first part cannot be found by simply counting the pipe tiles. To solve the first part it is necessary to travel through the pipeline counting all traveled tiles

The second part gets needs to know the tiles that belong to the loop, which is done easily from the first part. Once the loop is known, it is possible to find the non-loop tiles inside it by analizing the grid, either horizontally or vertically. The implemented solution decided (arbitrarily) to analize it horizontally.
Horizontally, from left to right, one will get inside the loop when finding the tile '|', 'L' or 'F'. For the case '|', one can assume that every tile will be inside the loop until finding another '|'.  Once a 'L' or 'F' is found, necessarily there has to be either a '|' closing the loop or their respective counterparts 'J' (for 'L') and '7' (for 'F'). Note how a connection between 'F' and 'J' such as 'FJ.' would not remove the condition that the tile to the right of 'J' is inside the loop (because the loop propagated from J has to enclose that tile at some point), while 'F7.' would.
The second part was implemented following this principle, using a boolean flag representing if the tiles are inside the loop. The flag would be toggled once finding '|' and any of either 'L' and 'J' or '7' and 'F'. The pairs 'L', 'J' and '7', 'F' shall not be considered together, just a pair is enough. Another way of understanding the problem would be to flip the flag only when a mixed pair is found as long as there are no other pairs in between this mixed pair

The explained solution for the second part has an identical explanation when solving the problem vertically, using '-' and either the pair 'F' and 'L' or the pair '7' and 'J',
*/

package main

import (
	"bufio"
	"errors"
	"fmt"
	"log"
	"os"
	"strings"
)

const (
	puzzleInputFileName        = "day10.txt"
	puzzleExampleInputFileName = "day10_example.txt"
)

const (
	northMovement = iota
	southMovement
	eastMovement
	westMovement
)

type coordinatesStruct struct {
	x, y int
}

func parsePuzzleFile(puzzleFilePath string) ([][]rune, rune, coordinatesStruct, error) {
	var puzzleFile, err = os.Open(puzzleFilePath)
	if err != nil {
		return nil, 0, coordinatesStruct{}, err
	}
	defer func() {
		if err = puzzleFile.Close(); err != nil {
			log.Println(err)
		}
	}()

	var tilesGrid = [][]rune{}
	var initialPositionOfTheAnimal = coordinatesStruct{-1, -1}
	var count = 0
	var fileScanner = bufio.NewScanner(puzzleFile)
	for fileScanner.Scan() {
		var fileLine = fileScanner.Text()
		if fileLine == "" {
			continue
		}

		if initialPositionOfTheAnimal.x == -1 {
			initialPositionOfTheAnimal.x = strings.Index(fileLine, "S")
			initialPositionOfTheAnimal.y++
		}

		var fileLineAsSliceOfRunes = make([]rune, len(fileLine))
		for idx, lineRune := range fileLine {
			fileLineAsSliceOfRunes[idx] = lineRune
			if lineRune != '.' {
				count++
			}
		}

		tilesGrid = append(tilesGrid, fileLineAsSliceOfRunes)
	}

	err = fileScanner.Err()
	if err != nil {
		return nil, 0, coordinatesStruct{}, err
	}

	if initialPositionOfTheAnimal.x == -1 {
		return nil, 0, coordinatesStruct{}, errors.New("No initial position for the animal found. Tile 'S' is missing")
	}

	var canItGoEast = false
	var canItGoWest = false
	var canItGoNorth = false
	var canItGoSouth = false
	if newXPosition := initialPositionOfTheAnimal.x + 1; newXPosition < len(tilesGrid[0]) {
		switch tilesGrid[initialPositionOfTheAnimal.y][newXPosition] {
		case '-', 'J', '7':
			canItGoEast = true
		}
	}
	if newXPosition := initialPositionOfTheAnimal.x - 1; newXPosition >= 0 {
		switch tilesGrid[initialPositionOfTheAnimal.y][newXPosition] {
		case '-', 'L', 'F':
			canItGoWest = true
		}
	}
	if newYPosition := initialPositionOfTheAnimal.y + 1; newYPosition < len(tilesGrid) {
		switch tilesGrid[newYPosition][initialPositionOfTheAnimal.x] {
		case '|', 'L', 'J':
			canItGoSouth = true
		}
	}
	if newYPosition := initialPositionOfTheAnimal.y - 1; newYPosition >= 0 {
		switch tilesGrid[newYPosition][initialPositionOfTheAnimal.x] {
		case '|', '7', 'F':
			canItGoNorth = true
		}
	}

	var pipeOfTheAnimal rune
	if canItGoEast && canItGoWest {
		pipeOfTheAnimal = '-'
	} else if canItGoEast && canItGoNorth {
		pipeOfTheAnimal = 'J'
	} else if canItGoEast && canItGoSouth {
		pipeOfTheAnimal = 'F'
	} else if canItGoWest && canItGoNorth {
		pipeOfTheAnimal = 'L'
	} else if canItGoWest && canItGoSouth {
		pipeOfTheAnimal = '7'
	} else if canItGoNorth && canItGoSouth {
		pipeOfTheAnimal = '|'
	} else {
		return nil, 0, coordinatesStruct{}, errors.New("Cannot figure out the pipe in the tile of the animal. This tile is likely pointing to the borders of the grid")
	}

	return tilesGrid, pipeOfTheAnimal, initialPositionOfTheAnimal, nil

}

func solveFirstPart(tilesGrid [][]rune, pipeOfTheAnimal rune, initialPositionOfTheAnimal coordinatesStruct) map[coordinatesStruct]bool {
	var initialStepPosition = initialPositionOfTheAnimal
	var previousMovementDirection int
	switch pipeOfTheAnimal {
	case '|', 'L', 'J':
		previousMovementDirection = northMovement
		initialStepPosition.y--
	case '-', 'F':
		previousMovementDirection = eastMovement
		initialStepPosition.x++
	case '7':
		previousMovementDirection = southMovement
		initialStepPosition.y++
	}

	var tilesThatBelongToTheLoop = map[coordinatesStruct]bool{}
	var currentTile = initialStepPosition
	var nSteps uint = 0
	for wasTileOfTheAnimalFound := false; wasTileOfTheAnimalFound == false; nSteps++ {

		tilesThatBelongToTheLoop[currentTile] = true
		switch tilesGrid[currentTile.y][currentTile.x] {
		case '|':
			if previousMovementDirection == northMovement {
				currentTile.y--
			} else {
				currentTile.y++
			}

		case '-':
			if previousMovementDirection == eastMovement {
				currentTile.x++
			} else {
				currentTile.x--
			}

		case 'L':
			if previousMovementDirection == southMovement {
				currentTile.x++
				previousMovementDirection = eastMovement
			} else {
				currentTile.y--
				previousMovementDirection = northMovement
			}

		case 'J':
			if previousMovementDirection == southMovement {
				currentTile.x--
				previousMovementDirection = westMovement
			} else {
				currentTile.y--
				previousMovementDirection = northMovement
			}

		case '7':
			if previousMovementDirection == northMovement {
				currentTile.x--
				previousMovementDirection = westMovement
			} else {
				currentTile.y++
				previousMovementDirection = southMovement
			}

		case 'F':
			if previousMovementDirection == northMovement {
				currentTile.x++
				previousMovementDirection = eastMovement
			} else {
				currentTile.y++
				previousMovementDirection = southMovement
			}

		case 'S':
			wasTileOfTheAnimalFound = true

		default:
			panic(fmt.Sprintf("Impossible tile was found, it has the character %c", tilesGrid[currentTile.y][currentTile.x]))
		}
	}

	var nStepsToFarthestPosition = nSteps / 2
	fmt.Println("In the loop, there are", nStepsToFarthestPosition, "steps from a starting position to its farthest")

	return tilesThatBelongToTheLoop
}

func solveSecondPart(tilesGrid [][]rune, pipeOfTheAnimal rune, initialPositionOfTheAnimal coordinatesStruct, tilesThatBelongToTheLoop map[coordinatesStruct]bool) {

	for rowIdx := range tilesGrid {
		for colIdx := range tilesGrid[rowIdx] {
			var coordinateToAnalize = coordinatesStruct{colIdx, rowIdx}
			_, isTilePartOfTheLoop := tilesThatBelongToTheLoop[coordinateToAnalize]
			if isTilePartOfTheLoop == false {
				tilesGrid[coordinateToAnalize.y][coordinateToAnalize.x] = '.' // consider pipe parts that non belong to the loop as ground
			}
		}
	}

	tilesGrid[initialPositionOfTheAnimal.y][initialPositionOfTheAnimal.x] = pipeOfTheAnimal
	var nEnclosedTiles = 0
	for _, tileRow := range tilesGrid {
		var insideTheLoop = false
		for _, currentTile := range tileRow {
			switch currentTile {
			case '.':
				if insideTheLoop == true {
					nEnclosedTiles++
				}

			case '|', 'L', 'J': // an alternative to this case would be to check for either '|', '7' and 'F'
				insideTheLoop = !insideTheLoop
			}
		}
	}

	fmt.Println("There are", nEnclosedTiles, "tiles enclosed by the loop")
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

	var tilesGrid, pipeOfTheAnimal, initialPositionOfTheAnimal, err = parsePuzzleFile(puzzleFilePath)
	if err != nil {
		log.Fatal(err)
	}

	var tilesThatBelongToTheLoop = solveFirstPart(tilesGrid, pipeOfTheAnimal, initialPositionOfTheAnimal)
	solveSecondPart(tilesGrid, pipeOfTheAnimal, initialPositionOfTheAnimal, tilesThatBelongToTheLoop)
}
