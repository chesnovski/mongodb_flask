from tradingview_ta import TA_Handler, Interval
from tradingview_ta import TradingView

import time
from datetime import datetime
import datetime
from firebase import* 
import json
import requests
from mongodb import connection_with_db
import pandas as pd


    # INTERVAL_1_MINUTE = "1m"
    # INTERVAL_5_MINUTES = "5m"
    # INTERVAL_15_MINUTES = "15m"
    # INTERVAL_30_MINUTES = "30m"
    # INTERVAL_1_HOUR = "1h"
    # INTERVAL_2_HOURS = "2h"
    # INTERVAL_4_HOURS = "4h"
    # INTERVAL_1_DAY = "1d"
    # INTERVAL_1_WEEK = "1W"
    # INTERVAL_1_MONTH = "1M"


mydatabase = connection_with_db()


# symbols = ['ETHUSDT', 'BNBUSDT', 'LTCUSDT', 'BTCUSDT']
date = datetime.datetime.now()
time_stamp = date.timestamp()
dt_string_date = date.strftime("%d-%m-%Y")
df_string_time = date.strftime("%H:%M")


class Crypto():
    """crypto input parameters description"""
    def __init__(self , currency_params, timer):
        self.timer = timer
        self.symbol = currency_params['name']
        self.exchange = currency_params['exchange']

    def get_recommend(self):
        output= TA_Handler(
            symbol=self.symbol,
            screener='Crypto',
            exchange = self.exchange,
            interval=self.timer
        )
        recommendation=output.get_analysis().summary["RECOMMENDATION"]
        return recommendation
  

    def get_data(self):
            recommendation = self.get_recommend()
            url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={self.symbol}"
            data = requests.get(url)
            data = data.json()
            price = float(data['lastPrice'])
            price_change_percent = data['priceChangePercent']
            high_price = float(data['highPrice'])
            low_price = float(data['lowPrice'])
            high_curr = float(data['highPrice'])-(price)
            low_curr = float(data['lowPrice'])-(price)
            result = {'time frame':f'{self.timer}','symbol':f'{self.symbol}', 'date':f'{dt_string_date}', 'time':f'{df_string_time}',
                            'recomendation':f'{recommendation}', 'price':f'{price}',
                            'price change percent':f'{price_change_percent}', 'high price': f'{high_price}',
                            'low price':f'{low_price}', 'high&curr':f'{high_curr}', 'low&curr':f'{low_curr}', 'exchange':f"{self.exchange}", 'timestamp':f'{time_stamp}'
                            }
            collection_crypto = mydatabase.binance_currency
            inserted_id=collection_crypto.insert_one(result).inserted_id
            return inserted_id



def get_fear_index():
    fear_index_api='https://api.alternative.me/fng/?limit=2'
    fear_index=requests.get(fear_index_api)
    fear_index=fear_index.json()
    today_fear_index=fear_index['data'][0]
    collection_fear=mydatabase.fear_index
    inserted_fear_index=collection_fear.insert_one(today_fear_index).inserted_id
    return inserted_fear_index, collection_fear
    


inserted_fear_index, collection_fear=get_fear_index()



class Stocks():
    """stocks input parameters description"""
    def __init__(self, timer, stocks_params):
        """properties"""
        self.timer = timer
        self.stocks_params = stocks_params


    def get_stocks_info(self):
            output= TA_Handler(
                    symbol = self.stocks_params['stock_symbol'],
                    screener = self.stocks_params['screener'],
                    exchange = self.stocks_params['exchange'],
                    interval = self.timer
                )
            stock_info = output.get_analysis()
            open_price = round(stock_info.indicators['open'],2)
            close_price = round(stock_info.indicators['close'],2)
            change_price = round(stock_info.indicators['change'],2)
            high = round(stock_info.indicators['high'],2)
            low = round(stock_info.indicators['low'],2)
            result_info = {'name':f"{self.stocks_params['name']}", 'time frame':f'{self.timer}', 'symbol':f"{self.stocks_params['stock_symbol']}", 'open price':f'{open_price}',
                    'current price':f'{close_price}', 'change price':f'{change_price}', 'high price':f'{high}', 'low price':f'{low}',
                    'date':f'{dt_string_date}', 'time':f'{df_string_time}', 'exchange':f"{self.stocks_params['exchange']}", 'timestamp':f'{time_stamp}'
                    }
            collection_stocks = mydatabase.stocks_currency
            inserted_id = collection_stocks.insert_one(result_info).inserted_id
            return inserted_id
    



  
def main():
    """ read  parameters from csv """
    input_stocks_info = pd.read_csv('my_file.csv')
    stocks_info_dict = input_stocks_info.to_dict('index')
    input_crypto_info = pd.read_csv('my_file _crypto.csv')
    crypto_info_dict = input_crypto_info.to_dict('index')

    """ end """
    time_frame = ['15m', '1h', '4h', '1d']
    for timer in time_frame:
        for currency_params in crypto_info_dict.values():
            crypto = Crypto(currency_params, timer)
            crypto.get_data()
            # recommendation = get_recommend(symbol['name'], timer)
            # result = get_data(symbol['name'], recommendation)
        for stocks in stocks_info_dict.values() :
                stock = Stocks(timer, stocks)
                stock.get_stocks_info()
    inserted_fear_index=get_fear_index()


if __name__ == "__main__":
    main()
    print('----------------------------------------')




