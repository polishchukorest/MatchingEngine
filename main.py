import pandas as pd
import csv
import numpy as np
import sys
from lightmatchingengine.lightmatchingengine import LightMatchingEngine, Side

from threading import Thread
from collections import deque


def convert_side(str):
    if str.lower().strip() in ['bid', 'buy']:
        return 1
    elif str.lower().strip() in ['ask', 'sell']:
        return 2
    else:
        return None


if __name__ == "__main__":

    df = pd.read_csv("TestTask//okcoin_incremental_book_L2_2020-01-01_BTC-USD_raw.csv")
    df.drop('is_snapshot', axis=1, inplace=True)

    df_market = pd.read_csv("TestTask//okcoin_trades_2020-01-01_BTC-USD.csv", delimiter=';')
    df_market['price'] = np.where(df_market['side'] == 'sell', np.finfo(np.float64).min, np.finfo(np.float64).max)
    df_market = df_market.loc[:, df.columns]
    df = df.append(df_market)
    df.sort_values(by=['timestamp', 'local_timestamp'])
    print(df.size)

    lme = LightMatchingEngine()

    trades_dict = dict(order_id=[], instmt=[], trade_price=[], trade_qty=[], trade_side=[], trade_id=[])
    trades_df = pd.DataFrame(trades_dict)
    # trades_df = pd.DataFrame()
    file = open('trades.csv', 'w')
    writer = csv.writer(file)

    for index, row in df.iterrows():
        print(index)
        name = row['symbol']
        price = row['price']
        qty = row['amount']
        side = convert_side(row['side'])
        # test
        order, trades = lme.add_order(name, price, qty, side)
        if trades is not None:
            for trade in trades:
                writer.writerow([trade.order_id, trade.instmt,
                                 trade.trade_price, trade.trade_qty,
                                 trade.trade_side, trade.trade_id])
                '''trades_df = trades_df.append([trade.order_id, trade.instmt,
                                  trade.trade_price, trade.trade_qty,
                                  trade.trade_side, trade.trade_id])'''
                # print(trades_df.size)
                '''trades_dict['order_id'].append(trade.order_id)
                trades_dict['instmt'].append(trade.instmt)
                trades_dict['trade_price'].append(trade.trade_price)
                trades_dict['trade_qty'].append(trade.trade_qty)
                trades_dict['trade_side'].append(trade.trade_side)
                trades_dict['trade_id'].append(trade.trade_id)'''
        # if index == 1000:
        #    break
    file.close()
    # trades_df.to_csv('trades.csv')
    # print(len(trades))
    # print(trades_dict.items())
