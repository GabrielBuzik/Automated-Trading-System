from datetime import datetime
import numpy as np
from binance.client import Client
client = Client()  # Paste API key and secret key as arguments

for i in client.futures_position_information():
    if i['symbol'] == 'BTCBUSD':
        print('current BTCBUSD position:')
        Pose_BUSD = i

busd_balance = client.futures_account_balance()[-1]['balance']
busd_symbol_name = client.futures_account_balance()[-1]['asset']

recent_trades = client.futures_account_trades()
times = np.zeros(len(recent_trades))

print('current BTCBUSD position:{}'.format(Pose_BUSD))
print('The account balance in BUSD is {} units of {}'.format(
    busd_balance, busd_symbol_name))
print('Trades:')
for i in recent_trades:
    print(datetime.fromtimestamp(i['time']/1000),
          i['side'],
          i['qty'],
          i['price'],
          i['symbol'])
