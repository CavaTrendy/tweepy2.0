from config import create_api
import logging
from pyshorteners import Shortener
from feeds_post import food
logging.basicConfig(
    filename='twitter-bot.log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger()

API_KEY = "8d3dc08c8a0d27a88e41a46b14b8c9106fc939c4"
API_USER = "cavatrendy"

s = Shortener(api_key=API_KEY)
def shorten_link(link):
    short_link = s.bitly.short(link)
    return short_link
def twitter_message(title, url):
    hashtag = "#foodtech #agritech #blockchain #innovation"
    print("Creating message for " + title + url + " " + hashtag)
    create_mesage = f"{title} at {url} {hashtag}"
    if len(create_mesage) >= 281:
        print("to loong" + len(create_mesage))
    else:
        create_mesage
    return create_mesage

# for pdata in publish_data:
#     print(len(twitter_message(pdata["TITLE"], shorten_link(pdata["URL"]))))
#     print(twitter_message(pdata["TITLE"], shorten_link(pdata["URL"])))

def post_tweet(event="", context=""):
    api = create_api()
    for pdata in food:
        article = twitter_message(pdata["TITLE"], shorten_link(pdata["URL"]))
    # article = df_diff
    tweet = article.write_tweet()
    try:
        api.update_status(status=tweet)
    except Exception as e:
        logger.error("Error posting tweet", exc_info=True)
        raise e
    logger.info("Tweet successfully posted")


post_tweet()