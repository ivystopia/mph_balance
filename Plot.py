# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 14:33:17 2017

@author: aspit
"""


def converttimestamp(stamp):
	return datetime.datetime.fromtimestamp(int(stamp)).strftime('%Y-%m-%d %H:%M:%S')
	
	
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

df = pd.read_csv('Data/monitorlog.csv')

time = df['Time']
BTC = df['BTC_total_value']
Fiat = df['Fiat_total_value']

timeconvert = time.apply(converttimestamp)

ax1 = plt.subplot(121)
ax1.set_title('BTC')
ax1.plot(time,BTC)


ax2 = plt.subplot(122)
ax2.set_title('Fiat')
ax2.plot(time,Fiat)

plt.show()

  
    
    
