from tradingview_ta import TA_Handler, Interval
from tradingview_ta import TradingView

import time
from datetime import datetime
import datetime
from firebase import* 
import json
import requests
from mongodb import *


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


def get_data(key, j):
            url = key+symbols[j]  
            data = requests.get(url)
            data = data.json()
            return data
def get_price_data(price_data,volatility_data):
        price=float(price_data['price'])
        price_change_percent=volatility_data['priceChangePercent']
        high_price=float(volatility_data['highPrice'])
        low_price=float(volatility_data['lowPrice'])
        high_curr=float(volatility_data['highPrice'])-(price)
        low_curr=float(volatility_data['lowPrice'])-(price)
        return price, price_change_percent, high_price, low_price, high_curr, low_curr   
def get_recommend(timer):
    output= TA_Handler(
            symbol=symbol,
            screener='Crypto',
            exchange='Binance',
            interval=timer
        )
    recommend=output.get_analysis().summary["RECOMMENDATION"]
    return recommend

def get_stocks_info(time_frame, stock_symbol, screener, exchange):
    for timer in time_frame:
        output= TA_Handler(
                symbol=stock_symbol,
                screener=screener,
                exchange=exchange,
                interval=timer
            )
        stock_info=output.get_analysis()
        open_price=stock_info.indicators['open']
        close_price=stock_info.indicators['close']
        change_price=stock_info.indicators['change']
        high=stock_info.indicators['high']
        low=stock_info.indicators['low']
        result_info = {'time frame':f'{timer}', 'symbol':f'{stock_symbol}', 'open price':f'{open_price}$',
                'current price':f'{close_price}$', 'change price':f'{change_price}%', 'high price':f'{high}$', 'low price':f'{low}$',
                'date':f'{dt_string_date}', 'time':f'{df_string_time}' 
                }
        collection_stocks=mydatabase.stocks_currency
        inserted_id=collection_stocks.insert_one(result_info).inserted_id


    return result_info









def inser_text_doc(result,timer,collection):
    # if timer==time_frame[0]:
    inserted_id=collection.insert_one(result).inserted_id
    print(inserted_id)

def get_fear_index():
    fear_index_api='https://api.alternative.me/fng/?limit=2'
    fear_index=requests.get(fear_index_api)
    fear_index=fear_index.json()
    today_fear_index=fear_index['data'][0]
    collection_fear=mydatabase.fear_index
    inserted_fear_index=collection_fear.insert_one(today_fear_index).inserted_id
    return inserted_fear_index, collection_fear
    


inserted_fear_index, collection_fear=get_fear_index()

fear_info=[]
# info=collection_fear.distinct("data.0").sort({"timestamp":-1})
info=collection_fear.aggregate( [ { '$unwind' : "$0" } ] )
        # info['_id']=str(info['_id'])
        # info['data.timestamp'] = str(datetime.date.fromtimestamp(info['timestamp']))
print(info)
fear_info.append(info)





 

  
while(True):
    # symbols=['ETHUSDT', 'BNBUSDT', 'LTCUSDT', 'BTCUSDT','XRPUSDT','DOGEUSDT','LINKUSDT']
    time_frame = ['15m', '1h', '4h', '1d']
    symbols = ['ETHUSDT', 'BNBUSDT', 'LTCUSDT', 'BTCUSDT']
    key = "https://api.binance.com/api/v3/ticker/price?symbol="
    key2 = "https://api.binance.com/api/v3/ticker/24hr?symbol="
    date=datetime.datetime.now()
    dt_string_date = date.strftime("%d-%m-%Y")
    df_string_time = date.strftime("%H:%M")


    nasdaq = get_stocks_info(time_frame, 'NDX', 'america', 'NASDAQ')
    spx = get_stocks_info(time_frame, 'SPX', 'cfd', 'SP') 
    dji = get_stocks_info(time_frame, 'DJI', 'cfd', 'TVC') 
    dax = get_stocks_info(time_frame, 'DAX', 'cfd', 'XETR') 
    cac40 = get_stocks_info(time_frame, 'CAC40', 'cfd', 'TVC') 
    ukx = get_stocks_info(time_frame, 'UKX', 'cfd', 'TVC') 
    sse = get_stocks_info(time_frame, '000001', 'cfd', 'SSE') 
    bno = get_stocks_info(time_frame, 'UKOIL', 'cfd', 'FX') 
    gold = get_stocks_info(time_frame, 'GOLD', 'cfd', 'TVC')
    silver = get_stocks_info(time_frame, 'SILVER', 'cfd', 'TVC')
    zw1 = get_stocks_info(time_frame, 'ZW1!', 'america', 'CBOT') 
    kc1 = get_stocks_info(time_frame, 'KC1!', 'america', 'ICEUS') 




    j = 0
    for symbol in symbols:
            price_data=get_data(key, j)
            volatility_data=get_data(key2, j)
            price, price_change_percent, high_price, low_price, high_curr, low_curr=get_price_data(price_data,volatility_data)
            for timer in time_frame:
                recommend=get_recommend(timer)
                result={'time frame':f'{timer}','symbol':f'{symbol}', 'date':f'{dt_string_date}', 'time':f'{df_string_time}',
                        'recomendation':f'{recommend}', 'price':f'{price}$',
                        'price change percent':f'{price_change_percent}%', 'high price': f'{high_price}$',
                        'low price':f'{low_price}$', 'high&curr':f'{high_curr}$', 'low&curr':f'{low_curr}$'}
                collection_crypto=mydatabase.binance_currency
                inser_text_doc(result,timer,collection_crypto)
                # print(result)
                # #upload to the database
                # database.child(f'Curr_{timer}').child(f'{dt_string}').child(f'Coin_{symbol}').set(result)
                # print(result)
            j+=1
    inserted_fear_index=get_fear_index()


        
        

    time.sleep(300)
    print('-----------------------------------')



