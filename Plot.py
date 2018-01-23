# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 14:33:17 2017

@author: aspit
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import os

def converttimestamp(stamp):
	return dt.datetime.fromtimestamp(int(stamp)).strftime('%Y-%m-%d %H:%M:%S')

##these might need to be combined

def utc_to_local(utc_dt):
    #sets the timezone of a timestamp object to local time
    return utc_dt.replace(tzinfo=dt.timezone.utc).astimezone(tz=None)

    
def read_from_csv(window = None, endtime = None):
#    if rawtext_csvfile == None:
#        folder = os.path.dirname(os.path.abspath("__file__"))
#        rawtext_csvfile = folder + "\\rawtext.csv"

    rawtext_read = pd.read_csv('Data/monitorlog.csv', encoding = "ISO-8859-1")
    
    time = rawtext_read['Time']
    BTC = rawtext_read['BTC_total_value']
    Fiat = rawtext_read['Fiat_total_value']

    if endtime == None:
        endtime = time.iloc[-1]
    if window == None:
        window = 24*60*60
    starttime = endtime - window

    diff_start = abs(time - starttime)
    index_start = diff_start.idxmin()
    diff_end = abs(time - endtime)
    index_end = diff_end.idxmin()

    starttimestr = str(utc_to_local(dt.datetime.fromtimestamp(starttime)))
    endtimestr = str(utc_to_local(dt.datetime.fromtimestamp(endtime)))

    print("Reading file from " + starttimestr + " to " + endtimestr)
    print("contains " + str(index_end - index_start) + " comments")

    time = time[index_start:index_end]
    BTC = BTC[index_start:index_end]
    Fiat = Fiat[index_start:index_end]

    return time, BTC, Fiat

def convert_unixarray_timesamparray(intarray_unix):
    datetimearray=[]
    for unix in intarray_unix:
        datetimearray.append(dt.datetime.fromtimestamp(unix))
        
    return datetimearray

	
window = 30*24*60*60

time, BTC, Fiat = read_from_csv(window)

time = convert_unixarray_timesamparray(time)

#timeconvert = time.apply(converttimestamp)
figsize = plt.figaspect(1/2)
fig, axs = plt.subplots(1,2,figsize=figsize) 


#ax1 = plt.subplot(121)
axs[0].set_title('BTC')
axs[0].plot(time,BTC)


#ax2 = plt.subplot(122)
axs[1].set_title('Fiat')
axs[1].plot(time,Fiat)


plt.tight_layout()
fig.autofmt_xdate()
plt.show()

  

    
