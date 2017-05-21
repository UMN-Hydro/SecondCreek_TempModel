# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 10:08:20 2017

@author: Jack
"""

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
TPrun = 2
#read in model output, data
data =pd.read_csv('Temp_data\Archive\VS2DH_Archive_%d\MeasuredData.csv' % TPrun, sep= ',', header = None ) #import csv data
data[0] = pd.to_datetime(data[0], format='%m/%d/%Y %H:%M') #turn dates into datetime objects, use dates as the index
data = data.set_index(data[0])
data.rename(columns={ 1: '1data', 2:'2data', 3:'3data', 4:'4data', 5:'5data',6:'6data'}, inplace = True) #rename columns for convineince
data.apply(pd.to_numeric, errors='ignore') #turn strings into floats
 #delete first row with depth of thermistors
data = data.drop(data.index[0])



model =pd.read_csv('Archive\VS2DH_Archive_%d\ModeledData.csv' % TPrun, sep= ',', header = None ) #import csv data
model[0] = pd.to_datetime(model[0], format='%m/%d/%Y %H:%M:%S') #convert dates to datetime object, set as index
model = model.set_index(model[0])
model = model.drop(model.index[0])
 #delete first row containing the depth of each thermistor
model.rename(columns={ 1: '1model', 2:'2model', 3:'3model', 4:'4model', 5:'5model',6:'6model'}, inplace = True) #rename columns for convinience
model.apply(pd.to_numeric,errors='ignore') #turn strings into floats

#prune modeled points that we don't have data to compare 
combo =  pd.concat([data, model], axis =1)
combo = combo[pd.notnull(combo['1data'])]


#make a dataframe to record all errors 100* (model-data)/data 
error = pd.DataFrame(index = combo.index)
fig = plt.figure()

for i in range (1,7):
    error['%derror' % i] =100* (combo['%dmodel' % i] - combo['%ddata' % i])/combo['%ddata' % i]
    graph = fig.add_subplot(1,6,i)
    graph.plot(error.index,error['%derror' % i], 'ro')
#plot each error in a different color


    
# 
plt.show()
