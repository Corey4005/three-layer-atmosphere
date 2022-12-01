#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 10:03:21 2022

This is a module to demonstrate how you can find new parameters utilizing a 
temperature condition. In this case, we will increase thermal reflectivity and 
absorptivity until a warming of 1.5 Kelvins are achieved. Then, we will calculate 
new solar transmission and reflectivity to see what it would take to bring the temperature
back down by 1.5K. 

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

#the row we got when we changed the temp 1.5K
row = obj.row1

while(surfaceNext>surface):
    count2+=1
    print('\n')
    print("new step: ", count, '\n')
    obj.row1+=0.002 #solar reflectivity
    obj.tau1-=0.002 #solar transmission
    obj.calculateRadiationBudget()
    obj.getTemperatures(HF=True, Params='EBM30')
    surfaceNext = obj.T3

print('\n')
print("The solar reflectivity and transmission that would reduce the temperature back to {:.3f} is {:.3f} and {:.3f}".format(surface, obj.row1, obj.tau1))

#the rowchange from cooling the atmosphere back down 
rowChange = obj.row1-row

#calculate the change in temp with respect to change in reflectivity 
#how much change in temp do you get for 1.0 increase in row
relationship = tempChange/rowChange
print('\n')
print("For every 1.0 change in stratospheric solar reflectivity, you get {:.3f} change in temperature.".format(relationship))