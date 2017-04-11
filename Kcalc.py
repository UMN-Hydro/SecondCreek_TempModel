
import numpy as np
import pandas as pd



#Script to take average q output from 1DTempProbePro and a deltaH time series to calculate average K. Additionally
#it scales the delta H data to 0.3 meters, (the distance between the top and bottom temperature probes) for future use with 1DTempPro.
#Script is useful for double checking the 1DTemp results. 
#Variable names ending in 1 indicate that they are from the begining of the summer, May-August 1
#Variables names ending in 2 indicate that they are the end of summer, aug 1 - october
    

q1= -0.040889 #modeled average flux from 1dtempro
q2= -.045143 #modeled average flux from 1dtempro


#read in head difference timeseries

dh1 =pd.read_csv('HeadDiff1_1DTempPro.csv', sep= ',', header = None ) #first half of summer
dh2= pd.read_csv('HeadDiff2_1DTempPro.csv', sep= ',', header = None ) #second half of summer

#rename colums for ease of use

dh1.rename(columns={0: 'date', 1: 'deltah'}, inplace = True)
dh2.rename(columns={0: 'date', 1: 'deltah'}, inplace = True)

#convert dates to datetime objects, set datess as dataframe index



dh1['date']= pd.to_datetime(dh1['date'], format= '%m/%d/%Y %H:%M')
dh1 = dh1.set_index(['date'])

dh2['date']= pd.to_datetime(dh2['date'], format= '%m/%d/%Y %H:%M')
dh2 = dh2.set_index(['date'])



#calculate k/ds from q = dh* k/ ds 
# then convert k/ds to k that will be used by 1d temp pro

#Darcy's law to calculade k/ds
k1overds= -dh1['deltah'].mean() / q1
k2overds= -dh2['deltah'].mean() / q2

ds1 = 429.558 - 429.092 #distance from sg1 to PZCC (vertical distance between measurment devices, surveyed)
ds2 = 429.558 - 428.818 #distance from sg2 to PZCC

#calculate hydraulic conductivity
k1= k1overds *ds1
k2= k2overds *ds2

print 'k1 = %f' % (k1)
print 'k2 = %f' %(k2)

#scale dh to .3 meters for 1dtemppro. Also make it negative to indicate higher head in the stream bed
dh1['deltah'] = dh1['deltah'] * -.3/ds1
dh2['deltah'] = dh2['deltah'] * -.3/ds2 

#Save head data as a csv suitable for 1dtempProbePro. This requires reloading the
#csv as a numpy array so that the delimiter can be ', '. Pandas doesn't support multi
#character delimiters.
dh1.to_csv('scaleddh1.csv',sep =',',date_format='%m/%d/%Y %H:%M', header = False)
dh2.to_csv('scaleddh2.csv',sep =',',date_format='%m/%d/%Y %H:%M', header = False)
dh1temp = np.loadtxt('scaleddh1.csv', dtype =str , delimiter = ',')
dh2temp = np.loadtxt('scaleddh2.csv', dtype =str, delimiter = ',')
np.savetxt('scaleddh1.csv',dh1temp,fmt= '%s', delimiter = ', ')
np.savetxt('scaleddh2.csv',dh2temp,fmt = '%s', delimiter = ', ')
#








