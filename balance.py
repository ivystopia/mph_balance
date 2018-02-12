#! /usr/bin/env python

# Distributed under MIT license, please see LICENSE file

import requests
import argparse
import json
import time
import csv
import datetime
import os
import numpy as np
import sys
import pandas as pd

filename = "defaults.txt"
f = open(filename, 'r')
APIkey = f.readline().rstrip()
Fiat = f.readline().rstrip()
Crypto = f.readline().rstrip()
Output = f.readline().rstrip()




parser = argparse.ArgumentParser(description="Estimate total balance of a MPH account")
parser.add_argument('-a', metavar='api_key', default = APIkey, help='API key from account settings page')
parser.add_argument('-f', metavar='fiat_currency', default=Fiat, help='Which fiat currency to display total in')
parser.add_argument('-c', metavar='currency', default=Crypto, help='Which exchange currency to display total in (default btc)')
parser.add_argument('-o', metavar='output', default=Output, choices=["text", "csv"], help='Output format. "text" (default) or csv')
args = parser.parse_args()

symbols = {
      "adzcoin": "ADZ",
      "auroracoin": "AUR",
      "bitcoin": "BTC",
      "bitcoin-cash": "BCH",
      "bitcoin-gold": "BTG",
      "dash": "DSH",
      "digibyte": "DGB",
      "digibyte-groestl": "DGB",
      "digibyte-skein": "DGB",
      "digibyte-qubit": "DGB",
      "ethereum": "ETH",
      "ethereum-classic": "ETC",
      "expanse": "EXP",
      "feathercoin": "FTC",
      "gamecredits": "GAME",
      "geocoin": "GEO",
      "globalboosty": "BSTY",
      "groestlcoin": "GRS",
      "litecoin": "LTC",
      "maxcoin": "MAX",
      "monacoin": "MONA",
      "monero": "XMR",
      "musicoin": "MUSIC",
      "myriadcoin": "XMY",
      "myriadcoin-skein": "XMY",
      "myriadcoin-groestl": "XMY",
      "myriadcoin-yescrypt": "XMY",
      "sexcoin": "SXC",
      "siacoin": "SC",
      "startcoin": "START",
      "verge": "XVG",
      "vertcoin": "VTC",
      "zcash": "ZEC",
      "zclassic": "ZCL",
      "zcoin": "XZC",
      "zencash": "ZEN"
}

def get_value(symbol, amount, compare=args.c):
    """
    Convert some amount of some coin, into the currency specified by -c
    """
    if symbol.upper() == compare.upper():
        return amount
    #sometimes the API does not respond so this loop tri
    num_attempts = 10
    for attempt in range(num_attempts):
        url = "https://api.cryptonator.com/api/ticker/{}-{}".format(symbol.lower(), compare.lower())
        raw_response = requests.get(url).text    
        
        try:
            response = json.loads(raw_response)
            if(response["success"]):
                price = response["ticker"]["price"]
                value = float(price) * float(amount)
                print("Successfully obtained data for " +symbol)
                return value
            else:
                print(symbol + " is not on ticker website")
                return 0 #returns zero if the coin is not on the ticker website
        except json.decoder.JSONDecodeError:
            print("JSON decode error from ticker " + symbol + " in attempt #" + str(attempt + 1))
            time.sleep(10)
            print("Trying again...")
            
    sys.exit("couldn't get response from website")
    return 0
#log_filename  = datetime.date.today().strftime('Data\monitorlog_%Y-%m-%d.csv')

def obtain_mph_balance():
    os.system('clear')
    log_filename  = ('Data\monitorlog.csv')
    should_write_header = 1
    should_write_header = int(not (os.path.exists(log_filename)))
    # Query the MPH API to get all current balances
    
    url = "https://miningpoolhub.com/index.php?page=api&action=getuserallbalances&api_key={}".format(args.a)
    raw_response = requests.get(url).text
    response = json.loads(raw_response)
    coindata = []
    coinheaders = []

        # Parse the response into a basic dictionary keyed on coin name
    coins = {}
    for coin in response["getuserallbalances"]["data"]:
        symbol = symbols[coin["coin"]]
        balance = sum([
            coin["confirmed"],
            coin["unconfirmed"],
            coin["ae_confirmed"],
            coin["ae_unconfirmed"],
            coin["exchange"]
               ])
        coins[symbol] = balance
        if(balance != 0):
            coinheaders.extend([symbol])
            coindata.extend([balance])


          # Get the total value of all the coin balances
    
    value_total = 0
    valuelist = []
    #TODO:need to improve pandas handling here
    #getting btc value for each coin and making a new datafram for printing 
    for coin in coins:
        value_new = get_value(coin, coins[coin], "btc")
        valuelist.append([coin,coins[coin],value_new])
        value_total = value_total + value_new
    fiat_value = get_value("btc", value_total, "usd")
    
    #convert the list into a dataframe and set the index to the ticker name
    valuelist = pd.DataFrame(valuelist, columns = ['ticker','amount','value'])
    valuelist = valuelist.sort_values(by = ['value'],ascending = False)
    valuelist = valuelist.set_index('ticker')
    
    #clear the screen and print the amount of each coin
    os.system('clear')
    for coin,row in valuelist.iterrows():
        print(coin + ": "+ str(row['amount']) + " worth " + str(row['value']) + " BTC")
    print("Total Value (BTC): " + str(value_total))
    print("Total Value (USD): " + str(fiat_value))
      # Print report

    coindata = [int(time.time()),value_total,round(fiat_value, 3)] + coindata
    coinheaders = ["Time","BTC_total","Fiat_total"] + coinheaders

    if should_write_header:
        with open(log_filename, 'w') as f:
            Writer = csv.writer(f, lineterminator='\n')
            print(coinheaders)
            Writer.writerow(coinheaders)
            should_write_header = 0



    with open(log_filename, 'a') as f:
        Writer = csv.writer(f, lineterminator='\n')
        Writer.writerow(coindata)
    #print(coindata)
    #time.sleep(50)

#if __name__ == "__main__":
#    main()
