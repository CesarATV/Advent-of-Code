/*
The first part is solved in a straightforward way, checking if each one of the workflows will be accepted or rejected

The second can in theory be solved as the first part, but the time it will take to do it is absurdly big. It was decided to evaluate how many ratings would be accepted by each of the rules, considering that each of them are ranges of values in which the ratings have to be. So, it is only necessary to calculate the upper and lower limit of each range
*/

package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

const (
	puzzleInputFileName        = "day19.txt"
	puzzleExampleInputFileName = "day19_example.txt"

	startingWorkflowName = "in"
	acceptedPartString   = "A"
	rejectedPartString   = "R"
	minimumRating        = 1
	maximumRating        = 4000
)

func isFirstNumberLessThanSecondNumber(firstNumber int, secondNumber int) bool {
	return firstNumber < secondNumber
}

func isFirstNumberGreaterThanSecondNumber(firstNumber int, secondNumber int) bool {
	return firstNumber > secondNumber
}

type workflowStepRuleStruct struct {
	affectedRatingName             rune
	conditionFunction              func(int, int) bool
	isConditionFunctionGreaterThan bool // only relevant for the second part, although could have been used in the first part instead of the field conditionFunction
	conditionValue                 int  // value that will be used in the condition function
	followingWorkflowName          string
}

type partRatingsStruct struct {
	x, m, a, s int
}

/* This struct is meant to contain non-inclusive limits (i.e. a number x fulfills lowerLimit < x < upperLimit) */
type ratingLimitsStruct struct {
	lowerLimit int // non-inclusive limit
	upperLimit int // non-inclusive limit
}

func (ratingLimit *ratingLimitsStruct) getRangeExtension() int {
	if ratingLimit.upperLimit <= ratingLimit.lowerLimit {
		return 0
	} else {
		return ratingLimit.upperLimit - ratingLimit.lowerLimit - 1
	}
}

type partRatingsLimitsStruct struct {
	x, m, a, s            ratingLimitsStruct
	followingWorkflowName string
}

func (partRatingsLimits *partRatingsLimitsStruct) getNumberOfRatingCombinations() int {
	return partRatingsLimits.x.getRangeExtension() * partRatingsLimits.m.getRangeExtension() * partRatingsLimits.a.getRangeExtension() * partRatingsLimits.s.getRangeExtension()
}

func parsePuzzleFile(puzzleFilePath string) (map[string][]workflowStepRuleStruct, []partRatingsStruct, error) {
	var puzzleFile, err = os.Open(puzzleFilePath)
	if err != nil {
		return nil, nil, err
	}
	defer func() {
		if err = puzzleFile.Close(); err != nil {
			log.Println(err)
		}
	}()

	var workflowsStepsRules = map[string][]workflowStepRuleStruct{} // the maps registers the workflow by its name as a key
	var fileScanner = bufio.NewScanner(puzzleFile)
	for fileScanner.Scan() {
		var fileLine = fileScanner.Text()
		if fileLine == "" {
			break
		}

		var workflowStepRules = []workflowStepRuleStruct{}
		var workflowNameAndContent = strings.Split(fileLine[:len(fileLine)-1], "{")

		var workflowStepRulesString = strings.Split(workflowNameAndContent[1], ",")
		for _, workflowStepRulestring := range workflowStepRulesString[:len(workflowStepRulesString)-1] {
			var workflowStepRule = workflowStepRuleStruct{}

			var workflowConditionAndReturn = strings.Split(workflowStepRulestring, ":")
			workflowStepRule.followingWorkflowName = workflowConditionAndReturn[1]

			var workflowCondtion = workflowConditionAndReturn[0]
			var comparisonSymbolPosition = strings.Index(workflowCondtion, ">")
			if comparisonSymbolPosition == -1 {
				comparisonSymbolPosition = strings.Index(workflowCondtion, "<")
				if comparisonSymbolPosition == -1 {
					return nil, nil, fmt.Errorf("No greater-than nor less-than symbol found in workflow: \"%s\"", workflowStepRulestring)
				}
				workflowStepRule.conditionFunction = isFirstNumberLessThanSecondNumber
				workflowStepRule.isConditionFunctionGreaterThan = false
			} else {
				workflowStepRule.conditionFunction = isFirstNumberGreaterThanSecondNumber
				workflowStepRule.isConditionFunctionGreaterThan = true
			}

			conditionValue, err := strconv.Atoi(workflowCondtion[comparisonSymbolPosition+1:])
			if err != nil {
				return nil, nil, err
			}
			workflowStepRule.conditionValue = conditionValue
			workflowStepRule.affectedRatingName = []rune(workflowCondtion[:comparisonSymbolPosition])[0]

			workflowStepRules = append(workflowStepRules, workflowStepRule)
		}

		var workflowStepRule = workflowStepRuleStruct{followingWorkflowName: workflowStepRulesString[len(workflowStepRulesString)-1]} // by design, the last workflow rule is the one that is kept when al other rule conditions fail
		workflowStepRules = append(workflowStepRules, workflowStepRule)

		var workflowName = workflowNameAndContent[0]
		workflowsStepsRules[workflowName] = workflowStepRules
	}

	err = fileScanner.Err()
	if err != nil {
		return nil, nil, err
	}

	var partRatingsSlice []partRatingsStruct
	for fileScanner.Scan() {
		var fileLine = fileScanner.Text()
		if fileLine == "" {
			continue
		}

		var partRatings = partRatingsStruct{}
		var rateValuePairs = strings.Split(fileLine[1:len(fileLine)-1], ",") // remove curly braces
		for _, rateValuePair := range rateValuePairs {

			var rateValuePairSplit = strings.Split(rateValuePair, "=")

			var rateName = []rune(rateValuePairSplit[0])[0]
			rateValue, err := strconv.Atoi(rateValuePairSplit[1])
			if err != nil {
				return nil, nil, err
			}

			switch rateName {
			case 'x':
				partRatings.x = rateValue
			case 'm':
				partRatings.m = rateValue
			case 'a':
				partRatings.a = rateValue
			case 's':
				partRatings.s = rateValue
			}
		}
		partRatingsSlice = append(partRatingsSlice, partRatings)
	}

	err = fileScanner.Err()
	if err != nil {
		return nil, nil, err
	}

	return workflowsStepsRules, partRatingsSlice, nil
}

func findFollowingWorkflowName(workflowStepRule []workflowStepRuleStruct, partRatings partRatingsStruct) string {
	for _, workflowStepRule := range workflowStepRule[:len(workflowStepRule)-1] { // iterate over all the elements bar the last, which is the default "else" condition
		var conditionFulfilled bool
		switch workflowStepRule.affectedRatingName {
		case 'x':
			conditionFulfilled = workflowStepRule.conditionFunction(partRatings.x, workflowStepRule.conditionValue)
		case 'm':
			conditionFulfilled = workflowStepRule.conditionFunction(partRatings.m, workflowStepRule.conditionValue)
		case 'a':
			conditionFulfilled = workflowStepRule.conditionFunction(partRatings.a, workflowStepRule.conditionValue)
		case 's':
			conditionFulfilled = workflowStepRule.conditionFunction(partRatings.s, workflowStepRule.conditionValue)
		}

		if conditionFulfilled == true {
			return workflowStepRule.followingWorkflowName
		}
	}

	return workflowStepRule[len(workflowStepRule)-1].followingWorkflowName
}

func solveFirstPart(workflowsStepsRules map[string][]workflowStepRuleStruct, workflowStepRule []partRatingsStruct) {
	var sumOfRatings = 0
	for _, partRatings := range workflowStepRule {
		var nextWorkflowToCheck = startingWorkflowName
		for {
			nextWorkflowToCheck = findFollowingWorkflowName(workflowsStepsRules[nextWorkflowToCheck], partRatings)

			if nextWorkflowToCheck == acceptedPartString {
				// part has been accepted
				sumOfRatings += partRatings.x + partRatings.m + partRatings.a + partRatings.s
				break
			} else if nextWorkflowToCheck == rejectedPartString {
				// part has been rejected
				break
			}
		}
	}

	println("Adding the rating numbers for all accepted parts gives", sumOfRatings)
}

/*
The function begins with a starting workflow inside a slice, and then keeps adding workflows to this slice. These added workflows are the product of the different conditions inside each workflow, each condition may generate one or cause a part to be accepted or rejected. Every element of the slice is analized to check if it will create a workflow or not

Different instances of ratingLimitsStruct, a structure keeping track of the limits of the workflows, are created and kept for every workflow in the slice
*/
func solveSecondPart(workflowsStepsRules map[string][]workflowStepRuleStruct) {
	var initialAllRates = partRatingsLimitsStruct{followingWorkflowName: startingWorkflowName}
	initialAllRates.x = ratingLimitsStruct{lowerLimit: minimumRating - 1, upperLimit: maximumRating + 1}
	initialAllRates.m = ratingLimitsStruct{lowerLimit: minimumRating - 1, upperLimit: maximumRating + 1}
	initialAllRates.a = ratingLimitsStruct{lowerLimit: minimumRating - 1, upperLimit: maximumRating + 1}
	initialAllRates.s = ratingLimitsStruct{lowerLimit: minimumRating - 1, upperLimit: maximumRating + 1}

	var ratingLimitsToCheck = []partRatingsLimitsStruct{initialAllRates}
	var numberOfAcceptableRatings = 0
	for len(ratingLimitsToCheck) != 0 {
		var currentRatingLimits = ratingLimitsToCheck[len(ratingLimitsToCheck)-1]
		ratingLimitsToCheck = ratingLimitsToCheck[:len(ratingLimitsToCheck)-1] // remove the rating that was just retrieved

		var workflowStepRules = workflowsStepsRules[currentRatingLimits.followingWorkflowName]
		for _, workflowStepRule := range workflowStepRules[:len(workflowStepRules)-1] { // iterate over all the elements bar the last, which is one used when all other step rule conditions are proven false

			var ratingThatPassedCondition = currentRatingLimits // create a copy of the current ratings to store the ratings that pass the condition associated with this workflow step

			var limitFromRatingThatPassedCondition *ratingLimitsStruct
			var limitFromRatingThatFailedCondition *ratingLimitsStruct // reuse the current ratings to store the ratings that do not pass the condition associated with this workflow step. This will also low the following workflow-steps to keep their limit values correct
			switch workflowStepRule.affectedRatingName {
			case 'x':
				limitFromRatingThatPassedCondition = &ratingThatPassedCondition.x
				limitFromRatingThatFailedCondition = &currentRatingLimits.x
			case 'm':
				limitFromRatingThatPassedCondition = &ratingThatPassedCondition.m
				limitFromRatingThatFailedCondition = &currentRatingLimits.m
			case 'a':
				limitFromRatingThatPassedCondition = &ratingThatPassedCondition.a
				limitFromRatingThatFailedCondition = &currentRatingLimits.a
			case 's':
				limitFromRatingThatPassedCondition = &ratingThatPassedCondition.s
				limitFromRatingThatFailedCondition = &currentRatingLimits.s
			}

			if workflowStepRule.isConditionFunctionGreaterThan == true {
				if limitFromRatingThatPassedCondition.lowerLimit < workflowStepRule.conditionValue {
					limitFromRatingThatPassedCondition.lowerLimit = workflowStepRule.conditionValue
				}
				if limitFromRatingThatFailedCondition.upperLimit > workflowStepRule.conditionValue {
					limitFromRatingThatFailedCondition.upperLimit = workflowStepRule.conditionValue + 1
				}
			} else {
				if limitFromRatingThatPassedCondition.upperLimit > workflowStepRule.conditionValue {
					limitFromRatingThatPassedCondition.upperLimit = workflowStepRule.conditionValue
				}
				if limitFromRatingThatFailedCondition.lowerLimit < workflowStepRule.conditionValue {
					limitFromRatingThatFailedCondition.lowerLimit = workflowStepRule.conditionValue - 1
				}
			}

			if workflowStepRule.followingWorkflowName == acceptedPartString {
				numberOfAcceptableRatings += ratingThatPassedCondition.getNumberOfRatingCombinations()
			} else if workflowStepRule.followingWorkflowName != rejectedPartString {
				ratingThatPassedCondition.followingWorkflowName = workflowStepRule.followingWorkflowName
				ratingLimitsToCheck = append(ratingLimitsToCheck, ratingThatPassedCondition) // analize the following workflow, until a decision is made about the rating associated with it
			}
		}

		// evaluate the last possible workflow (the default one when all the conditions are proven false)
		if workflowStepRules[len(workflowStepRules)-1].followingWorkflowName == acceptedPartString {
			numberOfAcceptableRatings += currentRatingLimits.getNumberOfRatingCombinations()
		} else if workflowStepRules[len(workflowStepRules)-1].followingWorkflowName != rejectedPartString {
			currentRatingLimits.followingWorkflowName = workflowStepRules[len(workflowStepRules)-1].followingWorkflowName
			ratingLimitsToCheck = append(ratingLimitsToCheck, currentRatingLimits)
		}
	}

	println("The workflows will accept", numberOfAcceptableRatings, "combinations of ratings")
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

	var workflowsStepsRules, partRatingsSlice, err = parsePuzzleFile(puzzleFilePath)
	if err != nil {
		log.Fatal(err)
	}

	solveFirstPart(workflowsStepsRules, partRatingsSlice)
	solveSecondPart(workflowsStepsRules)
}
