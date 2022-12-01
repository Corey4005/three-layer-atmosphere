#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This will simulate the sensitivity of the surface to a change in solar reflectivity. 

@author: coreywalker
"""

from modelEquations import model


#textfile location for starting values
model_params = './EBM30.txt'

obj = model()

#get values from textfile and set them to class attributes
obj.setVariables(model_params)

#create some lists to store various temps 
l3_temps = [] #surface temp list 
row1_list = []
tau1_list = []

#first we will calculate what the starting surface temp is
obj.calculateRadiationBudget()
obj.getTemperatures(HF=True, Params='EBM30')
surface = obj.T3

surfaceNext = surface #setting surfaceNext to surface for first calculation
count = 0 #to count the number of loops 

while(surfaceNext-surface)<=1.5:
    count += 1
    print('\n')
    print("new step: ", count, '\n')
    obj.r2+=0.002 #IR reflectivity
    obj.a2-=0.002 #IR absorption
    obj.calculateRadiationBudget()
    obj.getTemperatures(HF=True, Params='EBM30')
    surfaceNext = obj.T3
    
print('\n')   
print("The thermal reflectivity and absorbtivity that would create 1.5K warming is {:.3f} and {:.3f}.".format(obj.r2, obj.a2))

#here we want to calculate the change in temperature from 
tempChange = surfaceNext-surface

count2 = 0# the count of the second while loop

#the row we got when we changed the temp 1.5K in troposphere
row = obj.row3

#now we will change the surface albedo and measure it with temp change at surface
while(surfaceNext>surface):
    count2+=1
    print('\n')
    print("new step: ", count, '\n')
    obj.row3+=0.002 #solar reflectivity surface
    obj.alpha3-=0.002 #solar transmission surface
    obj.calculateRadiationBudget()
    obj.getTemperatures(HF=True, Params='EBM30')
    surfaceNext = obj.T3

print('\n')
print("The solar reflectivity and transmission that would reduce the temperature back to {:.3f} is {:.3f} and {:.3f}".format(surface, obj.row1, obj.tau1))

#the rowchange from cooling the surface atmosphere back down 
rowChange = obj.row3-row

#calculate the change in temp with respect to change in reflectivity 
#how much change in temp do you get for 1.0 increase in row
relationship = tempChange/rowChange
print('\n')
print("For every 1.0 change in surface solar reflectivity, you get {:.3f} change in temperature.".format(relationship))