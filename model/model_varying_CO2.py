#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 13:54:53 2022

This is a module to simulate changing CO2 and its effect on the surface temperature

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
obj.r2 = 0.190 #reseting r2 to another number
obj.a2 = 0.765 #reseting a2 to higher absorption for CO2 environment
l1_temps = []
l2_temps = []
l3_temps = []
r2_list = []
for i in range(26):
    obj.r2 = obj.r2+0.002
    r2_list.append(obj.r2)
    obj.a2 = obj.a2-0.002
    obj.calculateRadiationBudget()
    #solve the set of linear equations and print temps
    obj.getTemperatures(HF=True, Params='EBM30') #print temperature parameters
    l1_temps.append(obj.T1)
    l2_temps.append(obj.T2)
    l3_temps.append(obj.T3)

df = pd.DataFrame()
df['r2'] = r2_list
df['Upper Atmpsphere']=l1_temps
df['Lower Atmosphere']=l2_temps
df['Surface']=l3_temps

fig, ax = plt.subplots()
df.set_index('r2', inplace=True)
ax.plot(df, label=df.columns)
ax.set_xlabel('r2')
ax.set_ylabel('Temp - K')
ax.set_title('Varied r2 vs Layer Temperature')
ax.legend()