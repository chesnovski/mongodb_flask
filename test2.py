
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
    "symbol": "S&P 500 "
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '9fb49d1c-3f0b-4617-a3c5-edd911f87186',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  tags=data
  print(tags)
#   tags=data['data']['ETH']['quote']['USD']


except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)