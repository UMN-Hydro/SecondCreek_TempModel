# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 20:08:16 2017

@author: Jack
"""
import scipy.io
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

    
##match up dates in q and dh time series
#dh.rename(columns={0: 'date', 1: 'deltah'}, inplace = True)
#tempData.rename(columns={0: 'date',1:'0m',2:'0.5m',3:'0.1m',4:'0.15m',5:'0.2m',6:'0.3m'}, inplace = True)

#    
#dh.['date']= pd.to_datetime(dh['date'], format= '%m/%d/%Y %H:%M')
#dh = dh.set_index(['date'])

    
#fig = plt.figure(dh[:,0],dh[:,1])
#fig = plt.figure(figsize=(8,12))
#dhSeries = fig.add_subplot(1,1,1)
#dhSeries.plot(dh.date, dh.deltah)
##calculate k/ds
#convert k/ds to k that will be used by 1d temp pro

PZO = scipy.io.loadmat('PZ-Out_161005_Calib20161001_1545_results.mat') #load matlab data
DivTotHead=  PZO['DivTotHead'].reshape(PZO['DivTotHead'].size)  #make array 1 dimensional


#import PZ data
PZO = pd.DataFrame({'DivDateTime':PZO[ 'DivDateTime' ] , 'DivTotHead':DivTotHead})#Turn matlab data into pd dataframe
PZO['DivTotHead'] = PZO['DivTotHead'].apply(lambda x:x/100) #convert cm to m

    
PZO['DivDateTime']= pd.to_datetime(PZO['DivDateTime'], format='%Y/%m/%d %H:%M:%S')
PZO = PZO.set_index(['DivDateTime'])

PZO = PZO.resample('1d').sum()  #bin the PZ data by day
PZO['DivTotHead'] = PZO['DivTotHead'].apply(lambda x:x/(24*4)) #make each bin an average of the head measurment for that day 


#import rain data
RainGauge = pd.read_csv('Weather_EmbarrassMN_151017_161005.csv', sep= ',' )
RainGauge['Date']= pd.to_datetime(RainGauge['Date'], format='%m/%d/%Y')
RainGauge = RainGauge.set_index(['Date'])



#throw out m and t dats
RainGauge = RainGauge[RainGauge.PRCP !='M' ]
RainGauge = RainGauge[RainGauge.PRCP !='T' ]

#put 2 data frames together
RPZ = pd.concat([PZO, RainGauge], axis =1)
#Throw out all Nan, including places where there issn't PZ data
RPZ = RPZ[pd.notnull(RPZ['PRCP'])]
RPZ = RPZ[pd.notnull(RPZ['DivTotHead'])]
#Throw out first and last day where there is not a full 24 hr record
RPZ = RPZ.drop([RPZ.first_valid_index()])
RPZ = RPZ.drop([RPZ.last_valid_index()])
          
          
#plot PZ head as fxn of rainfall

plt.xlabel('Rainfall, UNIT ')
plt.ylabel('Head, m')
plt.title('Testplot')
plt.plot(RPZ.PRCP, RPZ.DivTotHead, 'ro')

##rain and pz-o correlation


#figure out how to do y axis as one day later

