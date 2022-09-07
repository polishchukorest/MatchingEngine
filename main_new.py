from orderbook import *
import pandas  as pd
from matching_engine import *

def convert_side(str):
    if str.lower().strip() in ['bid', 'buy']:
        return 'buy'
    elif str.lower().strip() in ['ask', 'sell']:
        return 'sell'
    else:
        return None

if __name__ == "__main__":
    #read csv and sort by time
    df = pd.read_csv("TestTask//okcoin_incremental_book_L2_2020-01-01_BTC-USD_raw.csv")
    df.sort_values(by=['timestamp', 'local_timestamp'])

    #run the Matching Engine
    me = MatchingEngine(threaded=False)



    for index, row in df.iterrows():
        name = row['symbol']
        price = row['price']
        qty = row['amount']
        side = convert_side(row['side'])

        order = Order(name, side, price, qty)
        # test
        if qty != 0:
            me.process(order)
    print(me.get_trades())

