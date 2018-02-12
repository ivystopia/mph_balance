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
import sys


def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts



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
    print("contains " + str(index_end - index_start) + " data points")
    
    #rawtext_read.set_index(rawtext_read['Time'])
    #print(str(rawtext_read.index[0]))
    rawtext_read = rawtext_read.truncate(before = index_start, after = index_end)
    
    #rawtext_read = rawtext
    
#    
#    BTC = rawtext_read['BTC_total_value']
#    Fiat = rawtext_read['Fiat_total_value']
#    
#
#
#    time = time[index_start:index_end]
#    BTC = BTC[index_start:index_end]
#    Fiat = Fiat[index_start:index_end]

    return rawtext_read

def convert_unixarray_timesamparray(intarray_unix):
    datetimearray=[]
    for unix in intarray_unix:
        datetimearray.append(dt.datetime.fromtimestamp(unix))
        
    return datetimearray

	
if __name__ == '__main__':
    from sys import argv
    myargs = getopts(argv)
    if '-w' in myargs:  # Example usage. 
        days = int(myargs['-w'])#
    else:
        days = 30

    window = days*24*60*60
    
    data = read_from_csv(window)
    
    
    datetimedata = pd.to_datetime(data['Time'], unit = 's')
    datetimedata = datetimedata.dt.strftime('%Y-%m-%d')
    
    #data['Time']  = data['Time'].dt.strftime('%Y-%m-%d')
    
    titlestr = "Plotting " + str(days) + " Days, From " + str(datetimedata.iloc[0])  + " to " + str(datetimedata.iloc[-1])
    
    data.plot(x='Time', subplots = True, layout = (3,6), title = titlestr, marker = 'o', fontsize = 7)
    
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    #plot.rcParams.update({'font.size': 9})
    plt.show()

#time = convert_unixarray_timesamparray(time)
#
##timeconvert = time.apply(converttimestamp)
#figsize = plt.figaspect(1/2)
#fig, axs = plt.subplots(1,2,figsize=figsize) 
#
#
##ax1 = plt.subplot(121)
#axs[0].set_title('BTC')
#axs[0].plot(time,BTC)
#
#
##ax2 = plt.subplot(122)
#axs[1].set_title('Fiat')
#axs[1].plot(time,Fiat)
#
#
#plt.tight_layout()
#fig.autofmt_xdate()
  

    
