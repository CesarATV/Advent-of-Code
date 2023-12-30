/*
The problem describes a polygon and asks to calculate the number of points that compose it.
Both parts can be solved in the same way, using Pick's theorem. The theorem shows how the number 'i' of discrete points inside a discrete polygon (defined by discrete vertices) are related to the number of 'b' (also discrete) boundary points and its 'A' area, such that:
i = A - b/2
While the boundary points are the given input to the problem, the area still needs to be calculated. It can be done with the shoelace formula, having as input the vertices of the polygon. Conveniently, the problem gives as input the vertices of the polygon in ordered manner, so they can be plugged into the shoelace formula maintaining they order.

While the problem does not state it explicetely, the given instructions are the vertices of the described polygon and do not contain a single point inside of it, so there is no need filter out the non-vertex points from the instructions
*/

package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

const (
	puzzleInputFileName        = "day18.txt"
	puzzleExampleInputFileName = "day18_example.txt"
)

type coordinatesStruct struct {
	x, y int
}

func parsePuzzleFile(puzzleFilePath string) ([]coordinatesStruct, []coordinatesStruct, error) {
	var puzzleFile, err = os.Open(puzzleFilePath)
	if err != nil {
		return nil, nil, err
	}
	defer func() {
		if err = puzzleFile.Close(); err != nil {
			log.Println(err)
		}
	}()

	var diggingPositions = []coordinatesStruct{}
	var colorCodedDiggingPositions = []coordinatesStruct{}

	var fileScanner = bufio.NewScanner(puzzleFile)
	var diggingPosition = coordinatesStruct{0, 0}
	var colorCodedDiggingPosition = coordinatesStruct{0, 0}
	for fileScanner.Scan() {
		var fileLine = fileScanner.Text()
		if fileLine == "" {
			continue
		}

		var digPlan = strings.Fields(fileLine)
		movement, err := strconv.Atoi(digPlan[1])
		if err != nil {
			return nil, nil, err
		}

		var direction = digPlan[0]
		switch direction {
		case "U":
			diggingPosition.y -= movement
		case "D":
			diggingPosition.y += movement
		case "L":
			diggingPosition.x -= movement
		case "R":
			diggingPosition.x += movement
		default:
			return nil, nil, fmt.Errorf("Found direction different than U, D, L or R: %s", direction)
		}
		diggingPositions = append(diggingPositions, diggingPosition)

		var colorCode = digPlan[2][2 : len(digPlan[2])-1]
		var colorCodedDirection = colorCode[len(colorCode)-1]
		var colorCodedPositionHex = colorCode[:len(colorCode)-1]
		colorCodedMovement, err := strconv.ParseInt(colorCodedPositionHex, 16, 0)
		if err != nil {
			return nil, nil, err
		}

		switch colorCodedDirection {
		case '3':
			colorCodedDiggingPosition.y -= int(colorCodedMovement)
		case '1':
			colorCodedDiggingPosition.y += int(colorCodedMovement)
		case '2':
			colorCodedDiggingPosition.x -= int(colorCodedMovement)
		case '0':
			colorCodedDiggingPosition.x += int(colorCodedMovement)
		default:
			return nil, nil, fmt.Errorf("Color-coded direction different than 0, 1, 2 or 3: %c", colorCodedDirection)
		}
		colorCodedDiggingPositions = append(colorCodedDiggingPositions, colorCodedDiggingPosition)
	}

	err = fileScanner.Err()
	if err != nil {
		return nil, nil, err
	}

	return diggingPositions, colorCodedDiggingPositions, nil
}

func getAreaOfASimplePolygonWithTheShoelaceFormula(listOfVertices []coordinatesStruct) int {
	var polygonArea = 0
	for idx := 0; idx < (len(listOfVertices) - 1); idx++ {
		polygonArea += listOfVertices[idx].x*listOfVertices[idx+1].y - listOfVertices[idx].y*listOfVertices[idx+1].x
	}
	polygonArea += listOfVertices[len(listOfVertices)-1].x*listOfVertices[0].y - listOfVertices[len(listOfVertices)-1].y*listOfVertices[0].x

	polygonArea = int(math.Abs(float64(polygonArea)) / 2)
	return polygonArea
}

func getNumberOfBoundaryPoints(listOfVertices []coordinatesStruct) int {
	var nBoundaryPoints = 0
	for idx := 0; idx < (len(listOfVertices) - 1); idx++ {
		nBoundaryPoints += int(math.Abs(float64(listOfVertices[idx].x - listOfVertices[idx+1].x)))
		nBoundaryPoints += int(math.Abs(float64(listOfVertices[idx].y - listOfVertices[idx+1].y)))
	}
	nBoundaryPoints += int(math.Abs(float64(listOfVertices[len(listOfVertices)-1].x - listOfVertices[0].x)))
	nBoundaryPoints += int(math.Abs(float64(listOfVertices[len(listOfVertices)-1].y - listOfVertices[0].y)))
	return nBoundaryPoints
}

func getNumberOfPointsEncompassedByAPolygonByItsVertices(listOfVertices []coordinatesStruct) int {
	var polygonArea = getAreaOfASimplePolygonWithTheShoelaceFormula(listOfVertices)
	var nBoundaryPoints = getNumberOfBoundaryPoints(listOfVertices)
	var nInsidePoints = polygonArea - nBoundaryPoints/2 + 1 // Pick's theorem

	var nPointsInPolygon = nBoundaryPoints + nInsidePoints
	return nPointsInPolygon
}

func printLagoonPotentialCubicMetersOfLava(diggingPositions []coordinatesStruct, instructionsName string) {
	var nPointsInPolygon = getNumberOfPointsEncompassedByAPolygonByItsVertices(diggingPositions)
	fmt.Printf("Following %s, the lagoon can hold %d cubic meters of lava\n", instructionsName, nPointsInPolygon)
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

	var diggingPositions, colorCodedDiggingPositions, err = parsePuzzleFile(puzzleFilePath)
	if err != nil {
		log.Fatal(err)
	}

	var solveFirstPart = printLagoonPotentialCubicMetersOfLava
	var solveSecondPart = printLagoonPotentialCubicMetersOfLava

	solveFirstPart(diggingPositions, "the instructions")
	solveSecondPart(colorCodedDiggingPositions, "the color-coded instructions")
}
