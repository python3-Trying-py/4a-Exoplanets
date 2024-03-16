# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 02:06:24 2024

@author: payta

"""

import pandas as pd
import matplotlib.pyplot as plt
import math

#The following function filters the dataframe by reading through "pl_controv_flag". If the value in a
#row is C, then that row is kept, if it is not then it is removed from the dataframe
def filterConfirm(C = 0):
    #epl is shorthand for Exo Planet
    #creates a dataframe using our csv file
    epl = pd.read_csv("Exoplanet_Archive2.2024.csv", skiprows = 96)
    #Checks if the value in the dataframe matches C
    eplFiltered = epl[epl["pl_controv_flag"] == C]
    
    return eplFiltered

#This function is the same as filterConfirm, except it can filter any column. I keep these as seperate
#functions for ease of reading
#The function also have a variable called "Type". This simply determines wether C is a whitelist or blacklist
#Setting Type to White will keep all values that match C, and Black will do the opposite
def filterDF(df, column, C, Type = "white"):
    
    if (Type == "white"):
        dfFiltered = df[df[column] == C]
    elif (Type == "black"):
        dfFiltered = df[df[column] != C]
    
    return dfFiltered

#This function takes a column of data and creates a histogram using the data
def distribution(column):
    
    #This gives us our filtered data
    epl = filterConfirm()
    
    #The try/except statements below are a failsafe because some columns contain out of place data types
    try:
        
        #Here we set the range of our data so we can customize our number of bins
        #Fist we grab the smallest value in our data
        #Then the largest value
        #Takes the difference between the two, sets the value to an integer and adds one so no data gets cut
        lower = epl[column].min()
        upper = epl[column].max()
        rang = int((upper - lower)) + 1

        #And here the program creates the histogram with a logorthmic scale
        hist = epl.hist(column, bins = rang, log = True)
    
    except:
        #prints this text if data can't be plotted on a histogram
        print("Invalid Data Type")
        
#This function will create a dictionary where the keys are listed values and their corresponding values
#are their number of occurances
def makedict(column):
    
    #filters our data
    epl = filterConfirm()

    #creates our dictionary
    dicti = {}
    
    #Here we iterate through evrey value in a given column. If the value is already in our dictionary
    #then we increase the corresponding value by 1. If the value is new, then we create a new value
    #for it and set it equal to 1
    for col in epl[column]:
        if col in dicti:
            dicti[col] += 1
        else:
            dicti[col] = 1
    return dicti

#This function finds the percentage of singel somethings within our data
#In the program we use it to find the percetage of systems with a single star or planet
def percentSingle(column):
    #Here we make a dictionary with all our values
    itemNum = makedict(column)
    
    #this value will be the total number of somethings in all systems
    totItem = 0
    
    #here we iterate through the entire dictionary to fill totItem
    for i in range(len(itemNum)):
        totItem += itemNum[i + 1]
    
    #and here we calculate the percentage
    itemPer = (totItem - itemNum[1]) / totItem
    
    return itemPer
       


#Final outputs below
#1
epl = filterConfirm()

#2
"""
def distribution(column):
    
    epl = filterConfirm()
    
    try:
        
        lower = epl[column].min()
        upper = epl[column].max()
        rang = int((upper - lower) / 1)

        
        hist = epl.hist(column, bins = rang, log = True)
    
    except:
        print("Invalid Data Type")
        
        
Note: The functionality will be demonstrated in part 4b
"""

#3a       
disMeth = makedict("discoverymethod")
print(disMeth)

#3b
singleStarPer = percentSingle("sy_snum")

print(str(singleStarPer) + "% of confirmed systems have a single star")

#3c
singlePlanPer = percentSingle("sy_pnum")
print(str(singlePlanPer) + "% of confirmed systems have a single exoplanet")

#3d
#filters our data
epl = filterConfirm()

#further filters our data
eplSingleSt = filterDF(epl, "sy_snum", 1, "white")

#grasb the length of data we are wokring with and creates to lists to store data
n = len(eplSingleSt["pl_bmasse"])
stmass = []
sterror = []

#iterates through the data to preform the calculation of Stellar mass
for i in range(n):
    try:
        #here we grab data and convert to si units
        m = 5.972 * pow(10, 24) * (eplSingleSt.iloc[i, 27])#"pl_bmasse" converted to kilograms
        a = 1.496 * pow(10, 11) * eplSingleSt.iloc[i, 15]#"pl_orbsmax" converted to meters
        T = 86400 * eplSingleSt.iloc[i, 11]#"pl_orbper" converted to seconds
        if (T == 0):
            T = 0.0000000001
    
    except:
        continue
    
    G = 6.67 * (pow(10,-11)) #in m^3 kg^-1 s^-2
    pi = math.pi
    
    #here we calculate the stellar mass in si units
    siStMass = (((pow(a, 3)) / G) * ((pow((2 * pi / T),2)))) - m #in kilograms
    #here we convert the stellar mass into solar mass
    EmStMass = siStMass / (1.988 * pow(10, 30)) #converts to solar masses
    
    #here we calculate the percent error
    starMass = eplSingleSt.iloc[i, 59]
    calError = (starMass - EmStMass) / starMass

    #here we fill the in our dataframe with the new data
    stmass.append(EmStMass)
    sterror.append(calError)

eplSingleSt.insert(92, "st_calmass", stmass, True)
eplSingleSt.insert(93, "st_mass", sterror, True)

#4a
epl.plot.scatter("disc_year", "pl_rade", logy = True)
#we are getting better at finding small planets

#4b
distribution("st_mass")

#4c
epl.plot.scatter(x = 'sy_dist', y = 'st_teff', c = "pl_eqt", cmap = "hot", logy = True)




            
            
            

    