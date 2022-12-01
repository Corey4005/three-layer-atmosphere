#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 14:32:27 2022

@author: coreywalker
"""

import numpy as np

class model():
    
    def __init__(self):
        
        #greek letter solar variables
        self.tau1 = np.nan #transmission layer 1 (upper atmosphere)
        self.tau2 = np.nan #transmission layer 2 (lower atmosphere)
        self.tau3 = np.nan #transmission layer 3 (surface)
        self.row1 = np.nan #reflection layer 1
        self.row2 = np.nan #reflection layer 2
        self.row3 = np.nan #reflection layer 3
        self.alpha1 = np.nan #absorption layer 1
        self.alpha2 = np.nan #absorption layer 2
        self.alpha3 = np.nan #absorption layer 3
        
        #english letter infrared variables 
        self.t1 = np.nan #transmission layer 1
        self.t2 = np.nan #transmission layer 2
        self.t3 = np.nan #transmission layer 3
        self.r1 = np.nan #reflection layer 1
        self.r2 = np.nan #reflection layer 2
        self.r3 = np.nan #reflection layer 3
        self.a1 = np.nan #absorption layer 1
        self.a2 = np.nan #absorption layer 2
        self.a3 = np.nan #absorption layer 3
        
        #shortwave absorption coeficients 
        self.S1 = np.nan #shortwave absorption Layer 1
        self.S2 = np.nan #shortwave absorption Layer 2
        self.S3 = np.nan #shortwave absorption Surface
        
        #longwave loss coeficients L1 layer 1
        self.L1_A1 = np.nan #A1
        self.L1_A2 = np.nan #A2
        self.L1_A3 = np.nan #A3
        
        #longwave loss coeficients L2 layer 2
        self.L2_A1 = np.nan #A1
        self.L2_A2 = np.nan #A2
        self.L2_A3 = np.nan #A3
        
        #longwave loss coeficients L3 surface
        self.L3_A1 = np.nan #A1
        self.L3_A2 = np.nan #A2
        self.L3_A3 = np.nan #A3
        
        #temperatures calculated in the infrared
        self.T1 = np.nan #temperature emitted Layer 1
        self.T2 = np.nan #temperature emitted Layer 2
        self.T3 = np.nan #temperature emitted Layer 3
        
        #heatflux parameters 3_2
        self.HF3_2 = 0.000
        #hetflux parameters 2_1
        self.HF2_1 = 0.000
        
        #other important variables 
        self.stefanBoltzmann = 5.67E-8 #energy emitted by a black body in wm^-2K^-4
        self.Q = 341 # Average solar flux from the sun over Earth in wm^-2
        
        #EB30 coeficients 
        self.EBa1 = 0.096
        self.EBa2 = 0.740
        self.EBa3 = 0.926
        
        #Kiehl and Trenberth 2 coeficients 
        self.KTa1 = 0.366
        self.KTa2 = 0.762
        self.KTa3 = 0.995
        
        
        
    def setVariables(self, path_to_text_file):
        
        with open(path_to_text_file, 'r') as fp:
            
            #line 1 is columns for dataframe
            textfile_lines = [0,1,2,3,4]
            
            #storage lists for each layer and column
            layer1 = []
            layer2 = []
            surface = []
            
            for i, line in enumerate(fp):
            
                #Read line 1 and get layer 1 values
                if i == textfile_lines[1]:
                    line = line.strip().split('\t')
                    for i in line:
                        if i == '':
                            pass
                        else:
                            layer1.append(i)
                
                #Read line 2 and get layer 2 values
                elif i == textfile_lines[2]:
                    line = line.strip().split('\t')
                    for i in line:
                        if i == '':
                            pass
                        else:
                            layer2.append(i)
                            
                #Read line 3 and get surface values
                elif i == textfile_lines[3]:
                    line = line.strip().split('\t')
                    for i in line:
                        if i == '':
                            surface.append('     ')
                        else:
                            surface.append(i)
                #break at line 4 to stop textfile reading
                elif i == 4:
                    break
        
        #print the filepath and data received from it
        print('Values in {}:'.format(path_to_text_file))
        print('Order:\t\tSol-a', '  ', 'Sol-t',
              '  ', 'Sol-r', '   ', 'IR-a', '   ', 'IR-t', '   ','IR-r')
        print(layer1)
        print(layer2)
        print(surface)
        
        #solar
        #set solar absorpitons at all layers in the class attributes
        self.alpha1 = float(layer1[1])
        self.alpha2 = float(layer2[1])
        self.alpha3 = float(surface[1])
        
        #set solar transmission 
        self.tau1 = float(layer1[2])
        self.tau2 = float(layer2[2])
        
        #set solar reflectance 
        self.row1 = float(layer1[3])
        self.row2 = float(layer2[3])
        self.row3 = float(surface[3])
        
        #IR 
        #set IR absorption at all layers in the class attributes
        self.a1 = float(layer1[4])
        self.a2 = float(layer2[4])
        self.a3 = float(surface[4])
        
        #set IR transmission 
        self.t1 = float(layer1[5])
        self.t2 = float(layer2[5])
        
        
        #set IR reflectance 
        self.r1 = float(layer1[6])
        self.r2 = float(layer2[6])
        self.r3 = float(surface[6])
        
    def calculateRadiationBudget(self):
        
        #creating groups of common variables 
        #solar common equations
        solar_row_group1 = (1-(self.row1*self.row2))
        solar_row_group2 = (1-(self.row2*self.row3))
        solar_tau_group1 = self.tau2*self.row3*self.tau2*self.row1
        solar_tau_group2 = self.tau2*self.row3*self.tau2
        
        #Longwave common equations
        IR_row_group1 = (1-(self.r1*self.r2))
        IR_row_group2 = (1-(self.r2*self.r3))
        IR_tau_group1 = self.t2*self.r3*self.t2*self.r1
        
        #letter substitutions for longwave equations for known solar variables
        B = (self.r2*(IR_row_group1))/((IR_row_group1*IR_row_group2)-IR_tau_group1) #substitution for first known IR term in L1
        C = (self.t2*(IR_row_group1))/((IR_row_group1*IR_row_group2)-IR_tau_group1) #substitutiion for second known IR term in L1
        D = (self.a2/((IR_row_group1*IR_row_group2)-IR_tau_group1)) #substitution for known IR term in L2
        E = (self.t2/((IR_row_group1*IR_row_group2)-IR_tau_group1)) #substitution for first known IR term in L3 
        F = (self.r2/((IR_row_group1*IR_row_group2)-IR_tau_group1)) #substitution for second known IR term in L3
        
        #shortwave equations layer 1 
        S1 = (self.alpha1*(float(self.Q)))*(1+((self.tau1/(((solar_row_group1)*(solar_row_group2))-solar_tau_group1))*((self.row2*(solar_row_group2))+solar_tau_group2)))
        
        #coeficient for L1: A1, A2, A3
        L1_A1 = (2-B*self.a1)+C*self.t2*self.r3/IR_row_group1
        L1_A2 = (-self.a1-self.a1*B*self.r1-(self.a1*B*self.t2*self.r1*self.r3/(IR_row_group2)+C*self.t2*self.r3*self.r1/(IR_row_group1))+(C*self.r3))
        L1_A3 = ((-B*self.t2*self.r1*self.a1)/IR_row_group2)+C
        
        #equations layer 2
        S2 = (((self.Q*self.tau1*self.alpha2)*(solar_row_group2+(self.tau2*self.row3)))/((solar_row_group1*solar_row_group2)-(solar_tau_group1)))
        L2_A1 = ((-D)+(D*self.r2*self.r3)-(D*self.t2*self.r3))
        L2_A2 = (2-(D*self.r1)+(D*self.r1*self.r2*self.r3)-(D*self.r1*self.t2*self.r3)-(D*self.r3)+(D*self.r3*self.r1*self.r2))
        L2_A3 = ((-D)+(D*self.r1*self.r2)-(D*self.t2*self.r1)-(D*self.t2*self.r1))
    
        #equations layer 3
        S3 = (((self.alpha3*(float(self.Q))*self.tau1)/((solar_row_group1*solar_row_group2)-solar_tau_group1))*((self.tau2*solar_row_group2)+(self.row2*self.tau2*self.row3)))
        L3_A1 = ((-E*self.a3)+(E*self.r2*self.r3*self.a3)-(F*self.t2*self.r3*self.a3))
        L3_A2 = ((-self.a3)-(E*self.a3*self.r1)+(E*self.a3*self.r1*self.r2*self.r3)-(F*self.a3*self.r1*self.t2*self.r3)-(F*self.a3*self.r3)+(F*self.a3*self.r3*self.r1*self.r2))
        L3_A3 = (1-(E*self.a3*self.t2*self.r1)-(F*self.a3)+(F*self.a3*self.r1*self.r2))
        
        #set solved shortwave parameters to class attributes
        self.S1 = S1
        self.S2 = S2
        self.S3 = S3
        
        #set layer 1 solved coeficients to class attributes
        self.L1_A1 = L1_A1
        self.L1_A2 = L1_A2
        self.L1_A3 = L1_A3
        
        #set layer 2 solved coeficients to class attributes 
        self.L2_A1 = L2_A1
        self.L2_A2 = L2_A2
        self.L2_A3 = L2_A3
        
        #set layer 3 solved coeficients to class attributes
        self.L3_A1 = L3_A1
        self.L3_A2 = L3_A2 
        self.L3_A3 = L3_A3
        
        #temp storage 
        self.T1 = np.nan
        self.T2 = np.nan
        self.T3 = np.nan
       
        
    def getTemperatures(self, HF=False, Params='EBM30'):
        
        if (HF==False) & (Params=='EBM30'): 
            #create arrays 
            lw = np.array([[self.L1_A1, self.L1_A2, self.L1_A3], [self.L2_A1, self.L2_A2, self.L2_A3], [self.L3_A1, self.L3_A2, self.L3_A3]])
            sw = np.array([self.S1, self.S2, self.S3])
        
           
            #solve for coeficients 
            coef = np.linalg.solve(lw, sw)
        
            #temperatures solved
            T1 = (coef[0]/(self.EBa1*self.stefanBoltzmann))**(0.25)
            T2 = (coef[1]/(self.EBa2*self.stefanBoltzmann))**(0.25)
            T3 = (coef[2]/(self.EBa3*self.stefanBoltzmann))**(0.25)
        
            print('\n')
            print('Total Absorption 1, 2 and sfc: {:.3f} {:.3f} {:.3f}'.format(self.S1, self.S2, self.S3))
            print('\n')
            print('Temp 1, 2, sfc {:.3f} {:.3f} {:.3f}'.format(T1, T2, T3))
            
        elif (HF==True) & (Params=='EBM30'): 
            HF = self.Q * 0.287
            self.HF3_2 = HF
            #create arrays 
            lw = np.array([[self.L1_A1, self.L1_A2, self.L1_A3], [self.L2_A1, self.L2_A2, self.L2_A3], [self.L3_A1, self.L3_A2, self.L3_A3]])
            sw = np.array([self.S1, self.S2+HF, self.S3-HF])
        
        
            #solve for coeficients 
            coef = np.linalg.solve(lw, sw)
            
            
            #temperatures solved
            T1 = (coef[0]/(self.EBa1*self.stefanBoltzmann))**(0.25)
            T2 = (coef[1]/(self.EBa2*self.stefanBoltzmann))**(0.25)
            T3 = (coef[2]/(self.EBa3*self.stefanBoltzmann))**(0.25)
            
            self.T1 = T1
            self.T2 = T2
            self.T3 = T3
            
            L1sum = self.L1_A1*coef[0]+self.L1_A2*coef[1]+self.L1_A3*coef[2]
            L2sum = self.L2_A1*coef[0]+self.L2_A2*coef[1]+self.L2_A3*coef[2]
            L3sum = self.L3_A1*coef[0]+self.L3_A2*coef[1]+self.L3_A3*coef[2]
            
            print('\n')
            print('Total Absorption 1, 2 and sfc: {:.3f} {:.3f} {:.3f}'.format(L1sum, L2sum, L3sum))
            
            print('\n')
            print('Temp 1, 2, sfc {:.3f} {:.3f} {:.3f}'.format(T1, T2, T3))
            
        elif (HF==True) & (Params=='K&T'):
            HF = self.Q * 0.287
            self.HF3_2 = HF
            #create arrays 
            lw = np.array([[self.L1_A1, self.L1_A2, self.L1_A3], [self.L2_A1, self.L2_A2, self.L2_A3], [self.L3_A1, self.L3_A2, self.L3_A3]])
            sw = np.array([self.S1, self.S2+HF, self.S3-HF])
        
           
            #solve for coeficients 
            coef = np.linalg.solve(lw, sw)
            
            
            #temperatures solved
            T1 = (coef[0]/(self.KTa1*self.stefanBoltzmann))**(0.25)
            T2 = (coef[1]/(self.KTa2*self.stefanBoltzmann))**(0.25)
            T3 = (coef[2]/(self.KTa3*self.stefanBoltzmann))**(0.25)
            
            L1sum = self.L1_A1*coef[0]+self.L1_A2*coef[1]+self.L1_A3*coef[2]
            L2sum = self.L2_A1*coef[0]+self.L2_A2*coef[1]+self.L2_A3*coef[2]
            L3sum = self.L3_A1*coef[0]+self.L3_A2*coef[1]+self.L3_A3*coef[2]
            
            print('\n')
            print('Total Absorption 1, 2 and sfc: {:.3f} {:.3f} {:.3f}'.format(L1sum, L2sum, L3sum))
            
            print('\n')
            print('Temp 1, 2, sfc {:.3f} {:.3f} {:.3f}'.format(T1, T2, T3))
            
    
        