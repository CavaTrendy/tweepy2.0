import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
from operator import itemgetter


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

def cleaning_link(dictionary):
    new_dictionary = {"TITLE": [], "URL": [],  "PUBDATE": []}
    for data in dictionary:
        # ###imposto la timezone gmt
        # tz_GMT = pytz.timezone('GMT')
        # date_obj = datetime.now(tz_GMT).strftime("%a, %d %b %Y %H:%M:%S")
        # ##pulisco la data di input
        # strip_gmt = data["PUBDATE"].rstrip(" GMT")
        # # setto uguale le date
        # data_pub = datetime.strptime(strip_gmt, "%a, %d %b %Y %H:%M:%S")
        # new_date = datetime.strptime(date_obj, "%a, %d %b %Y %H:%M:%S")
        # if (new_date - data_pub).days <= 1 :
            # print("superiorie " + str(data_pub))
        new_dictionary["TITLE"].append(data["TITLE"])
        new_dictionary["URL"].append(data["URL"])
        # new_dictionary["DESCR"].append(data["DESCR"])
        new_dictionary["PUBDATE"].append(data["PUBDATE"])

    publish_data = sorted([{"TITLE": s, "URL": t, "PUBDATE": l} for s, t, l in
                           zip(new_dictionary["TITLE"], new_dictionary["URL"], new_dictionary["PUBDATE"])],
                          key=itemgetter('PUBDATE'), reverse=True)
    return publish_data


# feed_food = ParseFeed("http://news.google.com/news?q=food+blockchain&hl=en-US&sort=date&gl=US&num=100&output=rss")
feed_food = ParseFeed("https://news.google.com/rss/search?q=food+blockchain+agriculture+blockchain+when:1d&hl=en-US&gl=US&ceid=US:en")
# feed_agriculture = ParseFeed("http://news.google.com/news?q=agriculture+blockchain&hl=en-US&sort=date&gl=US&num=100&output=rss")
link_food= feed_food.parse()
# link_agri= feed_agriculture.parse()

food = cleaning_link(link_food)
# agri = cleaning_link(link_agri)
print(food)
# print(agri)