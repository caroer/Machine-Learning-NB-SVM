# -*- coding: utf-8 -*-
def getAllowedInput():
    file = open('AllowedInput.txt', "r")
    return file.readline().split(",")

def getData():
    Golf = []
    countDict = {}
    
    file = open('TrainingDataGolf.txt', "r")
    fileData = file.readlines()

    for line in fileData:
        array = line.split(",")
        Golf.append(array[4].strip())
        
        for i in range(0,4):
            countDict[array[i].strip()+array[4].strip()] = countDict.get(array[i].strip()+array[4].strip(), 0) + 1
        
    return Golf, countDict

def getProb(golf, countDict):
    p_yes = golf.count('yes')/len(golf)
    p_no = golf.count('no')/len(golf)
    
    probDict = {}
    
    for i in countDict.keys():
        if i[-1] == 'o':
            probDict[i] = countDict[i]/p_no
        else:
            probDict[i] = countDict[i]/p_yes
    
    return probDict, p_yes, p_no
    
def getInputData():
    array = []
    allowedInput = getAllowedInput()
    prompt_var = ['WEATHER','TEMPERATURE','HUMIDITY','WIND']
    corr_valid_inp = ['Sun, Cloudy, Rain','Warm, Lagom, Cold','High, Medium', 'Strong, Weak']
    i = 0
    while i < 4:
        
        inData = input('Enter ' + prompt_var[i] + ' (' + corr_valid_inp[i] + '), or hit Return to skip this category: ').lower().strip()
        if inData == '':
            i += 1
        elif inData in allowedInput:
            array.append(inData)
            i += 1
        else:
            print('You entered invalid input argument: "' + inData + '".')
            print('Allowed input is: ' + str(allowedInput))

    return array

def calculateResult(userData, probDict, p_yes, p_no):
    yes_prod = 1
    no_prod = 1
    for i in userData:
        yes_prod *= probDict[i + 'yes']
        no_prod *= probDict[i + 'no']
    
    p_golf = yes_prod * p_yes / (yes_prod * p_yes + no_prod * p_no)
    p_no_golf = no_prod * p_no / (yes_prod * p_yes + no_prod * p_no)
    
    if p_golf > p_no_golf:
        return "\nYou're most likely golfing!\nChance of golfing: "+str(round(p_golf*100)) +"%\nChance of no golfing: " + str(round(p_no_golf*100)) + '%'
    return "\nYou're most likely staying at home!\nChance of golfing: "+str(round(p_golf*100)) +"%\nChance of no golfing: " + str(round(p_no_golf*100)) + '%'

def main():
    golf, countDict = getData()
    probDict, p_yes, p_no = getProb(golf, countDict)
    userData = getInputData()

    print(calculateResult(userData, probDict, p_yes, p_no))
    
main()





