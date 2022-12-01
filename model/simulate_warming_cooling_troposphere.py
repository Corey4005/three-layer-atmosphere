#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 14:09:42 2022

This is a module to test the climate sensitivity of the troposphere as 
compared to the stratosphere. 

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
tempChange = surfaceNext-surface #surface next is about 1.6K warmer than surface

#now we will test climate sensitivity of troposphere by increasing solar reflectance and transmission until surface is as cool as before. 
#set prior row to get change 
row2 = obj.row2

while(surfaceNext>surface):
    count += 1
    print('\n')
    print("new step: ", count, '\n')
    obj.row2+=0.002 #IR reflectivity
    obj.tau2-=0.002 #IR absorption
    obj.calculateRadiationBudget()
    obj.getTemperatures(HF=True, Params='EBM30')
    surfaceNext = obj.T3

rowChange = obj.row2-row2
relationship = tempChange/rowChange

print('\n')
print("For every 1.0 change in tropospheric solar reflectivity, you get {:.3f} change in temperature.".format(relationship))