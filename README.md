# mph_balance
Print total balance of Mining Pool Hub wallets. Very minimal output for use in other scripts, bots etc.

# Installing
You need Python 3.

Set up virtualenv (or use sudo for the following command if running globally)

`pip install -r requirements.txt`

# Using
Get your API key from your account details page: https://miningpoolhub.com/?page=account&action=edit

Run the program like so:

`./balance.py -a api_key`

Default fiat currency is GBP. You can specify a different currency with the `-f` argument (e.g. -f USD)

Default crypto currency is BTC. You can specify a different currency with the `-c` argument (e.g. -c LTC)

# License
MIT (See LICENSE file)
