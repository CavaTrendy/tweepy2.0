# from feeds_post import TweetPreparion, twitter_dict
# def main():
#     feed_food = TweetPreparion(
#         "https://news.google.com/rss/search?q=food+blockchain+agriculture+blockchain+when:1d&hl=en-US&gl=US&ceid=US:en")
#     link_food = feed_food.creating_data()
#     twitter_dict(link_food)
#     print(twitter_dict(link_food))
import time
from feeds_post import main_post
from tweet_post import main_posting


def main():
    main_post
    time.sleep(30)
    main_posting


if __name__ == '__main__':
    main()