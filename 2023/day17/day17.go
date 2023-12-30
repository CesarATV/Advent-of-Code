/*
The problem was solved using A*. A four-dimensional slice was used to keep track of the different positions (nodes) to visit. Any of the dimensions of the slice does not change in size after its creation, but its size depends of the input. Besides the two dimensions for the position of the crucible, the number of blocks it has traveled without changing direction and the direction in which it is traveling were part of this slice. For the second part of the puzzle is not actually necesary to have an slice as big as the maximum number of blocks one can travel without changing direction, one can use this number minus the minimum number of blocks that has to travel in one direction
The algorithm uses a heap to prioritize the nodes more likely to reach the destination with low heat loss
A heuristic function for A* is defined as the ideal Manhattan distance between the current position and the destination if every block were add the minimum heat loss found between all blocks
A multidimensional slice was chosen instead of a map, probably gaining some (minor) speed, but requiring more memory. A map could have been an equally good solution
*/

package main

import (
	"bufio"
	"container/heap"
	"fmt"
	"log"
	"math"
	"os"
)

const (
	puzzleInputFileName        = "day17.txt"
	puzzleExampleInputFileName = "day17_example.txt"

	maximumNumberOfBlocksTraveledInOneDirectionForFirstPart   = 3
	minimumNumberOfBlocksBeforeChangingDirectionForFirstPart  = 1 // technically 0 is correct, but for code compatibility 1 is set
	minimumNumberOfBlocksBeforeChangingDirectionForSecondPart = 4
	maximumNumberOfBlocksTraveledInOneDirectionForSecondPart  = 10
)

const (
	northMovement = iota
	southMovement
	eastMovement
	westMovement
	nDirectionalMovements
)

type coordinatesStruct struct {
	x, y int
}

type cityBlockStruct struct {
	accumulatedHeatLoss          uint // this represents the total accumulated heat loss when arriving to this block, not the individual heat loss that this block applies
	idealHeatLossInDestination   uint //this will be used as a heuristic
	nLastingConsecutiveMovements int
	direction                    int // each value refers to the previously-declared direction enum
	coordinates                  coordinatesStruct
}

// Slice that will act as heap, using interfaces from the heap package
type cityBlockHeapType []*cityBlockStruct

func (cbh cityBlockHeapType) Len() int { return len(cbh) }

func (cbh cityBlockHeapType) Less(i, j int) bool {
	// lowest idealHeatLossInDestination is prioritized
	return cbh[i].idealHeatLossInDestination < cbh[j].idealHeatLossInDestination
}

func (cbh cityBlockHeapType) Swap(i, j int) {
	cbh[i], cbh[j] = cbh[j], cbh[i]
}

func (cbh *cityBlockHeapType) Push(pushedObject any) {
	*cbh = append(*cbh, pushedObject.(*cityBlockStruct))
}

func (cbh *cityBlockHeapType) Pop() any {
	poppedItem := (*cbh)[len(*cbh)-1]
	(*cbh)[len(*cbh)-1] = nil
	*cbh = (*cbh)[:len(*cbh)-1]
	return poppedItem
}

func parsePuzzleFile(puzzleFilePath string) ([][]uint, uint, error) {
	var puzzleFile, err = os.Open(puzzleFilePath)
	if err != nil {
		return nil, 0, err
	}
	defer func() {
		if err = puzzleFile.Close(); err != nil {
			log.Println(err)
		}
	}()

	var fileScanner = bufio.NewScanner(puzzleFile)
	var heatLossChart = [][]uint{} // keeps track of the individual heat losses of each block
	var minimumHeatLossAmongAllBlocks uint = math.MaxUint64
	for fileScanner.Scan() {
		var heatLossRow = []uint{}
		var heatMapRowString = fileScanner.Text()
		for _, heatLossRune := range heatMapRowString {
			var heatLoss = uint(heatLossRune - '0')
			heatLossRow = append(heatLossRow, heatLoss)

			if heatLoss < minimumHeatLossAmongAllBlocks {
				minimumHeatLossAmongAllBlocks = heatLoss
			}
		}
		heatLossChart = append(heatLossChart, heatLossRow)
	}

	err = fileScanner.Err()
	if err != nil {
		return nil, 0, err
	}

	return heatLossChart, minimumHeatLossAmongAllBlocks, nil
}

func considerNewCityBlockMovement(currentCityBlock *cityBlockStruct, cityBlockChart [][][][nDirectionalMovements]*cityBlockStruct, heatLossChart [][]uint, replacementDirection int, minimumBlockMovementAfterNewDirection int, maximumNumberOfBlocksTraveledInOneDirection int, getIdealHeatLossInDestinationFromCurrentPosition func(coordinatesStruct) uint) (*cityBlockStruct, bool) {

	if currentCityBlock.nLastingConsecutiveMovements == 0 && currentCityBlock.direction == replacementDirection {
		return nil, false // cannot keep moving in that direction
	}

	var nextNLastingConsecutiveMovements int
	var nMovementsBetweenBlocks int
	if replacementDirection == currentCityBlock.direction {
		nMovementsBetweenBlocks = 1
		nextNLastingConsecutiveMovements = currentCityBlock.nLastingConsecutiveMovements - 1
	} else {
		nMovementsBetweenBlocks = minimumBlockMovementAfterNewDirection

		nextNLastingConsecutiveMovements = maximumNumberOfBlocksTraveledInOneDirection - minimumBlockMovementAfterNewDirection
	}

	var followingPosition = currentCityBlock.coordinates
	var heatLossAfterMovement = currentCityBlock.accumulatedHeatLoss
	switch replacementDirection {
	case northMovement:
		if currentCityBlock.coordinates.y <= 1+(nMovementsBetweenBlocks-1) || currentCityBlock.direction == southMovement {
			return nil, false // cannot keep moving north nor turn 180 degrees
		}
		for idx := 0; idx < nMovementsBetweenBlocks; idx++ {
			followingPosition.y--
			heatLossAfterMovement += heatLossChart[followingPosition.y][followingPosition.x]
		}

	case westMovement:
		if currentCityBlock.coordinates.x <= -1+nMovementsBetweenBlocks || currentCityBlock.direction == eastMovement {
			return nil, false // cannot keep moving west nor turn 180 degrees
		}
		for idx := 0; idx < nMovementsBetweenBlocks; idx++ {
			followingPosition.x--
			heatLossAfterMovement += heatLossChart[followingPosition.y][followingPosition.x]
		}

	case eastMovement:
		if currentCityBlock.coordinates.x >= (len(heatLossChart[0])-nMovementsBetweenBlocks) || currentCityBlock.direction == westMovement {
			return nil, false // cannot keep moving east nor turn 180 degrees
		}
		for idx := 0; idx < nMovementsBetweenBlocks; idx++ {
			followingPosition.x++
			heatLossAfterMovement += heatLossChart[followingPosition.y][followingPosition.x]
		}

	case southMovement:
		if currentCityBlock.coordinates.y >= (len(heatLossChart)-nMovementsBetweenBlocks) || currentCityBlock.direction == northMovement {
			return nil, false // cannot keep moving south nor turn 180 degrees
		}
		for idx := 0; idx < nMovementsBetweenBlocks; idx++ {
			followingPosition.y++
			heatLossAfterMovement += heatLossChart[followingPosition.y][followingPosition.x]
		}
	}

	var possibleNextCityBlockToVisit = cityBlockChart[followingPosition.y][followingPosition.x][nextNLastingConsecutiveMovements][replacementDirection]
	if heatLossAfterMovement >= possibleNextCityBlockToVisit.accumulatedHeatLoss {
		return nil, false // the heat loss calculated in this function does not offer any improvements with respect to what already has been considered
	}

	possibleNextCityBlockToVisit.accumulatedHeatLoss = heatLossAfterMovement
	possibleNextCityBlockToVisit.idealHeatLossInDestination = heatLossAfterMovement + getIdealHeatLossInDestinationFromCurrentPosition(followingPosition)
	possibleNextCityBlockToVisit.direction = replacementDirection
	possibleNextCityBlockToVisit.nLastingConsecutiveMovements = nextNLastingConsecutiveMovements
	return possibleNextCityBlockToVisit, true
}

func initializeCityBlocks(heatLossChart [][]uint, initialPosition coordinatesStruct, destinationPosition coordinatesStruct, minimumNumberOfBlocksBeforeChangingDirection int, maximumNumberOfBlocksTraveledInOneDirection int) [][][][nDirectionalMovements]*cityBlockStruct {
	var cityBlockChart = make([][][][nDirectionalMovements]*cityBlockStruct, len(heatLossChart))
	for rowIdx := range heatLossChart {
		var cityBlockRow = make([][][nDirectionalMovements]*cityBlockStruct, len(heatLossChart[rowIdx]))
		for columnIdx := range heatLossChart[rowIdx] {
			var cityBlock = cityBlockStruct{accumulatedHeatLoss: math.MaxUint64, idealHeatLossInDestination: math.MaxUint64, coordinates: coordinatesStruct{x: columnIdx, y: rowIdx}}

			var cityBlockByMaximumDirectionMovement = make([][nDirectionalMovements]*cityBlockStruct, maximumNumberOfBlocksTraveledInOneDirection-minimumNumberOfBlocksBeforeChangingDirection+1)

			for nLastingConsecutiveMovements := 0; nLastingConsecutiveMovements < (maximumNumberOfBlocksTraveledInOneDirection - minimumNumberOfBlocksBeforeChangingDirection + 1); nLastingConsecutiveMovements++ {
				var cityBlockByDirectionMovement = [nDirectionalMovements]*cityBlockStruct{}
				for movementDirection := 0; movementDirection < nDirectionalMovements; movementDirection++ {
					var newCityBlock = cityBlock
					cityBlockByDirectionMovement[movementDirection] = &newCityBlock
					cityBlockByDirectionMovement[movementDirection].nLastingConsecutiveMovements = nLastingConsecutiveMovements
				}
				cityBlockByMaximumDirectionMovement[nLastingConsecutiveMovements] = cityBlockByDirectionMovement
			}
			cityBlockRow[columnIdx] = cityBlockByMaximumDirectionMovement
		}
		cityBlockChart[rowIdx] = cityBlockRow
	}

	var initialCityBlock = cityBlockChart[initialPosition.y][initialPosition.x]
	for nLastingConsecutiveMovements := 0; nLastingConsecutiveMovements < (maximumNumberOfBlocksTraveledInOneDirection - minimumNumberOfBlocksBeforeChangingDirection + 1); nLastingConsecutiveMovements++ {
		for movementDirection := 0; movementDirection < nDirectionalMovements; movementDirection++ {
			initialCityBlock[nLastingConsecutiveMovements][movementDirection].accumulatedHeatLoss = 0 // give it a very low heat loss so the program does not try to process it again (the program would still work, but it would have done extra work unnecesarily). There is no benefit in going back to the initial position
			initialCityBlock[nLastingConsecutiveMovements][movementDirection].idealHeatLossInDestination = 0
			initialCityBlock[nLastingConsecutiveMovements][movementDirection].direction = nDirectionalMovements // give it a direction that does not exist, so the program knows that whatever following direction is chosen, it will not be a continuation of another movement
		}
	}

	return cityBlockChart
}

func calculateMinimumHeatLossUntilDestination(heatLossChart [][]uint, minimumNumberOfBlocksBeforeChangingDirection int, maximumNumberOfBlocksTraveledInOneDirection int, minimumHeatLossAmongAllBlocks uint) {

	var initialPosition = coordinatesStruct{0, 0}
	var destinationPosition = coordinatesStruct{x: len(heatLossChart[0]) - 1, y: len(heatLossChart) - 1}
	var cityBlockChart = initializeCityBlocks(heatLossChart, initialPosition, destinationPosition, minimumNumberOfBlocksBeforeChangingDirection, maximumNumberOfBlocksTraveledInOneDirection)

	var cityBlockHeap = cityBlockHeapType{cityBlockChart[initialPosition.y][initialPosition.x][0][0]}
	heap.Init(&cityBlockHeap)

	var getIdealHeatLossInDestinationFromCurrentPosition = func(currentPosition coordinatesStruct) uint {
		return minimumHeatLossAmongAllBlocks * uint(math.Abs(float64(currentPosition.x-destinationPosition.x))+math.Abs(float64(currentPosition.y-destinationPosition.y)))
	}

	var currentMinimumHeatLoss uint = math.MaxUint64
	for len(cityBlockHeap) > 0 {
		var currentCityBlock = heap.Pop(&cityBlockHeap).(*cityBlockStruct)

		if currentCityBlock.idealHeatLossInDestination >= currentMinimumHeatLoss {
			continue
		} else if currentCityBlock.coordinates == destinationPosition {
			if currentCityBlock.accumulatedHeatLoss < currentMinimumHeatLoss {
				currentMinimumHeatLoss = currentCityBlock.accumulatedHeatLoss
			}
			continue
		}

		for directionalMovement := 0; directionalMovement < nDirectionalMovements; directionalMovement++ {
			if proposedNewCityBlock, isTheProposedMovementBetter := considerNewCityBlockMovement(currentCityBlock, cityBlockChart, heatLossChart, directionalMovement, minimumNumberOfBlocksBeforeChangingDirection, maximumNumberOfBlocksTraveledInOneDirection, getIdealHeatLossInDestinationFromCurrentPosition); isTheProposedMovementBetter == true {
				heap.Push(&cityBlockHeap, proposedNewCityBlock)
			}
		}
	}

	if minimumNumberOfBlocksBeforeChangingDirection <= 1 {
		fmt.Println("With the crucible, the least heat lost that can incur is", currentMinimumHeatLoss)
	} else {
		fmt.Println("With the ultra crucible, the least heat lost that can incur is", currentMinimumHeatLoss)
	}

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

	var heatLossChart, minimumHeatLossAmongAllBlocks, err = parsePuzzleFile(puzzleFilePath)
	if err != nil {
		log.Fatal(err)
	}

	var solveFirstPart = calculateMinimumHeatLossUntilDestination
	solveFirstPart(heatLossChart, minimumNumberOfBlocksBeforeChangingDirectionForFirstPart, maximumNumberOfBlocksTraveledInOneDirectionForFirstPart, minimumHeatLossAmongAllBlocks)
	var solveSecondPart = calculateMinimumHeatLossUntilDestination
	solveSecondPart(heatLossChart, minimumNumberOfBlocksBeforeChangingDirectionForSecondPart, maximumNumberOfBlocksTraveledInOneDirectionForSecondPart, minimumHeatLossAmongAllBlocks)
}
