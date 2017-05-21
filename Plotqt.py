# -*- coding: utf-8 -*-
"""
Created on Sun May 07 22:56:42 2017

@author: Jack
"""
import pandas as pd
import numpy as np
import datetime


from matplotlib import pyplot as plt

qTPA1=pd.read_csv('Temp_data\Archive\VS2DH_Archive_15\CalculatedSpecificDischarge.csv', sep= ',', header = None )
qTPA2=pd.read_csv('Temp_data\Archive\VS2DH_Archive_14\CalculatedSpecificDischarge.csv', sep= ',', header = None )
qTPB1= pd.read_csv('Temp_data\Archive\VS2DH_Archive_16\CalculatedSpecificDischarge.csv', sep= ',', header = None )
qTPC1=pd.read_csv('Temp_data\Archive\VS2DH_Archive_17\CalculatedSpecificDischarge.csv', sep= ',', header = None )


print 'TPA1 q=',np.average(qTPA1[1] ), 'm/s'
print 'TPA2 q=',np.average(qTPA2[1] ),  'm/s'
print 'TPB q=',np.average(qTPB1[1] ), 'm/s'
print 'TPC q=',np.average(qTPC1[1] ), 'm/s'

#get q from darcy

KA1=0.0088
KA2=0.034
KB1=0.079
KC1=0.05

dhA1 =pd.read_csv('Head_diferences,no_scaling\Proper_signs\HeadDiff1_PZCWSG.csv', sep= ',', header = None ) #first half of summer
dhA2 =pd.read_csv('Head_diferences,no_scaling\Proper_signs\HeadDiff2CW.csv', sep= ',', header = None ) #first half of summer
dhB1 =pd.read_csv('Head_diferences,no_scaling\Proper_signs\HeadDiff1CC.csv', sep= ',', header = None ) #first half of summer
dhC1 =pd.read_csv('Head_diferences,no_scaling\Proper_signs\HeadDiff1in.csv', sep= ',', header = None ) #first half of summer


dhA1[0]= pd.to_datetime(dhA1[0], format = '%m/%d/%Y %H:%M')
dhA2[0]= pd.to_datetime(dhA2[0], format = '%m/%d/%Y %H:%M')
dhB1[0]= pd.to_datetime(dhB1[0], format = '%m/%d/%Y %H:%M')
dhC1[0]= pd.to_datetime(dhC1[0], format = '%m/%d/%Y %H:%M')


ds= 0.3

qdA1 = KA1*dhA1[1]/ds
qdA2= KA2*dhA2[1]/ds
qdB1= KB1*dhB1[1]/ds
qdC1= KC1*dhC1[1]/ds

#qdA1 =qdA1.set_index( pd.to_datetime(dhA1[0], format = '%m/%d/%Y %H:%M'))


print 'dA1 q=',np.average(qdA1[1] ), 'm/d'
print 'dA2 q=',np.average(qdA2[1] ), 'm/d'
print 'dB q=',np.average(qdB1[1] ), 'm/d'
print 'dC q=',np.average(qdC1[1] ), 'm/d'

#
#fig = plt.figure()
#graph = fig.add_subplot(1,2,1)
#graph.plot( dhA1[0],qdA1)
#plt.xlabel('Date')
#plt.ylabel('q, m/d')
#plt.title('TPA1')
#graph = fig.add_subplot(1,2,2)
#graph.plot( dhA2[0],qdA2)


##import rain data, set dates as the index
RainGauge = pd.read_csv('Weather_EmbarrassMN_151017_161005.csv', sep= ',' )
RainGauge['Date']= pd.to_datetime(RainGauge['Date'], format='%m/%d/%Y')
RainGauge = RainGauge.set_index(['Date'])
#
#
#
##throw out non numeric rain data such as days of trace rainfall
RainGauge = RainGauge[RainGauge.PRCP !='M' ]
RainGauge = RainGauge[RainGauge.PRCP !='T' ]


#turn string data into float
RainGauge['PRCP'] =pd.to_numeric(RainGauge['PRCP'])

##plot TPA
fig = plt.figure()
ax2 = fig.add_subplot(2,1,2)
ax2.plot(RainGauge['PRCP'])
plt.xlabel('Date')
plt.ylabel('Rainfall, inches')
plt.title('Rainfall')




ax1 = fig.add_subplot(2,1,1,sharex=ax2)

ax1.plot(dhA1[0],qdA1)
plt.xlabel('Date')
plt.ylabel('q, m/d')
plt.title('TPA')
ax1.set_xlim([datetime.date(2016, 6,4), datetime.date(2016, 7, 25)])


#graph.set_xlim([datetime.date(2016, 6,4), datetime.date(2016, 7, 25)])
plt.show()




#plot B
fig = plt.figure()

ax2 = fig.add_subplot(2,1,2)
ax2.plot(RainGauge['PRCP'])
plt.xlabel('Date')
plt.ylabel('Rainfall, inches')
plt.title('Rainfall')




ax1 = fig.add_subplot(2,1,1,sharex=ax2)

ax1.plot(dhB1[0],qdB1)
plt.xlabel('Date')
plt.ylabel('q, m/d')
plt.title('TPB')
ax1.set_xlim([datetime.date(2016, 6,4), datetime.date(2016, 7, 25)])

plt.show()

#plotC
fig = plt.figure()

ax2 = fig.add_subplot(2,1,2)
ax2.plot(RainGauge['PRCP'])
plt.xlabel('Date')
plt.ylabel('Rainfall, inches')
plt.title('Rainfall')




ax1 = fig.add_subplot(2,1,1,sharex=ax2)

ax1.plot(dhC1[0],qdC1)
plt.xlabel('Date')
plt.ylabel('q, m/d')
plt.title('TPC')
ax1.set_xlim([datetime.date(2016, 6,4), datetime.date(2016, 7, 25)])
plt.show()


#all three q and rain

fig = plt.figure()

ax2 = fig.add_subplot(4,1,4)
ax2.plot(RainGauge['PRCP'])
plt.xlabel('Date')
plt.ylabel('Rainfall, inches')
plt.title('Rainfall')

ax1 = fig.add_subplot(4,1,1,sharex=ax2)

ax1.plot(dhC1[0],qdC1)

plt.ylabel('q, m/d')
plt.title('TPC')
ax1.set_xlim([datetime.date(2016, 6,4), datetime.date(2016, 7, 25)])


ax3 = fig.add_subplot(4,1,2,sharex=ax2)

ax3.plot(dhA1[0],qdA1)

plt.ylabel('q, m/d')
plt.title('TPA')
ax3.set_xlim([datetime.date(2016, 6,4), datetime.date(2016, 7, 25)])

ax4 = fig.add_subplot(4,1,3,sharex=ax2)

ax4.plot(dhB1[0],qdB1)

plt.ylabel('q, m/d')
plt.title('TPB')
ax4.set_xlim([datetime.date(2016, 6,4), datetime.date(2016, 7, 25)])

plt.show()
