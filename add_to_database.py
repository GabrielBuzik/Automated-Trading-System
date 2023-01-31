"This file replicates the last transaction to personal database"

from datetime import datetime
# Firstly, import module allowing to access and write queries to our database
import psycopg2

# Also binance libraries are required as the data on account transactions is replicated from their servers
from binance import Client
from binance.enums import *


client = Client()


# Obviously not showing my keys

# Get the last trade from Binance
last_trade = client.futures_account_trades()[-1]

# Connect to our database
conn = psycopg2.connect(database='Binance', user='postgres', password='')
cur = conn.cursor()

# Now set all attributes to be inserted into database
trade_datetime = str(datetime.fromtimestamp(last_trade['time']/1000))
symbol = last_trade['symbol']
side = last_trade['side']
price = last_trade['price']
quantity = last_trade['qty']
amount = last_trade['quoteQty']
fee = last_trade['commission']
profit = last_trade['realizedPnl']

# SQL query to insert data
values = f"VALUES(\'{trade_datetime}\',\'{symbol}\',\'{side}\',{price},{quantity},{amount},{fee},{profit})"
query = "INSERT INTO trades (trade_datetime,symbol,side,price,quantity,amount,fee,profit) " + values

cur.execute(query)
conn.commit()
