# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 16:14:07 2020

@author: Filip & Caroline
"""
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

def getRequiredColumns(classes):
    prompt = True
    while(prompt):
        prompt = False
        inputStr = input("Enter ingredients for classification! \nAllowed input is commaseparated string of: Flour, Milk, Sugar, Butter, Egg, BakingPowder, Vanilla, Salt \n")
        #inputStr = 'sugar,butter'
        inputStr = inputStr.lower().split(",")
        retList = []
        for i in inputStr:
            temp = i.strip()
            if temp not in classes.keys():
                print("Invalid input!")
                prompt = True
                break
            retList.append(temp)
    n = len(retList) + 1
    return retList, n

def getInitialGuesses(reqCols, n):       
    # initial guesses
    x0 = np.zeros(n)
    for i in range(len(x0)):
        x0[i] = 100
    return x0

def getClassificationData(reqCols, classes):
    classificationData = {}
    for reqCol in reqCols:
        classificationData[reqCol] = []

    file = open('recipes_muffins_cupcakes.csv', "r")
    fileData = file.readlines()
    firstLap = True
    y_list = []
    for line in fileData:
        if firstLap:
            firstLap = False # First line contains class names. No data
        else:
            for reqCol in reqCols:
                classificationData[reqCol].append(int(line.split(",")[classes[reqCol]].strip("\n"))) 
            if line.split(",")[0] == "Muffin":
                y_list.append(1)
            elif line.split(",")[0] == "Cupcake":
                y_list.append(-1)
        classificationData["y"] = y_list
    return classificationData

def optPlane(initialGuesses, n):
    # optimize
    b = (-100,100)
    bnds = []
    for i in range(n):
        bnds.append(b)
    bnds = tuple(bnds)
    con1 = {'type': 'ineq', 'fun': constraint1} 
    
    cons = ([con1])
    solution = minimize(objective,initialGuesses,method='SLSQP',bounds=bnds,constraints=cons)
    return solution.x

def objective(w):
    d = 0
    for i in range(n):
        d += w[i]*w[i]*500
    # d=0.5*(w[0]*w[0]+w[1]*w[1])#*1000
    return d
  
def constraint1(w):
    y = classificationData["y"]
    x = []
    
    for reqCol in reqCols:
        x.append(classificationData.get(reqCol))
    
    #x1=(6,	8,	12,	10,	15,	13,	3,	7,	4,	8,	7,	10)
    #x2=(15,	12,	13,	10,	10,	8,	10,	7,	6,	4,	4,	2)
    #x3=(15,	12,	13,	10,	10,	8,	10,	7,	6,	4,	4,	2)
    
    y_size = len(y)
    c = np.zeros(y_size)
    temp = 0
    for i in range(y_size):
        for j in range(n-1):
            temp += w[j]*x[j][i]
        c[i]=(temp + w[n-1])*y[i]-1; #written in positive null form
        temp = 0  
    # for i in range(y_size):
    #       c[i]=(w[0]*x1[i]+w[1]*x2[i]+w[2])*y[i]-1; #written in positive null form
    return c

def classifyExternalRecipe():
    Input = input('Do you want to classify an external recipe? (Y/N)\n')
    if Input.lower() == 'n':
        print('Thank you, please come again!')
        return None
    
    input_recipe = []
    for reqCol in reqCols:
        invalid_input = True
        while invalid_input:
            try:
                Input = int(input('Enter integer amount of ' + reqCol + ': '))
                invalid_input = False
            except:
                print('You must enter an integer!')
        input_recipe.append(Input)
    
    temp = 0
    for i in range(len(input_recipe)):
        temp += hyperPlaneParams[i]*input_recipe[i]
    
    if temp + hyperPlaneParams[-1] - 1 < 0:
        print('You have entered a CUPCAKE recipe!')
    else:
        print('You have entered a MUFFIN recipe!')
        
    return None

################################ MAIN ################################################
########################## GLOBAL VARIABLES ##########################################

# The variety of allowed input classes:
classes = {"flour":1,"milk":2,"sugar":3,"butter":4,"egg":5,"bakingpowder":6,"vanilla":7,"salt":8}

# The name of the required columns, determined by the user.
reqCols, n = getRequiredColumns(classes)

# Initial guess for optimization algorithm
initialGuesses = getInitialGuesses(reqCols, n)

# The data in the columns of the file "recipes_muffins_cupcakes.csv" corresponding to reqCols 
classificationData = getClassificationData(reqCols, classes)

# The solution containing the parameters for the hyperplane
hyperPlaneParams = optPlane(initialGuesses, n)  

# The old input data
#x1=(6,8,12,10,15,13,3,7,4,8,7,10)
#x2=(15,12,13,10,10,8,10,7,6,4,4,2)

# This section is for plotting. Only viable for 2D input.
if n == 3:
    x1 = classificationData[reqCols[0]]
    x2 = classificationData[reqCols[1]]
    y2 = -hyperPlaneParams[0] * np.divide(x1, hyperPlaneParams[1]) - hyperPlaneParams[2] / hyperPlaneParams[1]
    #y2=-x[0]*x1/x[1]-x[2]/x[1]
    min1 = min(classificationData[reqCols[0]])
    max1 = max(classificationData[reqCols[0]])
    min2 = min(classificationData[reqCols[1]])
    max2 = max(classificationData[reqCols[1]])
    plt.plot(x1, x2, 'ro', x1, y2)
    plt.axis([min1, max1, min2, max2])
    plt.xlabel(reqCols[0])
    plt.ylabel(reqCols[1])
    plt.show()

classifyExternalRecipe()


