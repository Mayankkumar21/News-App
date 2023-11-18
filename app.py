from flask import Flask, abort, jsonify,render_template,request,redirect, url_for
from newsapi import NewsApiClient
app=Flask(__name__)


api = NewsApiClient(api_key='30d7eb960aaf452293896183aaf05c55')
#api key- 30d7eb960aaf452293896183aaf05c55
news=[]
@app.route('/')
def frontend():
    return render_template('index.html',news=news)

@app.route("/news")
def get_headlines():
    news_obj=api.get_top_headlines(country="in",category='sports')
    return jsonify({
        "headlines":news_obj.title,
        "Description":news_obj.description,
        "publishedAt":news_obj.publishedAt,
        
    })
    
    
    
    
app.run(debug=True)