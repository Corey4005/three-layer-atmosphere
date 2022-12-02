#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 14:31:59 2022

This is a module to show how a text file containing solar and infrared values
can be read in and processed to model temperatures across three atmospheric
layers. 

@author: coreywalker
"""

from modelEquations import model

#textfile location containing EBM30 values 
model_params = './EBM30.txt'

#instantiate model class object
obj = model()

#get values from textfile and set them to class attributes
obj.setVariables(model_params)

#solve matrix equations
obj.calculateRadiationBudget()

#solve the set of linear equations and print temps
obj.getTemperatures(HF=True, Params='EBM30') #print temperature parameters
