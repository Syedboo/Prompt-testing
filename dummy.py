from newsapi import NewsApiClient
import pandas as pd
import sentistrength
from sentistrength import PySentiStr
# Init
newsapi = NewsApiClient(api_key='d164128159094d9a9964a86602a45892')


import requests

api_key = 'YOUR_NEWSAPI_KEY'
url = 'https://newsapi.org/v2/everything'

params = {
    'q': 'TESCO',
    'from': '2024-07-10',
    'to': '2024-08-08',
    'sortBy': 'relevancy',
    'language': 'en',
    'apiKey': 'd164128159094d9a9964a86602a45892',
    'pageSize': 100,
    'page': 1
}

response = requests.get(url, params=params)
data = response.json()

articles = data['articles']
print(len(articles))
for article in articles:
    print(f"Title: {article['title']}")
    print(f"Published At: {article['publishedAt']}")
    print(f"Source: {article['source']['name']}")
    print(f"Description: {article['description']}")
    print(f"URL: {article['url']}")
    print("\n")
