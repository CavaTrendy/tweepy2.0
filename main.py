import tweepy
import logging
import os

logger = logging.getLogger()
# Authenticate to Twitter
auth = tweepy.OAuthHandler("CaxSsJbXHznHpCI2WumkkRB1i", "AMmE1tnSamoysenaOPpOhnWBskqQuMKt4ZB4ZZInVQ9sLhZWEa")
auth.set_access_token("1217715247798198273-qgisV64jPl3hBZT56t5dRCJBYYgkjj", "WqR3gnjBqyDrhr8SIvhvI5yHewAEkplTcoTI6gedbI3PC")

# Create API object

api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)
# Create a tweet
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
# api.update_status("Hello Tweepy")
timeline = api.home_timeline()
for tweet in timeline:
    print(f"{tweet.user.name} said {tweet.text}")