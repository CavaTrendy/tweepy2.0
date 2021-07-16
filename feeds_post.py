import sys

import feedparser
import b
from bs4 import BeautifulSoup
import datetime
from operator import itemgetter
from pyshorteners import Shortener
import os
import csv

API_TINY = os.getenv("API_KEY_TINY")

date_obj = datetime.datetime.now()
s = Shortener(api_key=API_TINY)


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

        final_data = sorted([{"TITLE": s, "URL": t, "HASTAG": l, "PUBDATE": p} for s, t, l, p in
                             zip(dict_input["TITLE"], dict_input["URL"], dict_input["HASTAG"], dict_input["PUBDATE"])],
                            key=itemgetter('PUBDATE'), reverse=True)
        return final_data

    def cleaning_double(self):
        dict_output = {"TITLE": [], "URL": [], "HASTAG": [], "PUBDATE": []}
        for link in self.creating_data():
            # print(link["TITLE"])
            if link["TITLE"] not in dict_output["TITLE"] or link["URL"] not in dict_output["URL"]:
                dict_output["TITLE"].append(link["TITLE"])
                dict_output["URL"].append(link["URL"])
                dict_output["HASTAG"].append(link["HASTAG"])
                dict_output["PUBDATE"].append(link["PUBDATE"])

        final_output = sorted([{"TITLE": s, "URL": t, "HASTAG": l, "PUBDATE": p} for s, t, l, p in
                               zip(dict_output["TITLE"], dict_output["URL"], dict_output["HASTAG"],
                                   dict_output["PUBDATE"])],
                              key=itemgetter('PUBDATE'), reverse=True)
        return final_output


def twitter_message(title, url, hashtag):
    # print("Creating message for ", title, url, hashtag)
    title_clean = title.replace('.', '')
    # message = f"{title_clean} at {s.tinyurl.short(url)} {hashtag}"
    message = f"{title_clean} at {url} {hashtag}"

    if len(title) >= 200:
        title_redux = title_clean[:150]
        # message = f"{title_redux} at {s.tinyurl.short(url)} {hashtag}"
        message = f"{title_clean} at {url} {hashtag}"
    else:
        message
    return message


def twitter_dict(dictionary):
    dict_publish = {"TITLE": []}
    for a in dictionary:
        dict_publish["TITLE"].append(twitter_message(a["TITLE"], a["URL"], a["HASTAG"]))

    final_publish = [{"TITLE": s} for s in dict_publish["TITLE"]]
    return final_publish


def main_post():
    feed_food = TweetPreparion(
        "https://news.google.com/rss/search?q=food+blockchain+agriculture+blockchain+when:1d&hl=en-US&gl=US&ceid=US:en")
    link_food = feed_food.cleaning_double()
    post = twitter_dict(link_food)
    try:
        with open('db.csv', newline='') as db_file:
            reader = csv.DictReader(db_file)
            for row in reader:
                if row["POSTED"] == "YES":
                    print("posted")
                else:
                    print("not_posted")
                    with open('db.csv', 'w', newline='') as csv_file:
                        fieldnames = ['TWEET', "POSTED"]
                        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        writer.writeheader()
                        for p in main_post():
                            writer.writerow({'TWEET': p["TITLE"], "POSTED": ""})
    except FileNotFoundError:
        with open('db.csv', 'w', newline='') as csv_file:
            fieldnames = ['TWEET', "POSTED"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for p in main_post():
                writer.writerow({'TWEET': p["TITLE"], "POSTED": ""})
    return post




