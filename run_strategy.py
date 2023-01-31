import os
import numpy as np
from binance import Client
from binance.enums import *
import Module as mb


# API Key and Secret key
client = Client()
np.set_printoptions(precision=10, threshold=100)

# Coef
AMOUNT_TRADED = 0.001

# Functions


def get_klines() -> np.ndarray:
    """Return Open High Low Close as an array."""
    data = client.futures_klines(symbol='BTCBUSD', interval='1h', limit=100)
    data_array = np.array(data)[:, 1:5]
    OHLC = data_array.astype(float)
    return OHLC


def cheque_position() -> str:
    """Return curent position"""
    if os.path.exists('state.txt'):
        with open('state.txt') as f:
            STATE = f.read()
    else:
        f = open("state.txt", "w")
        f.write('hold')
        f.close()
        with open('state.txt') as f:
            STATE = f.read()
    return STATE


def stop_loss_upper(OHLC):
        SL = mb.ATR_Trailing_Stops_BuyOrd(5, 2, OHLC)
        count = cheque_count('buy.txt')
        if count > 99:
            count = 99
        SL_max = np.max(SL[(99-count):99])
        return SL_max


def stop_loss_lower(OHLC):
    SL = mb.ATR_Trailing_Stops_SellOrd(5, 2, OHLC)
    count = cheque_count('buy.txt')
    if count > 99:
        count = 99
    SL_min = np.min(SL[(99-count):99])
    return SL_min


def init_count(file_name):
    """Start counting periods when enter a trade"""
    with open(file_name, 'w') as f:
        f.write('1')
        f.close()


def add_count(file_name):
    current_number = cheque_count(file_name)
    with open(file_name, 'w') as f:
            f.write(str(current_number))
            f.close()


def cheque_count(file_name) -> int:
    if os.path.exists('buy.txt'):
        with open('buy.txt') as f:
            count = int(f.read())
    return count


def make_trade(position_side: str, amount: float) -> None:
    """Set leverage and execute an order"""
    client.futures_change_leverage(symbol='BTCBUSD', leverage=4)
    # client.futures_create_order(symbol='BTCBUSD',
    #                           type='MARKET',
    #                            side=position_side,
    #                            quantity=amount)


def enter(side: str, file_name: str, amount: float) -> str:
    make_trade(side, amount)
    init_count(file_name)
    # import add_to_database
    if side == 'BUY':
        return 'yes_buy'
    else:
        return 'yes_sell'


def close(side: str, amount: float) -> str:
    make_trade('SELL', amount)
    # import add_to_database
    return 'hold'


def write_state(state):
    f = open("state.txt", "w")
    f.write(state)
    f.close()
    print(state)


def main(state: str,
         CLOSE: np.ndarray,
         OHLC: np.ndarray,
         ravi: np.ndarray) -> str:
    print(state)
    if state == 'hold':
        if mb.ravi_sign_to_pos(ravi):
            return enter('BUY', 'buy.txt', AMOUNT_TRADED)
        elif mb.ravi_sign_to_neg(ravi):
            return enter('SELL', 'sell.txt', AMOUNT_TRADED)
        else:
            return 'hold'
    elif state == 'yes_buy':
        stop_loss = stop_loss_upper(OHLC)
        if mb.exit_long(ravi, CLOSE, stop_loss):
            if ravi[-1] < 0:
                return enter('SELL', 'sell.txt', 2*AMOUNT_TRADED)
            else:
                return close('SELL', AMOUNT_TRADED)
        else:
            add_count('buy.txt')
            return 'yes_buy'
    elif state == 'yes_sell':
        stop_loss = stop_loss_lower(OHLC)
        if mb.exit_short(ravi, CLOSE, stop_loss):
            if ravi[-1] > 0:
                return enter('BUY', 'buy.txt', 2*AMOUNT_TRADED)
            else:
                return close('BUY', AMOUNT_TRADED)
        else:
            add_count('sell.txt')
            return 'yes_sell'


# The code
print('start')
OHLC = get_klines()
CLOSE = OHLC[:, 3]
STATE = cheque_position()
ravi = mb.ravi(5, 50, CLOSE)
print(ravi)
if __name__ == "__main__":
    NEW_STATE = main(STATE, CLOSE, OHLC, ravi)
    write_state(NEW_STATE)
