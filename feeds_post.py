from pyshorteners import Shortener
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

API_KEY = "8d3dc08c8a0d27a88e41a46b14b8c9106fc939c4"
API_USER = "cavatrendy"

s = Shortener(api_key=API_KEY)

# food_url = "http://news.google.com/news?q=food+blockchain&hl=en-US&sort=date&gl=US&num=100&output=rss"
# agriculture_url = "http://news.google.com/news?q=agriculture+blockchain&hl=en-US&sort=date&gl=US&num=100&output=rss"

class ParseFeed():

    def __init__(self, url):
        self.feed_url = url

    def clean(self, html):
        '''
        Get the text from html and do some cleaning
        '''
        soup = BeautifulSoup(html, features="lxml")
        text = soup.get_text()
        text = text.replace('\xa0', ' ')
        return text

    def parse(self):
        '''
        Parse the URL, and print all the details of the news
        '''
        feeds = feedparser.parse(self.feed_url).entries
        dictionary = {"TITLE": [], "URL": [], "DESCR": [], "PUBDATE": []}
        for f in feeds:
            dictionary["TITLE"].append(f.get("title", ""))
            dictionary["URL"].append(f.get("link", ""))
            dictionary["DESCR"].append(self.clean(f.get("description", "")))
            dictionary["PUBDATE"].append(f.get("published", ""))
        new_data = [{"TITLE": s, "URL": t, "DESCR": e, "PUBDATE": l} for s, t, e, l in
                    zip(dictionary["TITLE"], dictionary["URL"], dictionary["DESCR"], dictionary["PUBDATE"])]
        return new_data


feed = ParseFeed("http://news.google.com/news?q=food+blockchain&hl=en-US&sort=date&gl=US&num=100&output=rss")
link_dictionary = feed.parse()



for data in link_dictionary:
    ###imposto la timezone gmt
    tz_GMT = pytz.timezone('GMT')
    date_obj = datetime.now(tz_GMT).strftime("%a, %d %b %Y %H:%M:%S")
    ##pulisco la data di input
    strip_gmt = data["PUBDATE"].rstrip(" GMT")
    # setto uguale le date
    data_pub = datetime.strptime(strip_gmt, "%a, %d %b %Y %H:%M:%S")
    new_date = datetime.strptime(date_obj, "%a, %d %b %Y %H:%M:%S")
    # creo il dizionario per i dati
    new_dictionary = {"TITLE": [], "URL": [], "DESCR": [], "PUBDATE": []}
    # setto la paramatrizzione
    # print((new_date - data_pub).days)
    print((data_pub - new_date ).days)
    if (data_pub - new_date ).days < 7 :
        print("superiorie " + str(data_pub))
        new_dictionary["TITLE"].append(data["TITLE"])
        new_dictionary["URL"].append(data["URL"])
        new_dictionary["DESCR"].append(data["DESCR"])
        new_dictionary["PUBDATE"].append(data["PUBDATE"])

    else:
        print("inferiore")

publish_data = [{"TITLE": s, "URL": t, "DESCR": e, "PUBDATE": l} for s, t, e, l in
            zip(new_dictionary["TITLE"], new_dictionary["URL"], new_dictionary["DESCR"], new_dictionary["PUBDATE"])]

print(publish_data)




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
