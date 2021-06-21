import tweepy
import os
from feeds_post import TweetPreparion, twitter_dict
import time
import datetime

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def twitter_post ():
    dict_published = {"TITLE": [], "REALPUBDATE": []}
    feed_food = TweetPreparion(
        "https://news.google.com/rss/search?q=food+blockchain+agriculture+blockchain+when:1d&hl=en-US&gl=US&ceid=US:en")
    link_food = feed_food.creating_data()

    while twitter_dict(link_food) != dict_published:
        for message in twitter_dict(link_food):
            api.update_status(message)
            time_published = datetime.datetime.timestamp(datetime.now())
            dict_published["TITLE"].append(message["TITLE"])
            dict_published["REALPUBDATE"].append(time_published)
            time.sleep(1800)