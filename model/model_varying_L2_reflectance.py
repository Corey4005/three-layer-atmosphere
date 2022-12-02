#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 12:29:03 2022

This is a module to demonstrate the effect of small changes in solar reflectivity 
in the troposphere and absorption on the surface temperature. This is to simulate the effect of aerosols on the troposphere. 
Returns a plot after increasing solar reflectance and decreasing solar absorption. 

@author: coreywalker
"""
from modelEquations import model
import pandas as pd
import matplotlib.pyplot as plt

#textfile location for starting values
model_params = './EBM30.txt'

obj = model()

#get values from textfile and set them to class attributes
obj.setVariables(model_params)

#create some lists to store various temps 
l3_temps = [] #surface temp list 
row2_list = []
alpha2_list = []

#calcu
steps = (0.265-0.245)/0.002 #we want to increase reflectivity from 0.265-0.245 by 0.002
for i in range(int(steps)):
    obj.calculateRadiationBudget()
    print('step ' + str(i), '\n')
    obj.getTemperatures(HF=True, Params='EBM30') 
    print('\n')
    l3_temps.append(obj.T3)
    row2_list.append(obj.row2)
    alpha2_list.append(obj.alpha2)
    obj.row2+=0.002 #increase solar reflectance by 0.002
    obj.alpha2-=0.002 #decrease solar reflectance by 0.002
    


#dataframe to observe the calculations
df = pd.DataFrame()
df['Surface'] = l3_temps
df['L2 Reflectance'] = row2_list

#set index
df.set_index('L2 Reflectance', inplace=True)

#plot 
fig, ax = plt.subplots()
ax.plot(df, label=df.columns)
ax.set_xlabel('L2 Reflectance')
ax.set_ylabel('Surface Temp - K')
ax.set_title('Tropospheric (L2) Reflectance vs Surface Temperature')






