# mph_balance
Print total balance of Mining Pool Hub wallets. Very minimal output for use in other scripts, bots etc.

# Installing
You need Python 3.

Set up virtualenv (or use sudo for the following command if running globally)

`pip install -r requirements.txt`

# Using
Get your API key from your account details page: https://miningpoolhub.com/?page=account&action=edit

create a file defaults.txt that has the following information seperated by newlines:
api_key
Fiat currency (usd, gpb)
crpyto currency (btc)
outpt type (text, csv)

Run the program like so:

python balance.py

default parameters can be changed during excecution with flags.

Fiat currency: `-f` argument (e.g. -f USD)

Cryptocurrency: `-c` argument (e.g. -c LTC)

apikey: `-a`

output format: -o

# License
MIT (See LICENSE file)
