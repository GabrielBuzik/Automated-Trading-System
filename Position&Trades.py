import numpy as np
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from binance.enums import *
client = Client()
import datetime
import time
from datetime import datetime, date, time

for i in client.futures_position_information():
    if i['symbol'] == 'BTCBUSD':
        print('current BTCBUSD position:')
        Pose_BUSD = i 

BUSD_Balance = client.futures_account_balance()[-1]['balance']
BUSD_symbol_name = client.futures_account_balance()[-1]['asset']

a=client.futures_account_trades()
times=np.zeros(len(a))

print('current BTCBUSD position:{}'.format(Pose_BUSD))
print('The account balance in BUSD is {} units of {}'.format(BUSD_Balance, BUSD_symbol_name))
print('Trades:')
for i in a:
    print(datetime.fromtimestamp(i['time']/1000),i['side'],i['qty'],i['price'],i['symbol'])
