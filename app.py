# to activate env write this in terminal (comand prompt) env\Scripts\activate.bat
from flask import Flask, render_template, url_for, request, Response
from flask_socketio import SocketIO, emit
from asyncio import sleep
import snscrape.modules.twitter as sntwitter
from function.scrapeTweet import get_query
from function.scrape import twitter_scrape as ts
import time
import pandas as pd
from selenium import webdriver
from IPython.display import display
import math
import os
import requests
import json
# from function.twitter_summary.summary import summarise
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']
socketio = SocketIO(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        hashtag = request.form['hashtag']
        number_of_tweets = request.form['number_of_tweets']
        tweet_date_early = request.form['tweet_date_early']
        tweet_date_later = request.form['tweet_date_later']
        tweets = get_query(hashtag, number_of_tweets, tweet_date_early, tweet_date_later)
        return render_template('index.html', hashtag=hashtag, tweets=tweets)
    else:
        news_df = pd.read_csv('static/data/news.csv')
        news_hashtags = news_df['hashtag'].unique().tolist()
        return render_template('index.html', news_hashtags=news_hashtags)
    # return render_template('index.html')
    # return render_template('index.html')

@app.route('/about_us', methods=['GET'])
def progress():
    return render_template('about_us.html')

@socketio.on('formSubmit')
def handle_form_submit(data):
    # url = "https://apps.beam.cloud/52k08"
    # payload = {"text": "This is Beam!"}
    # headers = {
    # "Accept": "/",
    # "Accept-Encoding": "gzip, deflate",
    # "Authorization": "Basic N2VkMWE1ZjY5ZjhiYzZjYzdlMzE0ZWVmMDc2YTIyNGI6YmI0NTY5OTBkYzI2MzNlODc2NzMzZTRkZDRiNGIwMTQ=",
    # "Connection": "keep-alive",
    # "Content-Type": "application/json"
    # }

    # response = requests.request("POST", url, 
    # headers=headers,
    # data=json.dumps(payload)
    # )

    # print(response.json())
    # -----------------------------------------------
    hashtag = data['hashtag']
    n_tweet = data['n_tweets']
    if n_tweet is None:
        n_tweets = 1000
    else:
        n_tweets = int(n_tweet)
    tweet_date_early = data['tweet_date_early']
    tweet_date_later = data['tweet_date_later']
    snscrape = data['snscrape']
    selenium = data['selenium']
    socketid = data['socketid']
    print('form submited')
    
    query = get_query(hashtag, early_tweet_date=tweet_date_early, later_tweet_date=tweet_date_later)
    
    # URL = "https://twitter.com/i/flow/login"
    # WINDOW_SIZE = "1920,1080" # for starting with no window
    # options = webdriver.ChromeOptions()
    # options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # options.add_experimental_option("detach", True)
    # # options.add_argument("start-maximized")
    # options.add_argument("disable-extensions")
    # options.add_argument("--window-size=%s" % WINDOW_SIZE) # for starting with no window
    # options.add_argument("headless") # for starting with no window
    # options.add_argument('log-level=3')
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--no-sandbox")
    # PATH = "function\scrape\driver\chromedriver.exe"
    
    # driver = webdriver.Chrome(options=options, executable_path=os.environ.get("CHROMEDRIVER_PATH"))
    # # driver = webdriver.Chrome(options=options, executable_path=PATH) to use localy
    
    # if selenium:
    #     # driver = ts.get_driver
    #     socketio.emit("update progress", 2, to=socketid)
    #     socketio.emit("taskName", "log in..", to=socketid)
    #     ts.login(driver, URL)
    #     time.sleep(3)
    #     socketio.emit("update progress", 5, to=socketid)
    #     socketio.emit("taskName", "search query..", to=socketid)
        
    #     ts.search(query, driver)
    #     time.sleep(3)
        
    #     links = []
    
    #     socketio.emit("taskName", "searching through top tweets..", to=socketid)
    #     print("searching through top tweets..")
    #     y = 0
    #     new_height = 0
    #     scroll_pause_time = 0.8
    #     progress = 0
    #     while True:
    #         links, new_height, y  = ts.scrapeTweetLink(driver, links, y, scroll_pause_time)
    #         socketio.emit("update progress", 5+(progress/4), to=socketid)
    #         progress +=1
    #         if(y>new_height):
    #             break
    #         # if(progress>5): 
    #         #     break
    #         if(progress>100): 
    #             break
            
    #     socketio.emit("update progress", 25, to=socketid)
    
    #     socketio.emit("taskName", "searching through latest tweets..", to=socketid)
    #     ts.clickLastest(driver)
    #     time.sleep(3)
    #     print("searching through latest tweets..")
    #     y = 0
    #     new_height = 0
    #     scroll_pause_time = 0.5
    #     for i in range(0,n_tweets):
    #         links, new_height, y = ts.scrapeTweetLink(driver, links, y, scroll_pause_time)
    #         socketio.emit("update progress", 25+(i*25/n_tweets), to=socketid)
    #         if(y>new_height):
    #             break
    #     print("sort links")
    #     links = list(dict.fromkeys(links))
    #     links[:] = [url for url in links if "status" in url]
        
    #     df = pd.DataFrame(columns=['date','content','username','like_count','retweet_count','quote_count','bookmark_count', 'link'])
    
    #     socketio.emit("taskName", "scraping..", to=socketid)
    #     print("scraping links")
    #     for i, link in enumerate(links):
    #         socketio.emit("update progress", 50+(i*25/len(links)), to=socketid)
    #         try:
    #             df = ts.searchLink(driver, link, df)
    #         except: continue
    #     df['hashtag'] = hashtag

    # tweets = list(df['content'])
    # df.to_csv('test.csv')

    if snscrape:
        socketio.emit("update progress", 0, to=socketid)
        tweets = []
        socketio.emit("taskName", "scraping top tweets..", to=socketid)
        query_min_likes = query + " min_faves:20"
        scraper = sntwitter.TwitterSearchScraper(query_min_likes)
        num_scraped = 0
        for i, tweet in enumerate(scraper.get_items()):
            URL = "https://twitter.com/{0}/status/{1}".format(tweet.user.username,tweet.id)
            data = [
                tweet.date,
                tweet.id,
                tweet.content,
                tweet.user.username,
                tweet.likeCount,
                tweet.retweetCount,
                URL
            ]
            tweets.append(data)
            socketio.emit("update progress", (i/(n_tweets/2))*30, to=socketid)
            if i >= math.ceil(n_tweets/2):
                num_scraped = i
                break
            
        socketio.emit("taskName", "scraping tweets..", to=socketid)
        scraper = sntwitter.TwitterSearchScraper(query)
        for i, tweet in enumerate(scraper.get_items()):
            URL = "https://twitter.com/{0}/status/{1}".format(tweet.user.username,tweet.id)
            data = [
                tweet.date,
                tweet.id,
                tweet.content,
                tweet.user.username,
                tweet.likeCount,
                tweet.retweetCount,
                URL
            ]
            tweets.append(data)
            socketio.emit("update progress", 30+((i/(n_tweets-num_scraped))*60), to=socketid)
            if i >= n_tweets-num_scraped:
                break
            
        df = pd.DataFrame(tweets, columns=['date', 'id', 'content','username', 'like_count', 'retweet_count', "link"])
        df['hashtag'] = hashtag
        
    socketio.emit("taskName", "generating summary..", to=socketid)
    # summary = summarise(df, with_cluster=True)
    # socketio.emit("aiSum", summary, to=socketid)
    socketio.emit("update progress", 75, to=socketid)
    final_df = df.sort_values(['retweet_count'], ascending=[False])
    final_df = final_df.head(5)

    # display(final_df['retweet_count'])

    embedded_links = list(final_df['link'])
    socketio.emit("taskName", "getting embedded tweets..", to=socketid)
    socketio.emit("update progress", 85, to=socketid)
    embeded_tweets = []
    for link in embedded_links:
        embeded_tweets.append('<blockquote class="twitter-tweet"><a href="{}"></a></blockquote>'.format(link))
    final_retweets = list(final_df['retweet_count'])
    final_likes = list(final_df['like_count'])

    # socketio.emit("createTable", {'tweetList':tweets})

    socketio.emit("createEmbeded", {'embededHtml':embeded_tweets, 'reTweetCount': final_retweets, 'likeCount': final_likes}, to=socketid)
    socketio.emit("taskName", "DONE", to=socketid)
    socketio.emit("update progress", 100, to=socketid)
    
    
@socketio.on('quickSearch')
def quickSearch(data):
    hashtag = data['hashtag']
    socketid = data['socketid']
    
    # WINDOW_SIZE = "1920,1080" # for starting with no window
    # options = webdriver.ChromeOptions()
    # options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # options.add_experimental_option("detach", True)
    # options.add_argument("disable-extensions")
    # options.add_argument("--window-size=%s" % WINDOW_SIZE) # for starting with no window
    # options.add_argument("headless") # for starting with no window
    # options.add_argument('log-level=3')
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--no-sandbox")
    # PATH = "function\scrape\driver\chromedriver.exe"
    
    # driver = webdriver.Chrome(options=options, executable_path=os.environ.get("CHROMEDRIVER_PATH"))
    # # driver = webdriver.Chrome(options=options, executable_path=PATH) #to use localy
    
    socketio.emit("taskName", "getting tweets..", to=socketid)
    socketio.emit("update progress", 20, to=socketid)
    
    news_df = pd.read_csv('static/data/news.csv')
    hashtag_df = news_df[news_df['hashtag'] == hashtag].drop_duplicates(subset=['content'], keep='first')
    topFive_df = hashtag_df.sort_values(['retweet_count'], ascending=[False])
    topFive_df = topFive_df.head(5)
    embedded_links = list(topFive_df['tweet_link'])
    socketio.emit("taskName", "getting embeded tweets..", to=socketid)
    socketio.emit("update progress", 50, to=socketid)
    # embeded_tweets = ts.getEmbeddedTweet(driver, embedded_links)
    embeded_tweets = []
    for link in embedded_links:
        embeded_tweets.append('<blockquote class="twitter-tweet"><a href="{}"></a></blockquote>'.format(link))
    final_retweets = list(topFive_df['retweet_count'])
    final_likes = list(topFive_df['like_count'])
    socketio.emit("taskName", "DONE", to=socketid)
    socketio.emit("update progress", 100, to=socketid)
    socketio.emit("createEmbeded", {'embededHtml':embeded_tweets, 'reTweetCount': final_retweets, 'likeCount': final_likes}, to=socketid)
    
if __name__ == "__main__":
    socketio.run(app=app, debug=True)