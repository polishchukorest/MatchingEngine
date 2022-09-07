import pandas as pd
import csv
import numpy as np
from lightmatchingengine.lightmatchingengine import LightMatchingEngine, Side



#simple converting function
def convert_side(str):
    if str.lower().strip() in ['bid', 'buy']:
        return 1
    elif str.lower().strip() in ['ask', 'sell']:
        return 2
    else:
        return None


if __name__ == "__main__":
    #reading file with order trades
    df = pd.read_csv("TestTask//okcoin_incremental_book_L2_2020-01-01_BTC-USD_raw.csv")
    df.drop('is_snapshot', axis=1, inplace=True)

    #reading file with market trades
    df_market = pd.read_csv("TestTask//okcoin_trades_2020-01-01_BTC-USD.csv", delimiter=';')
    #converting them to the order trades with min possible price for sell and max pirce for buy
    df_market['price'] = np.where(df_market['side'] == 'sell', np.finfo(np.float64).min, np.finfo(np.float64).max)
    df_market = df_market.loc[:, df.columns]
    #adding them in one dataframe and sorting them by time
    df = df.append(df_market)
    df.sort_values(by=['timestamp', 'local_timestamp'])
    print(df.size)

    lme = LightMatchingEngine()

    # trades_df = pd.DataFrame()
    file = open('trades.csv', 'w')
    writer = csv.writer(file)

    #iterating over dataframe, taking data from each row and adding to the matching machine
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
                #writing directly to csv for speedup
                writer.writerow([trade.order_id, trade.instmt,
                                 trade.trade_price, trade.trade_qty,
                                 trade.trade_side, trade.trade_id])

    file.close()

