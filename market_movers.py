import requests
import json


api = 'nRvVqb9piYCXoBAskwPbuDpMDnoyGbnq'
# year = '2023'
# month = '01'
# day = '03'
limit = '30'


api_url = f'https://api.polygon.io/v2/reference/news?ticker=MASS&limit=20&apiKey={api}'
data = requests.get(api_url).json()
list_news = []

for i in range(int(limit)):
    try:
        description = data['results'][i]['description']
        article_url = (data['results'][i]['article_url'])
        article_image = (data['results'][i]['image_url'])
        title = (data['results'][i]['title'])
        keywords = (data['results'][i]['keywords'])
        if len(description) > 20:
            news = {'title':f'{title}', 'description':f'{description}', 'article_url':f'{article_url}', 
            'keywords':f'{keywords}', 'image_url':f'{article_image}'
            }  
            list_news.append(news)
    except:
        pass



