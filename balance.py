#! /usr/bin/env python

# Distributed under MIT license, please see LICENSE file

import requests
import argparse
import json
import time
import csv
import datetime
import os

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
	url = "https://api.cryptonator.com/api/ticker/{}-{}".format(symbol.lower(), compare.lower())
	raw_response = requests.get(url).text
	response = json.loads(raw_response)
	if(response["success"]):
		price = response["ticker"]["price"]
		value = float(price) * float(amount)
		return value
	else:
		return 0 #returns zero if the coin is not on the ticker website

#log_filename  = datetime.date.today().strftime('Data\monitorlog_%Y-%m-%d.csv')

def main():
	log_filename  = ('Data\monitorlog.csv')
	should_write_header = 1
	should_write_header = int(not (os.path.exists(log_filename)))
	# Query the MPH API to get all current balances
	while (True):

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
		value = sum([get_value(coin, coins[coin], args.c) for coin in coins])
		fiat_value = get_value(args.c, value, args.f)

		  # Print report

#	   coindata.exend([int(time.time()),value,round(fiat_value, 3)])
#	   coinheaders.extend(["time","BTC_total_value","Fiat_total_value"])
		coindata = [int(time.time()),value,round(fiat_value, 3)] + coindata
		coinheaders = ["Time","BTC_total_value","Fiat_total_value"] + coinheaders

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
		time.sleep(50)

if __name__ == "__main__":
	main()
