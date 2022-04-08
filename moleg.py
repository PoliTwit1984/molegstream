from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import tweepy
from PIL import Image, ImageDraw, ImageFont
from wordcloud import ImageColorGenerator, WordCloud
import numpy as np
import math
from collections import Counter

import config
from twit import makeitastring

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
bearer_token = config.bearer_token
api = tweepy.API(auth)
client = tweepy.Client(bearer_token=config.bearer_token)


class MoLegTwitter:
    def __init__(self):
        self.query = "moleg OR mogov OR mosenate OR mosen"
        # self.query = "moleg"
        self.hours_delta = 72
        self.max_cloud_words = 100

    def __start_time(self, hours):
        x = datetime.now()
        past_time = x - timedelta(hours=self.hours_delta)

        return past_time

    def __num_tweets_arguments(self, total_tweets):
        dict = {}

        total_tweets = int(math.ceil(total_tweets / 100.0)) * 100
        limit = round(int(total_tweets / 100), 0)

        dict["max_results"] = 100
        dict["limit"] = limit

        return dict

    def get_most_common(self, list, num_items):
        Counters_found = Counter(list)
        most_occur = Counters_found.most_common(num_items)

        return most_occur

    def get_hashtag_cloud(self, hashtags):
        mo_mask = np.array(Image.open("mo.jpg"))
        hashtags = makeitastring(hashtags)

        cloud = WordCloud(
            scale=3,
            max_words=1000,
            colormap="RdYlGn",
            mask=mo_mask,
            background_color="black",
            collocations=True,
        ).generate_from_text(hashtags)
        plt.figure(figsize=(5, 5))
        plt.title("#moleg", fontsize=48, color="white")
        plt.imshow(cloud)
        plt.axis("off")
        cloud = cloud.to_file("hashtags.png")
        # my_image = Image.open("cloud.png")

    def get_hashtags(self, filename="none", number_hashtags=200):
        htag_list = []
        tweet_arguments = self.__num_tweets_arguments(number_hashtags)
        max_results = tweet_arguments.get("max_results")
        limit = tweet_arguments.get("limit")

        i = 0

        for response in tweepy.Paginator(
            client.search_recent_tweets,
            self.query,
            tweet_fields=["entities", "created_at"],
            max_results=max_results,
            limit=limit,
        ):

            i = i + 1
            tweets = response.data
            for tweet in tweets:
                print(tweet.created_at)
                i = i + 1
                print(i)
                try:
                    if tweet["entities"]["hashtags"] is not None:
                        # print(
                        #     f"created at {tweet.created_at} - {tweet.text} - result - {i}"
                        # )
                        for h in tweet["entities"]["hashtags"]:
                            htag = h.get("tag")
                            htag = htag.lower()
                            if htag not in ("moleg", "mogov", "mosenate", "mosen"):
                                htag_list.append(htag)

                except:
                    pass

        filename = filename.lower()
        if filename != "none":
            with open(filename, "w", encoding="utf8") as f:
                f.write(makeitastring(htag_list))
                f.write("\n")

        return htag_list


m = MoLegTwitter()
hashtags = m.get_hashtags(filename="hashtags-moleg.txt", number_hashtags=100)
total = m.get_most_common(hashtags, 15)
print(total)
print(type(total))
