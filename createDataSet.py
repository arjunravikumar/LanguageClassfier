def readTrainingData(fileName,outPutFileName):
    inputFile = open(fileName, "r")
    outputFile = open(outPutFileName, "w+")
    outputFile.write("Feature1,Feature2,Feature3,Feature4,Feature5,Feature6,Feature7,Feature8,Feature9,Feature10,Language"+"\n")
    for trainingstringInput in inputFile:
        trainDataSplit = trainingstringInput.split("|")
        language = trainDataSplit[0]
        trainingstringInput = trainDataSplit[1]
        stringToWrite = countTheFeatures(trainingstringInput)
        outputFile.write(stringToWrite+language+"\n")
    inputFile.close()
    outputFile.close()

def countTheFeatures(stringInput):
	stringToWrite = ""
	stringToWrite = stringToWrite + str(getFeature1(stringInput)) + ","
	stringToWrite = stringToWrite + str(getFeature2(stringInput)) + ","
	stringToWrite = stringToWrite + str(getFeature3(stringInput)) + ","
	stringToWrite = stringToWrite + str(getFeature4(stringInput)) + ","
	stringToWrite = stringToWrite + str(getFeature5(stringInput)) + ","
	stringToWrite = stringToWrite + str(getFeature6(stringInput)) + ","
	stringToWrite = stringToWrite + str(getFeature7(stringInput)) + ","
	stringToWrite = stringToWrite + str(getFeature8(stringInput)) + ","
	stringToWrite = stringToWrite + str(getFeature9(stringInput)) + ","
	stringToWrite = stringToWrite + str(getFeature10(stringInput)) + ","
	return stringToWrite

def getFeaturesDict(stringInput):
	returnList = {}
	returnList["Feature1"] = getFeature1(stringInput)
	returnList["Feature2"] = getFeature2(stringInput)
	returnList["Feature3"] = getFeature3(stringInput)
	returnList["Feature4"] = getFeature4(stringInput)
	returnList["Feature5"] = getFeature5(stringInput)
	returnList["Feature6"] = getFeature6(stringInput)
	returnList["Feature7"] = getFeature7(stringInput)
	returnList["Feature8"] = getFeature8(stringInput)
	returnList["Feature9"] = getFeature9(stringInput)
	returnList["Feature10"] = getFeature10(stringInput)
	return returnList

def getFeaturesList(stringInput):
    returnList = []
    returnList.append(getFeature1(stringInput))
    returnList.append(getFeature2(stringInput))
    returnList.append(getFeature3(stringInput))
    returnList.append(getFeature4(stringInput))
    returnList.append(getFeature5(stringInput))
    returnList.append(getFeature6(stringInput))
    returnList.append(getFeature7(stringInput))
    returnList.append(getFeature8(stringInput))
    returnList.append(getFeature9(stringInput))
    returnList.append(getFeature10(stringInput))
    return returnList

		
def getFeature1(stringInput):
    words = stringInput.split()
    for word in words:
        word = word.lower().replace(',','')
        if word =='the' or word == "be" or word == 'a' or word =='an':
            return True
    return False

def getFeature2(stringInput):
    dutch = ['dat', 'dit', 'deze', 'groen', 'hij', 'een', 'haar', 'die',  'zij', 'wat', 'de', 'het', 'groene', 'wie', 'hem', 'zijn']
    words = stringInput.split()
    for word in words:
        word = word.lower().replace(',','')
        if word in dutch:
            return False
    return True

def getFeature3(stringInput):
    words = stringInput.split()
    totalLen = 0
    for word in words:
        word = word.lower().replace(',','')
        totalLen = totalLen + len(word)
    avg = totalLen / len(words)
    if(avg > 9):
        return False
    return True

def getFeature4(stringInput):
    dutch = ['niet','wat','ze', 'zijn', 'maar', 'die', 'heb','voor', 'ben','mijn','dit','hem','hebben','heeft','nu',
                'hoe', 'kom',    'gaan',    'bent',    'haar',    'doen',    'ook', 
                'daar',    'al',    'ons',    'gaat',    'hebt',    'waarom',    'deze',    'laat', 'moeten',    'wie',    'alles',    
                'kunnen',    'nooit',    'komt',    'misschien',    'iemand',    'veel',    'worden',    'onze',    'leven',    'weer',    
                'nodig',    'twee',    'tegen',    'maken', 'wordt',    'mag',    'altijd',    'wacht',    'geef',    'dag',    'zeker',    
                'allemaal',    'gedaan',    'huis',    'zij',    'jaar',    'vader',    'doet',    'vrouw',    'geld',    'hun',    'anders',    
                'zitten',    'niemand',    'binnen','spijt',    'maak',    'staat',    'werk',    'moeder',    'gezien',    'waren',    'wilde',    
                'praten',    'genoeg',    'meneer',    'klaar',    'ziet',    'elkaar',    'uur',    'zegt',    'helpen',    'helemaal',    
                'graag',    'krijgen',    'werd',    'zonder',    'naam',    'vriend',    'beetje',    'jongen',    'snel',    'geven',    'achter',
                'wanneer',    'kinderen',    'onder']
    words = stringInput.split()
    for word in words:
        word = word.lower().replace(',','')
        if word in dutch:
            return False
    return True

def getFeature5(stringInput):
    words = stringInput.split()
    for word in words:
        word = word.lower().replace(',','')
        if (word == 'omdat' or word == 'van'):
            return False
    return True

def getFeature6(stringInput):
    words = stringInput.split()
    for word in words:
        word = word.lower().replace(',','')
        if (('sch' in word) or ('tsj' in word)):
            return False
    return True

def getFeature7(stringInput):
    words = stringInput.split()
    wordCount = 0
    for word in words:
        word = word.lower().replace(',','')
        if (('zi' in word) or ('ji' in word) or ('iz' in word)):
            wordCount = wordCount + 1
    if wordCount > 3:
        return False
    return True

def getFeature8(stringInput):
    words = stringInput.split()
    wordCount = 0
    for word in words:
        word = word.lower().replace(',','')
        if (len(word) > 8):
            wordCount = wordCount + 1
        if(wordCount > 5):
            return False
    return True


def getFeature9(stringInput):
    words = stringInput.split()
    for word in words:
        word = word.lower().replace(',','')
        if (word.endswith('r') or word.endswith('i') or word.endswith('n') or word.endswith('e')):
            return False
    return True

def getFeature10(stringInput):
    words = stringInput.split()
    wordCount = 0
    for word in words:
        word = word.lower().replace(',','')
        if ('oo' in word) or ('aa' in word) or ('ii' in word) or ('ee' in word):
            wordCount = wordCount + 1
    if wordCount > 2:
        return False
    return True