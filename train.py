from createDataSet import *
from createTrainingData import *
import sys

def startTrainer(fileNameToTrain,hypoOut,trainingMode,dataSetFileName):
	readTrainingData(fileNameToTrain, dataSetFileName)
	startTraining(dataSetFileName,trainingMode,hypoOut)

if __name__ == "__main__":
	fileNameToTrain = sys.argv[1]
	hypoOut = sys.argv[2]
	trainingMode = sys.argv[3]
	dataSetFileName = "dataset.csv"
	if(len(sys.argv) == 5):
		dataSetFileName = sys.argv[4]
	startTrainer(fileNameToTrain,hypoOut,trainingMode,dataSetFileName)

