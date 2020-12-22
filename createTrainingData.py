import sys
import math
import copy
import pickle
import numpy as np
from TreeNode import *

languages = ['en','nl']
featureList = []
attribute = None

def startTraining(dataSetFileName, learningMode, hypoFname):
    global featureList
    loadDataFromFile(dataSetFileName)
    getLearningData(featureList[:],learningMode,hypoFname)

def loadDataFromFile(dataSetFileName):
    global featureList
    global attribute
    dataset = open(dataSetFileName, "r")
    numberOfRows = 0
    for dataLine in dataset:
        numberOfRows =  numberOfRows+1;
        if(attribute is None):
            dataLine = dataLine.replace("\n","")
            attribute = dataLine.split(",")
            featureList.append(attribute)
        else:
            dataLine = dataLine.replace("\n","")
            data = dataLine.split(",")
            featureList.append(data)

def calculateEntropy(countofLang1,countOfLan2):
    if countofLang1 > 0 and countOfLan2 > 0:
        f1 = countofLang1/(countofLang1+countOfLan2)
        f2 = countOfLan2/(countofLang1+countOfLan2)
        entropy = -1*((f1*math.log(f1,2)) + (f2*math.log(f2,2)))
    else:
        entropy = 0
    return entropy

def traverseThroughTree(root):
    if(root is not None):
        print(root.value)
        traverseThroughTree(root.leftChild)
        traverseThroughTree(root.rightChild)

def getLearningData(features,learningMode,hypoFname):
    if learningMode == 'dt':
        decisionTree = getDecisionTree(features, features)
        pickle.dump(decisionTree, open(hypoFname,'wb'))
        
    elif learningMode == 'ada':
        weights, decisionStumsID = getAdaBoost(features)
        pickle.dump([weights,decisionStumsID], open(hypoFname,'wb'))

def getDecisionTree(features, ancestor):
    global languages
    if len(features) == 1:
        lang1 = 0
        lang2 = 0
        for data in ancestor:
            lastIndex = len(data)-1
            if data[lastIndex] == languages[0]:
                lang1 = lang1 + 1
            if data[lastIndex] == languages[1]:
                lang2 = lang2 + 1
        if lang2 >= lang1:
            return DecisionTreeNode(languages[1])
        if lang1 > lang2:
            return DecisionTreeNode(languages[0])
    if len(features[0]) == 2:
        lang1 = 0
        lang2 = 0
        for data in features:
            lastIndex = len(data)-1
            if data[lastIndex] == languages[0]:
                lang1 = lang1 + 1
            if data[lastIndex] == languages[1]:
                lang2 = lang2 + 1
        if lang2 >= lang1:
            return DecisionTreeNode(languages[1])
        if lang1 > lang2:
            return DecisionTreeNode(languages[0])
    else:
        featureCopy = copy.deepcopy(features)
        lang1, lan2 = calculateDist(featureCopy)
        labels = featureCopy[0]
        splitIndex = calculateSplitNode(featureCopy, calculateEntropy(lang1, lan2))
        labels.pop(splitIndex)
        
        leftChild = []
        rightChild = []
        
        leftChild.insert(0, labels)
        rightChild.insert(0, labels)
        
        for i in range(1, len(featureCopy)):
            if(featureCopy[i][splitIndex] == "True"):
                featureCopy[i].pop(splitIndex)
                leftChild.append(featureCopy[i])
            elif(featureCopy[i][splitIndex] == "False"):
                featureCopy[i].pop(splitIndex)
                rightChild.append(featureCopy[i])
        
        currNode = DecisionTreeNode(features[0][splitIndex])
        currNode.leftChild = getDecisionTree(leftChild, ancestor)
        currNode.rightChild = getDecisionTree(rightChild, ancestor)
        return currNode

def calculateDist(features):
    global languages
    lang1 = 0
    lang2 = 0
    for i in range(len(features)):
        lastIndex = len(features[i])-1
        if features[i][lastIndex] == languages[0]:
            lang1 = lang1 + 1
        elif features[i][lastIndex] == languages[1]:
            lang2 = lang2 + 1
    return lang1, lang2

def calculateSplitNode(features, entropy):
    global languages
    gains = []
    for i in range(0, len(features[0])-1):
        lang1True = 0
        lang1False = 0
        lang2False = 0
        lang2True = 0
        for data in features:
            lang = data[len(data)-1]
            if(lang == languages[0]):
                if(data[i] == "True"):
                    lang1True = lang1True + 1
                elif(data[i] == "False"):
                    lang1False = lang1False + 1
            if(lang == languages[1]):
                if(data[i] == "True"):
                    lang2True = lang2True + 1
                elif(data[i] == "False"):
                    lang2False = lang2False + 1
        
        total = lang1True + lang2True + lang1False + lang2False
        childrenWithTrueEntropy = calculateEntropy(lang1True, lang2True) 
        childrenWithFalseEntropy = calculateEntropy(lang1False, lang2False)
        
        childrenWithTrueEntropy = (lang1True + lang2True / total)*childrenWithTrueEntropy
        childrenWithFalseEntropy = (lang1False + lang2False / total)*childrenWithFalseEntropy
        
        entropySplit = childrenWithTrueEntropy + childrenWithFalseEntropy
        
        locGain = entropy - entropySplit
        gains.append(locGain)
    
    return gains.index(max(gains))

def getAdaBoost(features):
    sampleWeights = [1 / len(features)] * len(features)
    numberOfClassfiers = 50
    finalStumpValues = []

    hypothesisWeights = [1] * numberOfClassfiers
    languages = []
    features = features[1:]
    for i in range(0,len(features)):
        languages.append(features[i][len(features[i])-1])
        features[i] = features[i][0:len(features[i])-1]

    for hypothesisIndex in range(0, numberOfClassfiers):
        error = 0
        stump = getStump(DecisionTreeNode(""), features, languages, sampleWeights)
        for index in range(len(features)):
            if valueFromTheCSV(stump, features, index) != languages[index]:
                error = error + sampleWeights[index]
        if(error == 0 or error > 1):
            return finalStumpValues, hypothesisWeights 
        amountOfSay = (0.5 * math.log(((1-error)/error),2))
        for index in range(len(features)):
            if valueFromTheCSV(stump, features, index) == languages[index]:
                sampleWeights[index] = sampleWeights[index] * math.exp(-amountOfSay)
            else:
                sampleWeights[index] = sampleWeights[index] * math.exp(amountOfSay)
        sampleWeights = normalizeweights(sampleWeights)
        hypothesisWeights[hypothesisIndex] = amountOfSay
        finalStumpValues.append(stump)
    return finalStumpValues, hypothesisWeights


def normalizeweights(sampleWeights):
    totalWeightsSum = 0
    for weight in sampleWeights:
        totalWeightsSum += weight
    for index in range(len(sampleWeights)):
        sampleWeights[index] = sampleWeights[index] / totalWeightsSum
    return sampleWeights


def valueFromTheCSV(stump, features, index):
    attributeValue = stump.value
    if features[index][attributeValue] == "True":
        return stump.leftChild.value
    else:
        return stump.rightChild.value

def getStump(node, features, results, weights):
    maxGain = getMaxGainBoost(features, results, weights)

    node.value = maxGain
    totalTrueEnglish = 0
    totalTrueDutch = 0
    totalFalseEnglish = 0
    totalFalseDutch = 0

    for index in range(len(features[maxGain])):
        if features[maxGain][index] == "True":
            if results[index] == 'en':
                totalTrueEnglish = totalTrueEnglish + 1 * weights[index]
            elif results[index] == 'nl':
                totalTrueDutch = totalTrueDutch + 1 * weights[index]
        else:
            if results[index] == 'en':
                totalFalseEnglish = totalFalseEnglish + 1 * weights[index]
            elif results[index] == 'nl':
                totalFalseDutch = totalFalseDutch + 1 * weights[index]

    left = DecisionTreeNode("")
    right = DecisionTreeNode("")
    if totalTrueEnglish > totalTrueDutch:
        left.value = 'en'
    else:
        left.value = 'nl'
    if totalFalseEnglish > totalFalseDutch:
        right.value = 'en'
    else:
        right.value = 'nl'

    node.leftChild = left
    node.rightChild = right

    return node

def getMaxGainBoost(features,results,weights):
    gain = []
    englishTotal = 0
    dutchTotal = 0
    for index in range(0,len(features)):
        if results[index] == 'en':
            englishTotal = englishTotal + 1 * weights[index]
        else:
            dutchTotal = dutchTotal + 1 * weights[index]
    for attributeIndex in range(len(features[0])):
        trueEnglish = 0
        trueDutch = 0
        falseEnglish = 0
        falseDutch = 0
        for index in range(len(features)):
            if features[index][attributeIndex] == "True":
                if(results[index] == "en"):
                    trueEnglish = trueEnglish + 1 * weights[attributeIndex]
                elif(results[index] == "nl"):
                    trueDutch = trueDutch + 1 * weights[attributeIndex]
            elif features[index][attributeIndex] == "False":
                if(results[index] == "en"):
                    falseEnglish = falseEnglish + 1 * weights[attributeIndex]
            elif features[index][attributeIndex] == "False":
                if(results[index] == "nl"):
                    falseDutch = falseDutch + 1 * weights[attributeIndex]

        if trueEnglish == 0:
            trueValue = 0
            falseValue = ((falseEnglish + falseDutch) / (dutchTotal + englishTotal)) * boostEntropy(falseEnglish / (falseDutch + falseEnglish))
        elif falseEnglish == 0:
            falseValue = 0
            trueValue = ((trueEnglish + trueDutch) / (dutchTotal + englishTotal)) * boostEntropy(trueEnglish / (trueDutch + trueEnglish))
        else:
            trueValue = ((trueEnglish + trueDutch) / (dutchTotal + englishTotal)) * boostEntropy(trueEnglish / (trueDutch + trueEnglish))

            falseValue = ((falseEnglish + falseDutch) / (dutchTotal + englishTotal)) * boostEntropy(falseEnglish / (falseDutch + falseEnglish))

        gainAtts = boostEntropy(englishTotal / (englishTotal + dutchTotal)) - (trueValue + falseValue)
        gain.append(gainAtts)
    return gain.index(max(gain))

def boostEntropy(value):
    if value == 1:
        return 0
    return (-1) * (value * math.log(value, 2.0) + (1 - value) * math.log((1 - value), 2.0))

def getDecisionStumpPrediction(stump_id, row):
    global featureList
    if(featureList[row][stump_id] == "True"):
        return "en"
    return "nl"
