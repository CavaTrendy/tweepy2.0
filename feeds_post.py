import feedparser
from bs4 import BeautifulSoup
import datetime
from operator import itemgetter
from pyshorteners import Shortener
import os

API_TINY = os.getenv("API_KEY_TINY")

date_obj = datetime.datetime.now()
s = Shortener(api_key= API_TINY)

def twitter_message(title, url, hashtag):
    # print("Creating message for ", title, url, hashtag)
    message = f"{title} at {s.tinyurl.short(url)} {hashtag}"

    if len(title) >= 200:
        title_redux = title[:150]
        print("title_redux")
        # create_mesage = f"{title_redux} at {s.tinyurl.short(url)} {hashtag}"
        message = f"{title_redux} at {s.tinyurl.short(url)} {hashtag}"
        print(message)
    else:
        message
    return message

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

    def cleaning_link(self):
        new_dictionary = {"TITLE": [], "URL": [], "PUBDATE": []}
        for data in ParseFeed.parse(self):
            # ###imposto la timezone gmt
            # tz_GMT = pytz.timezone('GMT')
            # date_obj = datetime.now(tz_GMT).strftime("%a, %d %b %Y %H:%M:%S")
            # ##pulisco la data di input
            # # strip_gmt = data["PUBDATE"].rstrip(" GMT")
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


    def cleaning_double(self):
        dict_output = {"TITLE": [], "URL": [], "HASTAG": [], "PUBDATE": []}
        for link in self.creating_data():
            print(link["TITLE"])
            if link["TITLE"] not in dict_output["TITLE"]:
                dict_output["TITLE"].append(link["TITLE"])
                dict_output["URL"].append(link["URL"])
                dict_output["HASTAG"].append(link["HASTAG"])
                dict_output["PUBDATE"].append(link["PUBDATE"])

        final_output = sorted([{"TITLE": s, "URL": t, "HASTAG": l, "PUBDATE": p} for s, t, l, p in
                             zip(dict_output["TITLE"], dict_output["URL"], dict_output["HASTAG"], dict_output["PUBDATE"])],
                            key=itemgetter('PUBDATE'), reverse=True)
        return final_output



feed_food = TweetPreparion("https://news.google.com/rss/search?q=food+blockchain+agriculture+blockchain+when:1d&hl=en-US&gl=US&ceid=US:en")
link_food = feed_food.creating_data()
link = feed_food.cleaning_double()
print(link)
print(link_food)
# dict_output = {"TITLE": [], "URL": [], "HASTAG": [], "PUBDATE": []}
# for link in link_food:
#     print(link["TITLE"])
#     if link["TITLE"] not in dict_output["TITLE"]:
#         dict_output["TITLE"].append(link["TITLE"])
#         dict_output["URL"].append(link["URL"])
#         dict_output["HASTAG"].append(link["HASTAG"])
#         dict_output["PUBDATE"].append(link["PUBDATE"])
#
# print (dict_output)
# for d in l:
#     if d not in l2:
#         l2.append(d)



# def twitter_dict(dictionary):
#     dict_publish = {"TITLE": [], "PUBDATE": []}
#     hours = 30
#     for a in dictionary:
#         hours += 30
#         add_time = datetime.timedelta(minutes =hours)
#         new_time = date_obj + add_time
#         time_to_publish = datetime.datetime.strftime(new_time, "%H:%M:%S")
#         dict_publish["TITLE"].append(twitter_message(a["TITLE"], a["URL"], a["HASTAG"]))
#         dict_publish["PUBDATE"].append(time_to_publish)
#     final_publish = sorted([{"TITLE": s, "PUBDATE": t} for s, t in
#                             zip(dict_publish["TITLE"], dict_publish["PUBDATE"])],
#                            key=itemgetter('PUBDATE'), reverse=False)
#     return final_publish


# def main():
#     feed_food = TweetPreparion(
#         "https://news.google.com/rss/search?q=food+blockchain+agriculture+blockchain+when:1d&hl=en-US&gl=US&ceid=US:en")
#     link_food = feed_food.creating_data()
#     twitter_dict(link_food)
#     return print(twitter_dict(link_food))


# if __name__ == '__main__':
#     main()