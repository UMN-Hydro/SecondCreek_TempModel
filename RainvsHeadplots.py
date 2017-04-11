#This work was done in hopes of visualizing groundwater recharge following rain events using data from Second Creek.
#Running the script will create 5 plots of Head vs Rainfall. In each plot the lendth of time between rainfall event and head measurment is increased
# by one day. In this way, delayed recharge could potentially be  observed.
#Unfortunatley there does not seem to be any positive correlation between head and rainfall at any number of offset days.
#Another possible line of analysis could be binning head and rainfall data weekly and looking for a correlation in  similar fashion.
#This script could also be used to measure correlation between stream gauge measurements and rainfall data.


import scipy.io
import pandas as pd
from matplotlib import pyplot as plt
import statsmodels.api as sm 

#Below: plots head vs rain at various time delays
#
PZO = scipy.io.loadmat('PZ-Out_161005_Calib20161001_1545_results.mat') #load head data from matlab file 
DivTotHead=  PZO['DivTotHead'].reshape(PZO['DivTotHead'].size)  #make array 1 dimensional

#
PZO = pd.DataFrame({'DivDateTime':PZO[ 'DivDateTime' ] , 'DivTotHead':DivTotHead})#Turn matlab data into pd dataframe
PZO['DivTotHead'] = PZO['DivTotHead'].apply(lambda x:x/100) #convert cm to m
#
# Index the dataframe by date
PZO['DivDateTime']= pd.to_datetime(PZO['DivDateTime'], format='%Y/%m/%d %H:%M:%S')
PZO = PZO.set_index(['DivDateTime'])
#

#BINNING

PZO['DivTotHead']= pd.to_numeric(PZO['DivTotHead'])

PZO = PZO.resample('1d').sum()  #sum the PZ head data by day 
PZO['DivTotHead'] = PZO['DivTotHead'].apply(lambda x:x/(7*24*4)) #divide the value in each bin by 24*4 because that's how many datapoints are taken by the PZ each day (one every 15 minutes)
#
#
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
PZO['DivTotHead']= pd.to_numeric(PZO['DivTotHead'])





#
#create maxOffset number of plots. Plots are head vs rainfall. When i = 0 head data and rain data are taken from the same day. When i = 1 head data is taken from the 
#day after the rain event. When I = 2 head data is taken from 2 days after the rain event. Days of zero rainfall are not plotted. 
#a linear trend line is fit on each plot. 

maxOffset=5
for i in range(0,maxOffset):
#    
#
    PZO.index = PZO.index +pd.DateOffset(days = 1)  #Incriment the begining date by one day

    RPZ = RPZ = pd.concat([PZO, RainGauge], axis =1) #put raing gauge and PZ data together
# 
    RPZ = RPZ[pd.notnull(RPZ['PRCP'])] #remove all Nan
    RPZ = RPZ[pd.notnull(RPZ['DivTotHead'])] #remove all Nan
    RPZ = RPZ.drop([RPZ.first_valid_index()]) #Remove first (incomplete) day
    RPZ = RPZ.drop([RPZ.last_valid_index()]) #remove last (incomplete) day
    RPZ = RPZ[RPZ.PRCP > 0] #remove days without rainfall
    fig = plt.figure(i)
    graph = fig.add_subplot(1,1,1)
    graph.plot(RPZ.PRCP, RPZ.DivTotHead, 'ro')
#  
    plt.xlabel('Rainfall, Inches')
    plt.ylabel('Head, m')
    plt.title('day incriment = %d' % i)
    
    #Fit, plot trendline
    X = RPZ['PRCP']
    X = sm.add_constant(X)
    fit = sm.OLS(RPZ['DivTotHead'],X).fit()
    graph.plot(RPZ['PRCP'],( RPZ['PRCP']*fit.params.values[1]) + fit.params.values[0], 'k-', linewidth = 2)
# 