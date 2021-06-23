import tweepy
import os
from feeds_post import main_post
import time
import datetime

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# def twitter_post ():
#     post = main_post()
#     for message in post:
#         print(message["TITLE"])
#         api.update_status(message["TITLE"])
#         time.sleep(1800)





if __name__ == '__main__':
    post = main_post()
    for message in post:
        print(message["TITLE"])
        api.update_status(message["TITLE"])
        time.sleep(1800)