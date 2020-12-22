import sys

output = open(sys.argv[3], "a+")
inputFile = open(sys.argv[2], "r")
for trainingstringInput in inputFile:
	line = trainingstringInput.split()
	stringInput = ""
	for i in range(1,len(line)):
		stringInput = stringInput + line[i] + " "
		if(i%15 == 0):
			output.write(sys.argv[1]+"|"+stringInput+"\n")
			stringInput = ""