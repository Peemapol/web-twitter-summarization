import pandas as pd
from datetime import datetime, timedelta
import snscrape.modules.twitter as sntwitter
from IPython.display import display

def get_tomorrow_and_yesterday(day):
    tomorrow = datetime.strftime(datetime.strptime(day, '%Y-%m-%d').date() + timedelta(1), '%Y-%m-%d')
    yesterday = datetime.strftime(datetime.strptime(day, '%Y-%m-%d').date() - timedelta(1), '%Y-%m-%d')
    return tomorrow, yesterday

def get_query(hashtag, early_tweet_date, later_tweet_date):
    if(early_tweet_date == None or later_tweet_date == ''):
        query = hashtag

    elif(early_tweet_date == later_tweet_date):
        later_day, earlier_day = get_tomorrow_and_yesterday(early_tweet_date)
        query = '(' + hashtag + ') lang:th until:' + later_day + ' since:' + earlier_day

    else:
        query = '(' + hashtag + ') lang:th until:' + later_tweet_date + ' since:' + early_tweet_date

    return query

def main():
    hashtag = 'Beam'
    n_tweets = 5

    scraper = sntwitter.TwitterSearchScraper(hashtag)

    tweets = []

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
        if i >= n_tweets-1:
            break
    df = pd.DataFrame(tweets, columns=['date', 'id', 'content','username', 'like_count', 'retweet_count', "tweet_link"])
    df['hashtag'] = hashtag
    display(df)
    links = df['tweet_link'].tolist()
    print(links)
    

if __name__ == '__main__':
    main()