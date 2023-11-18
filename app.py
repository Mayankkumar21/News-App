import json
from flask import Flask, abort, jsonify,render_template,request,redirect, url_for
from newsapi import NewsApiClient
import redis,sys
from datetime import datetime, timedelta
import requests,time
app=Flask(__name__)


# Create connectivity to the Redis server
def redis_connect():
    try:
        client = redis.Redis(host="localhost",port=6379,db=0,socket_timeout=5,)
        ping = client.ping()
        if ping is True:
            return client
    except redis.AuthenticationError:
        print("AuthenticationError")
        sys.exit(1)

# Create client
redis_client = redis_connect()


def get_news_data_from_cache(key: str) -> list:
    try:
        cache_data = redis_client.get(key)
        print("here is your cached data")
        print("this is the key in getting news from cache- "+key)
        print(cache_data)
        return cache_data
    except Exception as error:
        print(f"Error Occured : {error}")


# Add data to the redis cache with 3600s expiry
def put_news_data_to_cache(key: str, value: list) -> bool:
    try:
        data=json.dumps(value)
        # print(json.dumps(value))
        state = redis_client.setex(key, timedelta(seconds=3600), data)
        # time.sleep(5)
        return state
    except Exception as error:
        print(f"Error Occured : {error}")
        

# Obtain news data
def get_data(category: str) -> list:
    try:
        # Check data availability in Redis
        print("Checking redis for key")
        data = get_news_data_from_cache(key=category)
        # data=[]
        # If Aavailabe serve from cache
        if data is not None:
            print("Data Obtained From Cache")
            data = json.loads(data)
            return data
        else:
            # Get data from API
            data = get_news_from_api(category)

            # Check response
            if len(data)>0:
                print("Data Obtained From API")
                # data = data.content

                # Add data to cache
                state = put_news_data_to_cache(key=category, value=data)
                if state is True:
                    print("Data Added to Redis")
            return data
    except Exception as error:
        print(f"Error Occured : {error}")




api = NewsApiClient(api_key='30d7eb960aaf452293896183aaf05c55')
#api key- 30d7eb960aaf452293896183aaf05c55
news=[]
@app.route('/')
def frontend():
    return render_template('homepage.html',news=news)

@app.route("/news/<category>/",methods=["GET","POST"])
def handle_api_call(category):
    data=get_data(category=category)
    # print(data)
    global news
    news=data
    return render_template('index.html', news=news)



def get_news_from_api(cat):
    news_obj=api.get_top_headlines(country="in",category=cat)
    
    articles=news_obj['articles']
    
    # print(articles)
    data=[]
    print("We reached get_news_from_api")
    for article in articles:
        data.append({"Title":article['title'],
                     "Description":article['description'],
                     "urlToImage":article['urlToImage'],
                     "url":article['url'],
                     "publishedAt":article['publishedAt']
                     })
    return data
    
    
    
    
app.run(debug=True)