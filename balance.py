#! /usr/bin/env python

import requests
import argparse
import json

parser = argparse.ArgumentParser(description="Estimate total balance of a MPH account")
parser.add_argument('-a', metavar='api_key', required=True, help='API key from account settings page')
args = parser.parse_args()

def main():

  # Query the MPH API to get all current balances
  url = "https://miningpoolhub.com/index.php?page=api&action=getuserallbalances&api_key={}".format(args.a)
  raw_response = requests.get(url).text
  response = json.loads(raw_response)
  print(response)


if __name__ == "__main__":
  main()
