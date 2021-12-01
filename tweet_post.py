import tweepy
import os
from feeds_post import main_post
from

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

def calculate_posting_time(time):
    to_time = 0
    if time in (1, 2, 3, 4):
        to_time = time * 2000
    else:
        to_time = 2000
    return to_time


def main_posting():
    print(post)
    while len(post) > 0:
        print("Still elements? ", len(post))
        for item in post:
            # calculate_posting_time(len(post))
            posting = twitter_message(item["TITLE"])
            # posting = item["TITLE"]
            print(calculate_posting_time(len(post)))
            element = post.remove(item)
            print('The popped element is:', element)
            print('The dictionary is:', post)
    if len(post) == 0:
        print("No Elements ", len(post))
    return posting

