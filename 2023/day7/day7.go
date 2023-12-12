package main

import (
	"bufio"
	"errors"
	"fmt"
	"log"
	"os"
	"slices"
	"strconv"
	"strings"
)

const (
	puzzleInputFileName        = "day7.txt"
	puzzleExampleInputFileName = "day7_example.txt"
)

// the order of these enumerations is intentional, from less valuable to less valuable card set
const (
	highCard = iota
	onePair
	twoPairs
	threeOfAKind
	fullHouse
	fourOfAKind
	fiveOfAKind
)

const numberOfCardsInAHand = 5

type handDetailsStruct struct {
	handType            int // will follow the previously declared enumeration
	bidAmount           int
	handAsStrengthValue [numberOfCardsInAHand]uint
}

func selectHandType(handCount map[rune]uint, usingJokers bool) (int, error) {
	var handType int
	var numberOfJs = handCount['J']
	switch len(handCount) {
	case numberOfCardsInAHand:
		if usingJokers == false || numberOfJs == 0 {
			handType = highCard
		} else {
			handType = onePair
		}

	case numberOfCardsInAHand - 1:
		if usingJokers == false || numberOfJs == 0 {
			handType = onePair
		} else {
			handType = threeOfAKind
		}

	case numberOfCardsInAHand - 2:
		for _, numberOfcardsInSet := range handCount {
			if numberOfcardsInSet == 2 {
				if usingJokers == false || numberOfJs == 0 {
					handType = twoPairs
				} else if numberOfJs == 1 {
					handType = fullHouse
				} else {
					handType = fourOfAKind
				}
				break
			} else if numberOfcardsInSet == 3 {
				if usingJokers == false || numberOfJs == 0 {
					handType = threeOfAKind
				} else {
					handType = fourOfAKind
				}
				break
			}
		}

	case numberOfCardsInAHand - 3:
		if usingJokers == false || numberOfJs == 0 {
			for _, numberOfcardsInSet := range handCount {
				if numberOfcardsInSet == 3 {
					handType = fullHouse
					break
				} else if numberOfcardsInSet == 4 {
					handType = fourOfAKind
					break
				}
			}
		} else {
			handType = fiveOfAKind
		}

	case numberOfCardsInAHand - 4:
		handType = fiveOfAKind

	default:
		return 0, errors.New(fmt.Sprintf("File contains a file in the wrong format. It shows an impossible number of cards: %d", len(handCount)))
	}

	return handType, nil
}

func getHandStrengthValue(hand string, usingJokers bool) [numberOfCardsInAHand]uint {
	// the values of strength assigned almost arbitrarily. They were selected to exploit the fact that the numbers as runes follow the same comparison order as the numbers as integers (e.g. '2' > '1'). The importance of the values is that they follow the required order with respect to the type of card
	var handAsStrengthValue [numberOfCardsInAHand]uint
	for idx, card := range hand {
		switch card {
		case 'T':
			handAsStrengthValue[idx] = '9' + 1
		case 'J':
			if usingJokers == true {
				handAsStrengthValue[idx] = '0'
			} else {
				handAsStrengthValue[idx] = '9' + 2
			}
		case 'Q':
			handAsStrengthValue[idx] = '9' + 3
		case 'K':
			handAsStrengthValue[idx] = '9' + 4
		case 'A':
			handAsStrengthValue[idx] = '9' + 5
		default:
			handAsStrengthValue[idx] = uint(card)
		}
	}

	return handAsStrengthValue
}

func parsePuzzleFile(puzzleFile *os.File) ([]handDetailsStruct, []handDetailsStruct, error) {
	var allHandDetailsFirstPart []handDetailsStruct
	var allHandDetailsSecondPart []handDetailsStruct

	var fileScanner = bufio.NewScanner(puzzleFile)
	for fileScanner.Scan() {
		var handAndbidAmount = strings.Fields(fileScanner.Text())
		var hand = handAndbidAmount[0]

		bidAmount, err := strconv.Atoi(handAndbidAmount[1])
		if err != nil {
			return nil, nil, err
		}

		var handCount = map[rune]uint{}
		for _, card := range hand {
			handCount[card]++
		}

		handTypeFirstPart, err := selectHandType(handCount, false)
		if err != nil {
			return nil, nil, err
		}
		handTypeSecondPart, err := selectHandType(handCount, true)
		if err != nil {
			return nil, nil, err
		}

		var handAsStrengthValueFirstPart = getHandStrengthValue(hand, false)
		var handAsStrengthValueSecondPart = getHandStrengthValue(hand, true)

		allHandDetailsFirstPart = append(allHandDetailsFirstPart, handDetailsStruct{handTypeFirstPart, bidAmount, handAsStrengthValueFirstPart})
		allHandDetailsSecondPart = append(allHandDetailsSecondPart, handDetailsStruct{handTypeSecondPart, bidAmount, handAsStrengthValueSecondPart})
	}

	var err = fileScanner.Err()
	if err != nil {
		return nil, nil, err
	}

	return allHandDetailsFirstPart, allHandDetailsSecondPart, nil
}

// if the first hand has bigger rank than the second, 1 is returned. If it has less rank, -1 is returned. If both have the same rank a 0 is returned
func compareHands(firstHand handDetailsStruct, secondHand handDetailsStruct) int {
	if firstHand.handType > secondHand.handType {
		return 1
	} else if firstHand.handType < secondHand.handType {
		return -1
	} else {
		for idx := 0; idx < len(firstHand.handAsStrengthValue); idx++ {
			if firstHand.handAsStrengthValue[idx] > secondHand.handAsStrengthValue[idx] {
				return 1
			} else if firstHand.handAsStrengthValue[idx] < secondHand.handAsStrengthValue[idx] {
				return -1
			}
		}
	}

	return 0
}

func solveBothParts(allHandDetails []handDetailsStruct, considerJokerRule bool) {
	slices.SortFunc[[]handDetailsStruct](allHandDetails, compareHands) // sorts in ascending order

	var totalWinnings = 0
	for rank, handDetails := range allHandDetails {
		totalWinnings += handDetails.bidAmount * (rank + 1)
	}

	if considerJokerRule == false {
		println("The total winnings are", totalWinnings)
	} else {
		println("The total winnings are", totalWinnings, "when considering the joker rule")
	}

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

	puzzleFile, err := os.Open(filePath)
	if err != nil {
		log.Fatal(err)
	}
	defer func() {
		if err := puzzleFile.Close(); err != nil {
			log.Panicln(err)
		}
	}()

	allHandDetailsFirstPart, allHandDetailsSecondPart, err := parsePuzzleFile(puzzleFile)
	if err != nil {
		log.Fatal(err)
	}

	var solveFirstPart = solveBothParts
	solveFirstPart(allHandDetailsFirstPart, false)
	var solveSecondPart = solveBothParts
	solveSecondPart(allHandDetailsSecondPart, true)
}
