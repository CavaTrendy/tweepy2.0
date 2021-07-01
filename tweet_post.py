import tweepy
import os
from feeds_post import main_post
import time
import datetime
import itertools

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
post = main_post()


def twitter_message(text):
    return api.update_status(text)


while len(post) > 0:
    print("Still elements? ", len(post))
    for item in post:
        posting = twitter_message(item["TITLE"])
        # posting = item["TITLE"]
        time.sleep(3600)

        element = post.remove(item)
        print('The popped element is:', element)
        print('The dictionary is:', post)
    if len(post) == 0 :
        print("Still elements? ", len(post))
        break


