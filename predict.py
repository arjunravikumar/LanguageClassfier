import sys
import math
import copy
import pickle
import numpy as np
from TreeNode import *
from createDataSet import *

def startPrediction(hypothesis,fileName,trainingMode):
	fileLine = ''
	toPredictFile = open(fileName, "r")
	for fileLine in toPredictFile:
		if trainingMode == 'dt':
			decisionTree = pickle.load(open(hypothesis,'rb'))
			featureforString = getFeaturesDict(fileLine)
			prediction = languagePredictorDecisionTree(featureforString, decisionTree)
			print(prediction)
		elif trainingMode == 'ada':
			model = pickle.load(open(hypothesis,'rb'))
			prediction = languagePredictorAdaboost(fileLine, model[0], model[1])
			print(prediction)

def languagePredictorDecisionTree(featuresForString, tree):
	root = tree
	while(root.value != 'nl' and root.value != 'en'):
		feature = root.value
		if(featuresForString[feature] == True):
			root = root.leftChild
		if(featuresForString[feature] == False):
			root = root.rightChild
	return root.value

def stumpPrediction(stump_id, input_sample):
	return getFeaturesList(input_sample)[stump_id]

def languagePredictorAdaboost(stringFromFile, decisionStumps, weights):
	sum = 0
	for index in range(len(weights)):
		if(index <  len(decisionStumps)):
			sum += getPredictionValue(decisionStumps[index], stringFromFile) * weights[index]
	if sum > 0:
		return 'en'
	else:
		return 'nl'

def getPredictionValue(stump, sentence):
    arrtributeVal = stump.value
    if stumpPrediction(arrtributeVal,sentence) == True:
        if stump.leftChild.value == 'en':
            return 1
        else:
            return -1
    else:
        if stump.rightChild.value == 'en':
            return 1
        else:
            return -1

if __name__ == "__main__":
	hypothesis = sys.argv[1]
	outputFName = sys.argv[2]
	trainingMode = sys.argv[3]
	startPrediction(hypothesis,outputFName,trainingMode)