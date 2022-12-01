#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 15:07:18 2022

This module demonstrates how the model can be iterated upon to simulate 
temperature changes in the upper atmosphere with increasing cirrus cloud 
cover. 

@author: coreywalker
"""
from modelEquations import model
import pandas as pd
import matplotlib.pyplot as plt

#textfile location 
model_params = './EBM30.txt'

#instantiate model class object
obj = model()

#get values from textfile and set them to class attributes
obj.setVariables(model_params)
obj.r1 = 0.004 
l1_temps = []
l2_temps = []
l3_temps = []
r1_list = []
for i in range(26):
    obj.r1 = obj.r1+0.002
    r1_list.append(obj.r1)
    obj.a1 = 1 - (obj.t1+obj.r1)
    print(obj.r1, obj.a1, obj.t1)
    obj.calculateRadiationBudget()
    #solve the set of linear equations and print temps
    obj.getTemperatures(HF=True, Params='EBM30') #print temperature parameters
    l1_temps.append(obj.T1)
    l2_temps.append(obj.T2)
    l3_temps.append(obj.T3)

df = pd.DataFrame()
df['r1'] = r1_list
df['Upper Atmpsphere']=l1_temps
df['Lower Atmosphere']=l2_temps
df['Surface']=l3_temps

fig, ax = plt.subplots()
df.set_index('r1', inplace=True)
ax.plot(df, label=df.columns)
ax.set_xlabel('r1')
ax.set_ylabel('Temp - K')
ax.set_title('Varied r1 vs Layer Temperature')
ax.legend()