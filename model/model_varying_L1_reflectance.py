#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This is a module to demonstrate the effect of small changes in solar reflectivity 
in the stratosphere and absorption on the surface temperature. This would occur with the stratosphere being 
injected with aerosols that increase solar reflection and decrease solar transmission. 

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

obj.calculateRadiationBudget()
obj.getTemperatures(HF=True, Params='EBM30') 

#create some lists to store various temps 
l3_temps = [] #surface temp list 
row1_list = []
alpha2_list = []

#calculate steps that we want the for loop to go for
steps = (0.058-0.038)/0.002
 #we want to increase reflectivity from 0.265-0.245 by 0.002
for i in range(int(steps)):
    obj.calculateRadiationBudget()
    print('step ' + str(i), '\n')
    obj.getTemperatures(HF=True, Params='EBM30') 
    print('\n')
    l3_temps.append(obj.T3)
    row1_list.append(obj.row1)
    alpha2_list.append(obj.alpha2)
    obj.row1+=0.002 #increase solar reflectance by 0.002
    obj.tau1-=0.002 #decrease solar transmission by 0.002
    


#dataframe to observe the calculations
df = pd.DataFrame()
df['Surface'] = l3_temps
df['L1 Reflectance'] = row1_list

#set index
df.set_index('L1 Reflectance', inplace=True)

#plot 
fig, ax = plt.subplots()
ax.plot(df, label=df.columns)
ax.set_xlabel('L1 Reflectance')
ax.set_ylabel('Surface Temp - K')
ax.set_title('Stratospheric (L1) Reflectance vs Surface Temperature')
