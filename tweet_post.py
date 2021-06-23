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
post = main_post()
len_post = len(post)


def twitter_check():

    twitter_title = {"TITLE": []}
    for status in tweepy.Cursor(api.user_timeline, screen_name='@CavaTrendy', tweet_mode="extended").items(len_post + 1):
        title_redux = status.full_text[:150]
        print(
            title_redux
        )
        twitter_title["TITLE"].append(title_redux)
    print(twitter_title)

    for message in post:
        if message["TITLE"][:150] in twitter_title.items():
            print(message["TITLE"][:150])
            print("in")
        else:
            print("not")
            print(message["TITLE"])
            new_message = message["TITLE"]
    return new_message

def twitter_message(text):
    return api.update_status(text)

print(twitter_check())
count = 0

while count <= len_post:
    try:
        twitter_message(twitter_check())
        count +=1

        print(count)
    except tweepy.error.TweepError:
        print("error")


# tweet = client.user_timeline(id=self.client_id, count=1)[0]
# print(tweet.text)

# if __name__ == '__main__':
#     post = main_post()
#     for message in post:
#         print(message["TITLE"])
#         api.update_status(message["TITLE"])
#         # time.sleep(1800)
