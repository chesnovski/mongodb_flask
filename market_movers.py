import os
import requests
import time
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


# load the key from the enviroment variables
api_key = os.getenv('key_api')

ticker="MSFT"

def get_stock_price(exchange_name, api_key):
  url = f"https://api.twelvedata.com/market_state?&apikey={api_key}"
  response = requests.get(url).json()
  print(response)

get_stock_price("NYSE", api_key)

