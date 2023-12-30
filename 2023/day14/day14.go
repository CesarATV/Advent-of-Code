/*
The first part was done without simulating the movement of the rounded rocks, and just by assuming that they would cover the topmost parts of the subrow where they are. These subrows are parts of the row when this is subdivided by cube-shaped rocks

The second part required simulating the movement of the rounded rocks. As the number of spin cycles is very high (1000000000), it was assumed that there would be a repeating cycle after some iterations. Brent's algorithm was used to detect the length of this cycle and its start position. With these two numbers, it was possible to calculate in which cycle position the load will be for the required number of spin cycles
*/

package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

const (
	puzzleInputFileName        = "day14.txt"
	puzzleExampleInputFileName = "day14_example.txt"

	nSpinCycles = 1000000000
)

const (
	northTilt = iota
	westTilt
	southTilt
	eastTilt
)

func parsePuzzleFile(puzzleFilePath string) ([][]rune, int, error) {
	var puzzleFile, err = os.Open(puzzleFilePath)
	if err != nil {
		return nil, 0, err
	}
	defer func() {
		if err = puzzleFile.Close(); err != nil {
			log.Println(err)
		}
	}()

	var platformMap = [][]rune{}

	var fileScanner = bufio.NewScanner(puzzleFile)
	var rowIdx = 0
	var nRoundedRocks = 0
	for fileScanner.Scan() {
		var fileLine = fileScanner.Text()
		if fileLine == "" {
			continue
		}

		platformMap = append(platformMap, make([]rune, len(fileLine)))
		for columnIdx, platformElement := range fileLine {
			platformMap[rowIdx][columnIdx] = platformElement
			if platformElement == 'O' {
				nRoundedRocks++
			}
		}
		rowIdx++
	}

	err = fileScanner.Err()
	if err != nil {
		return nil, 0, err
	}

	return platformMap, nRoundedRocks, nil
}

/*
The function calculates directly the total load of north support beam witout simulating the movement of the rocks.
This function could use the functions that were created for the second part of the puzzle, simply using the functions tiltPlatform(platformMap) and northSupportBeamsLoad := getNorthSupportBeamLoad(platformMap, northTilt). This solution is probably slower than the implemented, and also would modify platformMap, which would leave it in a state where it could not be so easily used by the second part of the puzzle
*/
func solveFirstPart(platformMap [][]rune) {
	var northSupportBeamsLoad = 0
	for columnIdx := range platformMap[0] {
		var topmostRowIdxBeforeFindingCubeShapedRock = len(platformMap)
		var nRoundedRocksFoundBeforeCubeShapeRocks = 0
		for rowIdx := range platformMap {
			switch platformMap[rowIdx][columnIdx] {
			case 'O':
				nRoundedRocksFoundBeforeCubeShapeRocks++
			case '#':
				northSupportBeamsLoad += (nRoundedRocksFoundBeforeCubeShapeRocks * (2*topmostRowIdxBeforeFindingCubeShapedRock - nRoundedRocksFoundBeforeCubeShapeRocks + 1)) / 2 // arithmetic series representing the summation between n=0 and n=nRoundedRocksFoundBeforeCubeShapeRocks of (topmostRowIdxBeforeFindingCubeShapedRock-n)

				topmostRowIdxBeforeFindingCubeShapedRock = len(platformMap) - rowIdx - 1
				nRoundedRocksFoundBeforeCubeShapeRocks = 0
			}
		}

		northSupportBeamsLoad += (nRoundedRocksFoundBeforeCubeShapeRocks * (2*topmostRowIdxBeforeFindingCubeShapedRock - nRoundedRocksFoundBeforeCubeShapeRocks + 1)) / 2 // arithmetic series representing the summation between n=0 and n=nRoundedRocksFoundBeforeCubeShapeRocks of (topmostRowIdxBeforeFindingCubeShapedRock-n)
	}
	fmt.Println("After rolling the round rocks north, the load on the north support beams is", northSupportBeamsLoad)
}

/*
This function takes care of calculating the position of the rounded rocks after tilting the platform in any direction. The code for each one of the cases is really similar, but it was not possible to find an easier way to synthetize the four cases (one for each direction) into a shorter code, although non excessive effort was made to do it
*/
func tiltPlatform(platformMap [][]rune, tiltDirection int) {
	if tiltDirection == northTilt || tiltDirection == southTilt {
		for columnIdx := range platformMap[0] {
			var idxBeforeFindingCubeShapedRock = 0
			var nRoundedRocksFoundBeforeCubeShapeRocks = 0
			for rowIdx := range platformMap {
				switch platformMap[rowIdx][columnIdx] {
				case 'O':
					nRoundedRocksFoundBeforeCubeShapeRocks++
				case '#':
					// rewrite the visited section, pilling the rocks first and leaving the other spaces empty
					if nRoundedRocksFoundBeforeCubeShapeRocks != 0 {
						if tiltDirection == northTilt {
							// travel bottom from top until bottom
							for newRockPosition := idxBeforeFindingCubeShapedRock; newRockPosition < (idxBeforeFindingCubeShapedRock + nRoundedRocksFoundBeforeCubeShapeRocks); newRockPosition++ {
								platformMap[newRockPosition][columnIdx] = 'O'
							}
							for newEmptySpacePosition := idxBeforeFindingCubeShapedRock + nRoundedRocksFoundBeforeCubeShapeRocks; newEmptySpacePosition < rowIdx; newEmptySpacePosition++ {
								platformMap[newEmptySpacePosition][columnIdx] = '.'
							}
						} else { // southTilt
							for newEmptySpacePosition := idxBeforeFindingCubeShapedRock; newEmptySpacePosition < (rowIdx - nRoundedRocksFoundBeforeCubeShapeRocks); newEmptySpacePosition++ {
								platformMap[newEmptySpacePosition][columnIdx] = '.'
							}
							for newRockPositionIdx := rowIdx - nRoundedRocksFoundBeforeCubeShapeRocks; newRockPositionIdx < rowIdx; newRockPositionIdx++ {
								platformMap[newRockPositionIdx][columnIdx] = 'O'
							}
						}
					}

					idxBeforeFindingCubeShapedRock = rowIdx + 1
					nRoundedRocksFoundBeforeCubeShapeRocks = 0
				}
			}

			if nRoundedRocksFoundBeforeCubeShapeRocks != 0 {
				if tiltDirection == northTilt {
					// travel bottom from top until bottom
					for newRockPosition := idxBeforeFindingCubeShapedRock; newRockPosition < (idxBeforeFindingCubeShapedRock + nRoundedRocksFoundBeforeCubeShapeRocks); newRockPosition++ {
						platformMap[newRockPosition][columnIdx] = 'O'
					}
					for newEmptySpacePosition := idxBeforeFindingCubeShapedRock + nRoundedRocksFoundBeforeCubeShapeRocks; newEmptySpacePosition < len(platformMap); newEmptySpacePosition++ {
						platformMap[newEmptySpacePosition][columnIdx] = '.'
					}
				} else { // southTilt
					for newEmptySpacePosition := idxBeforeFindingCubeShapedRock; newEmptySpacePosition < (len(platformMap) - nRoundedRocksFoundBeforeCubeShapeRocks); newEmptySpacePosition++ {
						platformMap[newEmptySpacePosition][columnIdx] = '.'
					}
					for newRockPositionIdx := len(platformMap) - nRoundedRocksFoundBeforeCubeShapeRocks; newRockPositionIdx < len(platformMap); newRockPositionIdx++ {
						platformMap[newRockPositionIdx][columnIdx] = 'O'
					}
				}
			}
		}
	} else { // west or east tilt
		for rowIdx := range platformMap {
			var idxBeforeFindingCubeShapedRock = 0
			var nRoundedRocksFoundBeforeCubeShapeRocks = 0
			for columnIdx := range platformMap[0] {
				switch platformMap[rowIdx][columnIdx] {
				case 'O':
					nRoundedRocksFoundBeforeCubeShapeRocks++
				case '#':
					// rewrite the visited section, pilling the rocks first and leaving the other spaces empty
					if nRoundedRocksFoundBeforeCubeShapeRocks != 0 {
						if tiltDirection == westTilt {
							// travel bottom from top until bottom
							for newRockPosition := idxBeforeFindingCubeShapedRock; newRockPosition < (idxBeforeFindingCubeShapedRock + nRoundedRocksFoundBeforeCubeShapeRocks); newRockPosition++ {
								platformMap[rowIdx][newRockPosition] = 'O'
							}
							for newEmptySpacePosition := idxBeforeFindingCubeShapedRock + nRoundedRocksFoundBeforeCubeShapeRocks; newEmptySpacePosition < columnIdx; newEmptySpacePosition++ {
								platformMap[rowIdx][newEmptySpacePosition] = '.'
							}
						} else { // eastTilt
							for newEmptySpacePosition := idxBeforeFindingCubeShapedRock; newEmptySpacePosition < (columnIdx - nRoundedRocksFoundBeforeCubeShapeRocks); newEmptySpacePosition++ {
								platformMap[rowIdx][newEmptySpacePosition] = '.'
							}
							for newRockPositionIdx := columnIdx - nRoundedRocksFoundBeforeCubeShapeRocks; newRockPositionIdx < columnIdx; newRockPositionIdx++ {
								platformMap[rowIdx][newRockPositionIdx] = 'O'
							}
						}
					}

					idxBeforeFindingCubeShapedRock = columnIdx + 1
					nRoundedRocksFoundBeforeCubeShapeRocks = 0
				}
			}

			if nRoundedRocksFoundBeforeCubeShapeRocks != 0 {
				if tiltDirection == westTilt {
					// travel bottom from top until bottom
					for newRockPosition := idxBeforeFindingCubeShapedRock; newRockPosition < (idxBeforeFindingCubeShapedRock + nRoundedRocksFoundBeforeCubeShapeRocks); newRockPosition++ {
						platformMap[rowIdx][newRockPosition] = 'O'
					}
					for newEmptySpacePosition := idxBeforeFindingCubeShapedRock + nRoundedRocksFoundBeforeCubeShapeRocks; newEmptySpacePosition < len(platformMap[0]); newEmptySpacePosition++ {
						platformMap[rowIdx][newEmptySpacePosition] = '.'
					}
				} else { // eastTilt
					for newEmptySpacePosition := idxBeforeFindingCubeShapedRock; newEmptySpacePosition < (len(platformMap[0]) - nRoundedRocksFoundBeforeCubeShapeRocks); newEmptySpacePosition++ {
						platformMap[rowIdx][newEmptySpacePosition] = '.'
					}
					for newRockPositionIdx := len(platformMap[0]) - nRoundedRocksFoundBeforeCubeShapeRocks; newRockPositionIdx < len(platformMap[0]); newRockPositionIdx++ {
						platformMap[rowIdx][newRockPositionIdx] = 'O'
					}
				}
			}
		}
	}
}

/*
Writes the position of the rounded rocks in a slice
*/
func assignRoundedRockPositions(platformMap [][]rune, roundedRockPositions [][2]int) {
	var roundedRockIdx = 0
	for rowIdx, platformRow := range platformMap {
		for columnIdx, platformElement := range platformRow {
			if platformElement == 'O' {
				roundedRockPositions[roundedRockIdx] = [2]int{rowIdx, columnIdx}
				roundedRockIdx++
			}
		}
	}
}

func doASpinCycle(platformMap [][]rune, roundedRockPositions [][2]int) {
	tiltPlatform(platformMap, northTilt)
	tiltPlatform(platformMap, westTilt)
	tiltPlatform(platformMap, southTilt)
	tiltPlatform(platformMap, eastTilt)

	assignRoundedRockPositions(platformMap, roundedRockPositions) // writing the position of the rounded rocks in a slice allows to easily compare it with other positions
}

func doBothSlicesHaveSameElements(firstSlice [][2]int, secondSlice [][2]int) bool {
	for rowIdx := range firstSlice {
		for columnIdx := range firstSlice[rowIdx] {
			if firstSlice[rowIdx][columnIdx] != secondSlice[rowIdx][columnIdx] {
				return false
			}
		}
	}
	return true
}

func getNorthSupportBeamLoad(platformMap [][]rune) int {
	var northSupportBeamsLoad = 0
	for columnIdx := range platformMap[0] {
		for rowIdx := range platformMap {
			switch platformMap[rowIdx][columnIdx] {
			case 'O':
				northSupportBeamsLoad += len(platformMap) - rowIdx
			}
		}
	}
	return northSupportBeamsLoad
}

func solveSecondPart(platformMap [][]rune, nRoundedRocks int) {
	var originalPlatformMap = make([][]rune, len(platformMap))
	for rowIdx := range originalPlatformMap {
		originalPlatformMap[rowIdx] = make([]rune, len(platformMap[rowIdx]))
		copy(originalPlatformMap[rowIdx], platformMap[rowIdx])
	}

	var originalRoundedRockPositions = make([][2]int, nRoundedRocks)
	var roundedRockPositions = make([][2]int, nRoundedRocks)
	var previousRoundedRockPositions = make([][2]int, nRoundedRocks)
	assignRoundedRockPositions(originalPlatformMap, originalRoundedRockPositions) // writing the position of the rounded rocks in a slice allows to easily compare it with other positions
	assignRoundedRockPositions(originalPlatformMap, previousRoundedRockPositions) // writing the position of the rounded rocks in a slice allows to easily compare it with other positions

	// Brent's algorithm starts
	doASpinCycle(platformMap, roundedRockPositions)

	var currentPower = 1
	var cycleLength = 1
	var wasACycleDetected = false
	for spinCycleNumber := 1; spinCycleNumber < nSpinCycles; spinCycleNumber++ {

		if doBothSlicesHaveSameElements(roundedRockPositions, previousRoundedRockPositions) == true {
			wasACycleDetected = true
			break
		}

		if currentPower == cycleLength {
			copy(previousRoundedRockPositions, roundedRockPositions)
			currentPower *= 2
			cycleLength = 0
		}

		doASpinCycle(platformMap, roundedRockPositions)
		cycleLength++
	}

	if wasACycleDetected == true {
		for rowIdx := range originalPlatformMap {
			copy(platformMap[rowIdx], originalPlatformMap[rowIdx])
		}
		for idx := 0; idx < cycleLength; idx++ {
			doASpinCycle(platformMap, roundedRockPositions)
		}

		// platformMap now has a cycleLength difference between it and originalPlatformMap, so the starting position of the cycle can now be found

		restartedPlatformMap := originalPlatformMap
		restartedRoundedRockPositions := originalRoundedRockPositions
		var cycleStart = 0
		for doBothSlicesHaveSameElements(roundedRockPositions, restartedRoundedRockPositions) == false {
			doASpinCycle(restartedPlatformMap, restartedRoundedRockPositions)
			doASpinCycle(platformMap, roundedRockPositions)
			cycleStart++
		}

		// Brent's algorithm is over. Now it is possible to get the actual cycle map corresponding to the required number of spin cycles
		var cycleNumberAfterSpinCycles = (nSpinCycles - cycleStart) % cycleLength
		for idx := 0; idx < cycleNumberAfterSpinCycles; idx++ {
			doASpinCycle(platformMap, roundedRockPositions)
		}

	} else {
		// if no cycle is detected (unlikely using a very high number of nSpinCycles), it is not necessary to finish Brent's algorithm, as the map corresponding to the last spin cycle is already computed
	}

	var northSupportBeamsLoad = getNorthSupportBeamLoad(platformMap)
	fmt.Println("After", nSpinCycles, "spin cycles, the load on the north support beams is", northSupportBeamsLoad)
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

	var platformMap, nRoundedRocks, err = parsePuzzleFile(puzzleFilePath)
	if err != nil {
		log.Fatal(err)
	}

	solveFirstPart(platformMap)
	solveSecondPart(platformMap, nRoundedRocks)
}
