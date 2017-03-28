# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 20:08:16 2017

@author: Jack
"""
import numpy as np
import pandas as pd
from datetime import datetime 
from matplotlib import pyplot as plt
# Script to read average q output from 1DTempProbePro, and use deltaH time series to calculate average K
#read in deltah timeseries
dh = pd.read_csv('HeadDiff_Summer16_1DTempPro.csv', sep= ',', header = None )


#user inputs values from 1DtempProbe
#probe = raw_input("enter the name of the temperature probe to be investigated\n")
#if probe == "a":
#    tempData = pd.read_csv('TPA_CalibData_1DTempPro.csv', sep= ',', header = None )
#    q= float(raw_input("enter average q\n"))
#elif probe == "b":
#    
#    tempData = pd.read_csv('TPB_CalibData_1DTempPro.csv', sep= ',', header = None )
#    q= float(raw_input("enter average q\n"))
#
#elif probe == "c":
#    tempData = pd.read_csv('TPC_CalibData_1DTempPro.csv', sep= ',', header = None )
#    q= float(raw_input("enter average q\n"))

    
#match up dates in q and dh time series
dh.rename(columns={0: 'date', 1: 'deltah'}, inplace = True)
tempData.rename(columns={0: 'date',1:'0m',2:'0.5m',3:'0.1m',4:'0.15m',5:'0.2m',6:'0.3m'}, inplace = True)
for row in range(0, dh.shape[0]):
    
    dh.iloc[row, 0]= datetime.strptime(dh.iloc[row,0], '%m/%d/%Y %H:%M')


    
#fig = plt.figure(dh[:,0],dh[:,1])
plt.plot(dh.date, dh.deltah)
#calculate k/ds
#convert k/ds to k that will be used by 1d temp pro
