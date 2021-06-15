import feedparser
from bs4 import BeautifulSoup
import datetime
from operator import itemgetter
from pyshorteners import Shortener
import os

API_KEY = os.getenv("API_KEY_BITLY")
API_USER = os.getenv("API_USER_BITLY")
date_obj = datetime.datetime.now()
s = Shortener(api_key=API_KEY)


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


class TweetPreparion(ParseFeed):

    def __init__(self, url):
        super().__init__(url)
        # self.feed_dict = dict

    def cleaning_link(self):
        new_dictionary = {"TITLE": [], "URL": [], "PUBDATE": []}
        # dictionary = self.feed_dict
        for data in ParseFeed.parse(self):
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
            # students = ('Agric', 'Food', 'AGRIC', 'FOOD', 'agric', 'food')
            # for words in data:
            #     if all(words in new_dictionary["TITLE"] for words in students):
            #
            new_dictionary["TITLE"].append(data["TITLE"])
            new_dictionary["URL"].append(data["URL"])
            # new_dictionary["DESCR"].append(data["DESCR"])
            new_dictionary["PUBDATE"].append(data["PUBDATE"])

        publish_data = sorted([{"TITLE": s, "URL": t, "PUBDATE": l} for s, t, l in
                               zip(new_dictionary["TITLE"], new_dictionary["URL"], new_dictionary["PUBDATE"])],
                              key=itemgetter('PUBDATE'), reverse=True)
        return publish_data

    def creating_data(self):
        dict_input = {"TITLE": [], "URL": [], "HASTAG": [], "PUBDATE": []}
        students = ['Agric', 'Agriculture', 'Food', 'AGRIC', 'AGRICULTURE', 'FOOD', 'agric', 'agricultre', 'food']
        for i in self.cleaning_link():
            for j in students:
                if j in i["TITLE"]:
                    dict_input["TITLE"].append(i["TITLE"])
                    dict_input["URL"].append(i["URL"])
                    dict_input["HASTAG"].append("#foodtech #agritech #blockchain #innovation")
                    dict_input["PUBDATE"].append(i["PUBDATE"])

        final_data = sorted([{"TITLE": s, "URL": t, "HASTAG": l, "PUBDATE": p} for s, t, l,p in
                               zip(dict_input["TITLE"], dict_input["URL"], dict_input["HASTAG"], dict_input["PUBDATE"])],
                              key=itemgetter('PUBDATE'), reverse=True)
        return final_data


feed_food = TweetPreparion("https://news.google.com/rss/search?q=food+blockchain+agriculture+blockchain+when:1d&hl=en-US&gl=US&ceid=US:en")
link_food = feed_food.creating_data()

# class TweetText():
#
#     # def __init__(self, title, url, hashtag):
#     #     self.title = title
#     #     self.url = url
#     #     self.hashtag = hashtag
#
#     def twitter_message(self,  title, url, hashtag):
#         print("Creating message for ", self.title , self.url , self.hashtag)
#         # create_mesage = f"{self.title} at {s.bitly.short(self.url)} {self.hashtag}"
#         create_mesage = f"{self.title} at {self.url} {self.hashtag}"
#         if len(create_mesage) >= 281:
#             print("to loong" , len(create_mesage))
#         else:
#             create_mesage
#         return create_mesage
#
#     def twitter_dict (self):
#         dict_publish = {"TITLE": [],  "PUBDATE": []}
#         hours = 0
#         for a in link_food:
#             hours +=1
#
#             add_time = datetime.timedelta(hours=hours)
#             new_time = date_obj + add_time
#             time_to_publish = datetime.datetime.strftime(new_time, "%H:%M:%S")
#             dict_publish["TITLE"].append(self.twitter_message((a["TITLE"], a["URL"], a["HASTAG"])))
#             dict_publish["PUBDATE"].append(time_to_publish)
#         #
#         final_publish = sorted([{"TITLE": s, "PUBDATE": t} for s, t in
#                              zip(dict_publish["TITLE"], dict_publish["PUBDATE"])],
#                             key=itemgetter('PUBDATE'), reverse=False)
#         return  final_publish


def twitter_message(title, url, hashtag):
    print("Creating message for ",title, url, hashtag)
    create_mesage = f"{title} at {s.bitly.short(url)} {hashtag}"
    ##create_mesage = f"{title} at {url} {hashtag}"
    if len(create_mesage) >= 281:
        print("to loong", len(create_mesage))
    else:
        create_mesage
    return create_mesage


def twitter_dict():
    dict_publish = {"TITLE": [], "PUBDATE": []}
    hours = 30
    for a in link_food:
        hours += 30

        add_time = datetime.timedelta(minutes =hours)
        new_time = date_obj + add_time
        time_to_publish = datetime.datetime.strftime(new_time, "%H:%M:%S")
        dict_publish["TITLE"].append(twitter_message(a["TITLE"], a["URL"], a["HASTAG"]))
        dict_publish["PUBDATE"].append(time_to_publish)
    #
    final_publish = sorted([{"TITLE": s, "PUBDATE": t} for s, t in
                            zip(dict_publish["TITLE"], dict_publish["PUBDATE"])],
                           key=itemgetter('PUBDATE'), reverse=False)
    return final_publish

print(twitter_dict())
###gira una volta al giorno va su un database salve il dict e dice che se e' pubblicato. CLOUD FUNCATION
##o pubsub[tipo canale in cui elabori il messaggio]
