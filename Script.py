# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 15:58:05 2018

@author: aspit
"""

"""
Following configurations are set for the scheduler:

 - a MongoDBJobStore named “mongo”
 - an SQLAlchemyJobStore named “default” (using SQLite)
 - a ThreadPoolExecutor named “default”, with a worker count of 20
 - a ProcessPoolExecutor named “processpool”, with a worker count of 5
 - UTC as the scheduler’s timezone
 - coalescing turned off for new jobs by default
 - a default maximum instance limit of 3 for new jobs
"""


from balance import obtain_mph_balance

from datetime import datetime, timedelta

import time

while 1:
    print('.')
    obtain_mph_balance()
    
    dt = datetime.now() + timedelta(hours=1)
    dt = dt.replace(minute=10)

    while datetime.now() < dt:
        time.sleep(1)