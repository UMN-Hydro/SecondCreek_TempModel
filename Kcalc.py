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
import statsmodels.api as sm
# Script to read average q output from 1DTempProbePro, and use deltaH time series to calculate average K
#read in deltah timeseries
dh = pd.read_csv('HeadDiff_Summer16_1DTempPro.csv', sep= ',', header = None )
dh1 =pd.read_csv('HeadDiff1_1DTempPro.csv', sep= ',', header = None )
dh2= pd.read_csv('HeadDiff2_1DTempPro.csv', sep= ',', header = None )

#user inputs values from 1DtempProbe
probe = raw_input("enter the name of the temperature probe to be investigated\n")
if probe == "a":
    tempData = pd.read_csv('TPA_CalibData_1DTempPro.csv', sep= ',', header = None )
    q= float(raw_input("enter average q\n"))
elif probe == "b":
    
    tempData = pd.read_csv('TPB_CalibData_1DTempPro.csv', sep= ',', header = None )
    q= float(raw_input("enter average q\n"))

elif probe == "c":
    tempData = pd.read_csv('TPC_CalibData_1DTempPro.csv', sep= ',', header = None )
    q= float(raw_input("enter average q\n"))

q= -0.17692
tempData.rename(columns={0: 'date',1:'0m',2:'0.5m',3:'0.1m',4:'0.15m',5:'0.2m',6:'0.3m'}, inplace = True)

#match up dates in q and dh time series
dh.rename(columns={0: 'date', 1: 'deltah'}, inplace = True)
dh1.rename(columns={0: 'date', 1: 'deltah'}, inplace = True)
dh2.rename(columns={0: 'date', 1: 'deltah'}, inplace = True)

    
dh['date']= pd.to_datetime(dh['date'], format= '%m/%d/%Y %H:%M')
dh = dh.set_index(['date'])

dh1['date']= pd.to_datetime(dh1['date'], format= '%m/%d/%Y %H:%M')
dh1 = dh1.set_index(['date'])

dh2['date']= pd.to_datetime(dh2['date'], format= '%m/%d/%Y %H:%M')
dh2 = dh2.set_index(['date'])
    
#plot entire dh timeseries
#fig = plt.figure(figsize=(8,12))
#dhSeries = fig.add_subplot(1,1,1)
#dhSeries.plot(dh.deltah)
#plt.ylim(0,.2)
##calculate k/ds from q = dh* k/ ds 
#convert k/ds to k that will be used by 1d temp pro

k1overds= -dh1['deltah'].mean() / q
k2overds= -dh2['deltah'].mean() / q

ds1 = 429.558 - 429.092#distance from sg1 to PZCC
ds2 = 429.558 - 428.818#distance from sg2 to PZCC
print k1overds *ds1
print k2overds *ds2

#scale dh to .3 meters 
dh1['deltah'] = dh1['deltah'] * .3/ds1
dh2['deltah'] = dh2['deltah'] * .3/ds2 

dh1.to_csv('scaleddh1.csv',date_format='%m/%d/%Y %H:%M', header = False)
dh2.to_csv('scaleddh2.csv',date_format='%m/%d/%Y %H:%M', header = False)

#
#Below: plots head vs rain at various time delays
#
#PZO = scipy.io.loadmat('PZ-Out_161005_Calib20161001_1545_results.mat') #load matlab data
#DivTotHead=  PZO['DivTotHead'].reshape(PZO['DivTotHead'].size)  #make array 1 dimensional
#
#
##import PZ data  
#PZO = pd.DataFrame({'DivDateTime':PZO[ 'DivDateTime' ] , 'DivTotHead':DivTotHead})#Turn matlab data into pd dataframe
#PZO['DivTotHead'] = PZO['DivTotHead'].apply(lambda x:x/100) #convert cm to m
#
#    
#PZO['DivDateTime']= pd.to_datetime(PZO['DivDateTime'], format='%Y/%m/%d %H:%M:%S')
#PZO = PZO.set_index(['DivDateTime'])
#
#PZO = PZO.resample('1d').sum()  #bin the PZ data by day
#PZO['DivTotHead'] = PZO['DivTotHead'].apply(lambda x:x/(24*4)) #make each bin an average of the head measurment for that day 
#
#
##import rain data
#RainGauge = pd.read_csv('Weather_EmbarrassMN_151017_161005.csv', sep= ',' )
#RainGauge['Date']= pd.to_datetime(RainGauge['Date'], format='%m/%d/%Y')
#RainGauge = RainGauge.set_index(['Date'])
#
#
#
##throw out m and t dats
#RainGauge = RainGauge[RainGauge.PRCP !='M' ]
#RainGauge = RainGauge[RainGauge.PRCP !='T' ]
##turn strings into floats
#RainGauge['PRCP'] =pd.to_numeric(RainGauge['PRCP'])
#PZO['DivTotHead']= pd.to_numeric(PZO['DivTotHead'])
#
#
#
#
#
#
#
##
#for i in range(0,15):
#    
#
#    PZO.index = PZO.index +pd.DateOffset(days = 1)  #Incriment the begining date by one day
#
#    RPZ = RPZ = pd.concat([PZO, RainGauge], axis =1) #put raing gauge and PZ data together
# 
#    RPZ = RPZ[pd.notnull(RPZ['PRCP'])] #remove all Nan
#    RPZ = RPZ[pd.notnull(RPZ['DivTotHead'])] #remove all Nan
#    RPZ = RPZ.drop([RPZ.first_valid_index()]) #Remove first (incomplete) day
#    RPZ = RPZ.drop([RPZ.last_valid_index()]) #remove last (incomplete) day
#    RPZ = RPZ[RPZ.PRCP >= 0] #remove days without rainfall
#    fig = plt.figure(i)
#    graph = fig.add_subplot(1,1,1)
#    graph.plot(RPZ.PRCP, RPZ.DivTotHead, 'ro')
#  
#    plt.xlabel('Rainfall, Inches')
#    plt.ylabel('Head, m')
#    plt.title('day incriment = %d' % i)
##    plt.plot(RPZ.PRCP, RPZ.DivTotHead, 'ro')
#
#    X = RPZ['PRCP']
#
#    X = sm.add_constant(X)
#
#    fit = sm.OLS(RPZ['DivTotHead'],X).fit()
#
#    graph.plot(RPZ['PRCP'],( RPZ['PRCP']*fit.params.values[1]) + fit.params.values[0], 'k-', linewidth = 2)
# 
#to do:

#finish K calculation
#figure out how to pop out plots and make em look nicer/organize