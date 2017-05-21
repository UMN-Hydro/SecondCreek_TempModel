# -*- coding: utf-8 -*-
"""
Created on Sat May 06 21:15:54 2017

@author: Jack
"""

#Jack Lange
#5/6/17
#Use K generated from 1dtempProbe and delta h time series to plot q as fn of time

import numpy as np
import pandas as pd
dh1 =pd.read_csv('HeadDiff1_PZCWSG.csv', sep= ',', header = None )
dh1[1] = -1*dh1[1]
dh2 =pd.read_csv('HeadDiff2_PZCWSG.csv', sep= ',', header = None )
dh2[1] = -1*dh2[1]

dh1[0]= pd.to_datetime(dh1[0], format= '%m/%d/%Y %H:%M')
dh1 = dh1.set_index([0])

dh2[0]= pd.to_datetime(dh2[0], format= '%m/%d/%Y %H:%M')
dh2 = dh2.set_index([0])
dh1.to_csv('scaleddh1.csv',sep =',',date_format='%m/%d/%Y %H:%M', header = False)
dh2.to_csv('scaleddh2.csv',sep =',',date_format='%m/%d/%Y %H:%M', header = False)
dh1temp = np.loadtxt('scaleddh1.csv', dtype =str , delimiter = ',')
dh2temp = np.loadtxt('scaleddh2.csv', dtype =str, delimiter = ',')
np.savetxt('HeadDiff1CW.csv',dh1temp,fmt= '%s', delimiter = ', ')
np.savetxt('HeadDiff2CW.csv',dh2temp,fmt = '%s', delimiter = ', ')