import sys
import tweepy
import os
import csv
from feeds_post import main_post

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

with open('db.csv', newline='') as db_file:
    reader = csv.DictReader(db_file)
    for row in reader:
        if row["POSTED"] == "YES":
            print("posted")
        else:
            print("not_posted")
            while len(post) > 0:
                print("Still elements? ", len(post))
                for item in post:
                    calculate_posting_time(len(post))
                    # posting = twitter_message(item["TITLE"])
                    posting = item["TITLE"]
                    print(calculate_posting_time(len(post)))
                    with open('db.csv', 'w') as csv_writting:
                        fieldnames = ['TWEET', "POSTED"]
                        writer = csv.DictWriter(csv_writting, fieldnames=fieldnames)
                        writer.writeheader()
                        for p in main_post():
                            writer.writerow({'TWEET': p["TITLE"], "POSTED": "YES"})

                    element = post.remove(item)
                    print('The popped element is:', element)
                    print('The dictionary is:', post)
            if len(post) == 0:
                print("Still elements? ", len(post))
                sys.exit()
                break
