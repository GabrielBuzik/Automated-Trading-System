import numpy as np
import os
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from binance.enums import *
import module_bot as mb

#API Key and Secret key 
client = Client(api_key,secret_key)
np.set_printoptions(precision=10,threshold=100)

#RETRIEVE KLINES
#Open High Low Close as a numpy array
OHLC=((np.array(client.futures_klines(symbol='BTCBUSD',interval='1h',limit=100))[:,1:5]).astype(float))
C=OHLC[:,3]

#Cheque our current position: Hold means we are not in position,
#yes_buy means we are in long position, yes_sell means we are in short position
if os.path.exists('state.txt'):
	with open('state.txt') as f:
		STATE = f.read()
else:
	f = open("state.txt", "w")
	f.write('hold')
	f.close()
	with open('state.txt') as f:
		STATE = f.read()

#Depending on the position being entered or not, actions are chosen:
#Not in position yet:
ravi = mb.RAVI(5,50,C)
if STATE=='hold' or STATE== None:

	if mb.RAVI_sign_change_to_pos(5,50,ravi) or mb.RAVI_sign_change_to_pos_last_int(5,50,ravi):
		#transaction takes place
		client.futures_change_leverage(symbol='BTCBUSD', leverage=4)
		client.futures_create_order(symbol='BTCBUSD',type='MARKET',side='BUY',quantity=0.03)
		STATE='yes_buy'

		with open('buy.txt','w') as f:
			f.write('1')
			f.close()

		import add_to_database

	elif mb.RAVI_sign_change_to_neg(5,50,ravi) or mb.RAVI_sign_change_to_neg_last_int(5,50,ravi):
		#transaction takes place
		client.futures_change_leverage(symbol='BTCBUSD', leverage=4)
		client.futures_create_order(symbol='BTCBUSD',type='MARKET',side='SELL',quantity=0.03)

		STATE='yes_sell'
		with open('sell.txt', 'w') as f:
			f.write('1')
			f.close()
	
		import add_to_database

	else:
		STATE=='hold'
#In case a LONG position have been entered
elif STATE == 'yes_buy':
	#Trailing stop
	SL = mb.ATR_Trailing_Stops_BuyOrd(5,2,OHLC)
	#Intervals since open position 
	if os.path.exists('buy.txt'):
		with open('buy.txt') as f:
			BM=int(f.read())
	else:
		BM=1
	if BM<99:
		SL_max=np.max(SL[(99-BM):99])
	else:
		SL_max=np.max(SL[0:99])
	#Conditions for staying in position or leaving it 
	if  (ravi[-1]<(ravi[-2]-0.001) and ravi[-1]<(ravi[-3]-0.001)) or  ravi[-1]<0 or C[-1]<SL_max:
		if ravi[-1]<0:
			#transaction takes place
			client.futures_change_leverage(symbol='BTCBUSD', leverage=4)
			client.futures_create_order(symbol='BTCBUSD',type='MARKET',side='SELL',quantity=0.06)

			STATE='yes_sell'
			with open('sell.txt','w') as f:
				f.write('1')
				f.close()
			
			import add_to_database

		else:
			#transaction takes place
			client.futures_change_leverage(symbol='BTCBUSD', leverage=4)
			client.futures_create_order(symbol='BTCBUSD',type='MARKET',side='SELL',quantity=0.03)

			STATE='hold'

			import add_to_database
	else:
		STATE=='yes_buy'
		BM=BM+1
		with open('buy.txt', 'w') as f:
			f.write(str(BM))
			f.close()
#In case a SHORT position have been entered
elif STATE=='yes_sell':
	SL=mb.ATR_Trailing_Stops_SellOrd(5,2,OHLC)
	if os.path.exists('sell.txt'):
		with open('sell.txt') as f:
			BS=int(f.read())
	else:
		BS=1
	if BS<99:
		SL_min=np.min(SL[(99-BS):99])
	else:
		SL_min=np.min(SL[0:99])
    #Conditions for staying in position or leaving it
	if  (ravi[-1]>(ravi[-2]+0.001) and ravi[-1]>(ravi[-3]+0.001)) or ravi[-1]>0 or C[-1]>SL_min:
		if ravi[-1]>0:
			#transaction takes place
			client.futures_change_leverage(symbol='BTCBUSD', leverage=4)
			client.futures_create_order(symbol='BTCBUSD',type='MARKET',side='BUY',quantity=0.06)

			STATE='yes_buy'
			with open('buy.txt','w') as f:
				f.write('1')
				f.close()

			import add_to_database

		else:
			#transaction takes place
			client.futures_change_leverage(symbol='BTCBUSD', leverage=4)
			client.futures_create_order(symbol='BTCBUSD',type='MARKET',side='BUY',quantity=0.03)
			STATE='hold'
		
		import add_to_database
	else:
		STATE='yes_sell'
		BS=BS+1
		with open('sell.txt', 'w') as f:
			f.write(str(BS))
			f.close()
else:
	print('something is wrong')
	STATE='hold'
#Save the current state(in or out of position)
f = open("state.txt", "w")
f.write(STATE)
f.close()
print(STATE)
