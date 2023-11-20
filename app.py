import json
from flask import Flask, abort, jsonify,render_template,request,redirect, url_for
from newsapi import NewsApiClient
import redis,sys
from datetime import datetime, timedelta
import requests,time,os
# from dotenv import load_dotenv, dotenv_values

app=Flask(__name__)

# load_dotenv()

# redis_hash =({
#   "url": os.getenv("UPSTASH_REDIS_REST_URL"),
#   "token": os.getenv("UPSTASH_REDIS_REST_TOKEN"),
#   "PORT":os.getenv("PORT")
# })
UPSTASH_REDIS_REST_URL="apn1-singular-whippet-34240.upstash.io"
UPSTASH_REDIS_REST_TOKEN="b36b99cae8004776960edb231458ca88"
PORT="34240"

# print(redis_hash["url"])
# Create connectivity to the Redis server
def redis_connect():
    try:
        client = redis.Redis(host=UPSTASH_REDIS_REST_URL,port=PORT,password=UPSTASH_REDIS_REST_TOKEN,db=0,socket_timeout=5,)
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
       
        return cache_data
    except Exception as error:
        print(f"Error Occured : {error}")


# Add data to the redis cache with 3600s expiry
def put_news_data_to_cache(key: str, value: list) -> bool:
    try:
        data=json.dumps(value)
        state = redis_client.setex(key, timedelta(seconds=3600), data)
        return state
    
    except Exception as error:
        print(f"Error Occured : {error}")
        

# Obtain news data
def get_data(category: str) -> list:
    try:
        # Check data availability in Redis
        data = get_news_data_from_cache(key=category)
        # If Aavailabe serve from cache
        if data is not None:
            print("Data Obtained From Cache")
            data = json.loads(data)
            return data
        else:
            # Get data from API
            data = get_news_from_api(category)

            if len(data)>0:
                print("Data Obtained From API")

                # Add data to cache
                state = put_news_data_to_cache(key=category, value=data)
                if state is True:
                    print("Data Added to Redis")
            return data
    except Exception as error:
        print(f"Error Occured : {error}")




api = NewsApiClient(api_key='30d7eb960aaf452293896183aaf05c55')
news=[]
@app.route('/')
def frontend():
    return render_template("homepage.html")

@app.route("/news/<category>/",methods=["GET","POST"])
def handle_api_call(category):
    data=get_data(category=category)
    global news
    news=data
    return render_template('index.html', news=news)

@app.route("/search/",methods=["GET","POST"])
def search_query():
    query_to_search=request.form.get('query')
    print(query_to_search)
    data=search_data(query_to_search)
    news=data
    
    return render_template("index.html",news=news)



def search_data(query):
    try:
        # Check data availability in Redis
        data = get_news_data_from_cache(key=query)
        
        # If Aavailabe serve from cache
        if data is not None:
            print("Data Obtained From Cache")
            data = json.loads(data)
            return data
        else:
            # Get data from API
            data = search_from_api(query)

            if len(data)>0:
                print("Data Obtained From API")

                # Add data to cache
                state = put_news_data_to_cache(key=query, value=data)
                if state is True:
                    print("Data Added to Redis")
            return data
        
    except Exception as error:
        print(f"Error Occured : {error}")
    


def search_from_api(query):
    news_obj=api.get_everything(q=query)
    articles=news_obj['articles']
    
    data=[]
    for article in articles:
        data.append({"Title":article['title'],
                     "Description":article['description'],
                     "urlToImage":article['urlToImage'],
                     "url":article['url'],
                     "publishedAt":article['publishedAt']
                     })
        
    return data
    


def get_news_from_api(cat):
    news_obj=api.get_top_headlines(country="in",category=cat)
    
    articles=news_obj['articles']
    
    data=[]
    for article in articles:
        data.append({"Title":article['title'],
                     "Description":article['description'],
                     "urlToImage":article['urlToImage'],
                     "url":article['url'],
                     "publishedAt":article['publishedAt']
                     })
        
    return data
    
    
app.run(debug=True)