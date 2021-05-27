from pyshorteners import Shortener
import feedparser
from pprint import pprint
from bs4 import BeautifulSoup

food_url = "http://news.google.com/news?q=food+blockchain&hl=en-US&sort=date&gl=US&num=100&output=rss"
agriculture_url = "http://news.google.com/news?q=agriculture+blockchain&hl=en-US&sort=date&gl=US&num=100&output=rss"


class ParseFeed():

    def __init__(self, url):
        self.feed_url = url

    def clean(self, html):
        '''
        Get the text from html and do some cleaning
        '''
        soup = BeautifulSoup(html)
        text = soup.get_text()
        text = text.replace('\xa0', ' ')
        return text

    def parse(self):
        '''
        Parse the URL, and print all the details of the news
        '''
        feeds = feedparser.parse(self.feed_url).entries
        for f in feeds:
            pprint({
                'Description': self.clean(f.get("description", "")),
                'Published Date': f.get("published", ""),
                'Title': f.get("title", ""),
                'Url': f.get("link", "")
            })


feed = ParseFeed(food_url)
feed.parse()
# #create the df
# food = result_words("Food Blockchain")
# agriculture = result_words("Agriculture Blockchain")
# #col of interest
# col_list = ["title", "link"]
# #df cleaning
# df_diff = pd.concat([food, agriculture]).drop_duplicates(keep=False)
# df_diff = df_diff[col_list]
#reduce the link size
API_KEY = "8d3dc08c8a0d27a88e41a46b14b8c9106fc939c4"
API_USER = "cavatrendy"

s = Shortener(api_key=API_KEY)


# for l in df_diff.get("link"):
#     try:
#         link_to_short.append(s.bitly.short(l))
#         print(l)
#     except:
#         print("Not added " + l)
#
# title_to_short = []
# for t in  df_diff.get("title"):
#     title_to_short.append(t)
#
# def twitter_message (title, url):
#     print("Creating message for" + title + url)
#     create_mesage = f"{title} at {url}"
#     return create_mesage
#
# for title, link in zip(title_to_short,link_to_short):
#     a = twitter_message(title, link)
#     print (a)
