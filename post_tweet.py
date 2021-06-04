from config import create_api
import logging

from feeds_post import food
logging.basicConfig(
    filename='twitter-bot.log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger()


# for pdata in publish_data:
#     print(len(twitter_message(pdata["TITLE"], shorten_link(pdata["URL"]))))
#     print(twitter_message(pdata["TITLE"], shorten_link(pdata["URL"])))

def post_tweet(event="", context=""):
    api = create_api()

    # article = df_diff
    tweet = article.write_tweet()
    try:
        api.update_status(status=tweet)
    except Exception as e:
        logger.error("Error posting tweet", exc_info=True)
        raise e
    logger.info("Tweet successfully posted")


post_tweet()