import json
import math
from collections import Counter
from datetime import datetime, timedelta
from re import U

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import tweepy
from PIL import Image, ImageDraw, ImageFont
from tabulate import tabulate
import plotly.graph_objects as go

import config

# from twit import makeitastring
# from wordcloud import ImageColorGenerator, WordCloud

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
bearer_token = config.bearer_token
api = tweepy.API(auth)
client = tweepy.Client(
    bearer_token=config.bearer_token,
    consumer_key=config.consumer_key,
    consumer_secret=config.consumer_secret,
    access_token=config.dat,
    access_token_secret=config.das,
)


class MoLegTwitter:

    TOTAL_RESULTS = 1000

    def __init__(self):
        # self.query = "(moleg OR mogov OR mosenate OR mosen) -is:retweet"
        self.query = "moleg -is:retweet"
        self.hours_delta = 24
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

    def hydrate_tweets(self):

        response = tweepy.Paginator(
            client.search_recent_tweets,
            self.query,
            tweet_fields=[
                "attachments",
                "author_id",
                "context_annotations",
                "conversation_id",
                "created_at",
                "entities",
                "geo,id",
                "in_reply_to_user_id",
                "lang",
                "possibly_sensitive",
                "public_metrics",
                "referenced_tweets",
                "reply_settings",
                "source",
                "text",
                "withheld",
            ],
            user_fields=[
                "created_at",
                "description",
                "entities,id",
                "location",
                "name",
                "pinned_tweet_id",
                "profile_image_url",
                "protected,public_metrics",
                "url",
                "username",
                "verified",
                "withheld",
            ],
            expansions=[
                "attachments.poll_ids",
                "attachments.media_keys",
                "author_id",
                "geo.place_id",
                "in_reply_to_user_id",
                "referenced_tweets.id",
                "entities.mentions.username",
                "referenced_tweets.id.author_id",
            ],
            media_fields=[
                "duration_ms",
                "height",
                "media_key",
                "preview_image_url",
                "promoted_metrics",
                "public_metrics",
                "type,url",
            ],
            place_fields=[
                "contained_within,country",
                "country_code",
                "full_name",
                "geo,id",
                "name",
                "place_type",
            ],
            poll_fields=[
                "duration_minutes",
                "end_datetime",
                "id",
                "options",
                "voting_status",
            ],
            max_results=100,
        ).flatten(limit=self.TOTAL_RESULTS)

        return response

    def get_most_common(self, list, num_items):
        Counters_found = Counter(list)
        most_occur = Counters_found.most_common(num_items)
        return most_occur

    def makeitastring(self, wannabestring):
        convertedstring = ",".join(map(str, wannabestring))
        return convertedstring

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

    def get_hashtags(self, data):

        hashtag_list = []
        for tweet in data:
            try:
                h = tweet["entities"]
                h = h.get("hashtags")
                if h:
                    for index in range(0, len(h)):

                        if h[index].get("tag").lower() not in (
                            "moleg",
                            "mogov",
                            "mosenate",
                            "mosen",
                        ):
                            hashtag_list.append("#" + h[index].get("tag"))

            except:
                pass

        return hashtag_list

    def get_mentions(self, data):

        mentions_list = []
        for tweet in data:
            try:
                m = tweet["entities"]
                m = m.get("mentions")

                if m:
                    for index in range(0, len(m)):

                        mentions_list.append("@" + m[index].get("username"))

            except:
                pass

        return mentions_list

    def get_my_mentions(self, id):

        mention_tweets = []
        mention_row = []
        response = tweepy.Paginator(
            client.get_users_mentions,
            id=config.dingersid,
            tweet_fields=["created_at"],
        ).flatten(limit=300)

        for tweet in response:
            mention_row = [tweet.created_at, tweet.text]
            mention_tweets.append(mention_row)

        return mention_tweets

    def get_my_moleg_mentions(self, data):
        tweet_list = []

        for hashtags in data:
            try:
                m = hashtags["entities"]
                m = m.get("hashtags")
                if m:
                    for index in range(0, len(m)):

                        if (
                            m[index].get("tag") == "moleg"
                            or m[index].get("tag") == "mosenate"
                            or m[index].get("tag") == "mogov"
                            or m[index].get("tag") == "mosen"
                        ):
                            tweet_list.append(hashtags.text)
            except:
                pass

        return tweet_list

    def get_user_information(self, twitter_user):

        dict = {}
        user = api.get_user(screen_name=twitter_user)
        dict["screen_name"] = user.screen_name
        dict["user_name"] = user.name
        dict["user_description"] = user.description
        dict["user_location"] = user.location
        dict["user_created_at"] = user.created_at
        dict["user_tweets"] = user.statuses_count
        dict["user_liked_tweets"] = user.favourites_count
        dict["user_followers_count"] = user.followers_count
        dict["user_following_count"] = user.friends_count
        dict["user_get_enabled"] = user.geo_enabled
        dict["user_twitter_id"] = user.id
        dict["user_listed_count"] = user.listed_count

        return dict

    def get_stl_trends(self):
        trends = api.get_place_trends(id="23424977")

        return trends

    def get_user_lists(self, twitter_username):
        userinfo = api.get_user(screen_name=twitter_username)
        user_id = userinfo.id
        user_lists = client.get_list_memberships(user_id)

        return user_lists.data

    def get_auth_user(self):
        me = client.get_me().data
        return me

    def get_tweet_performance(self):
        df = pd.DataFrame(
            columns=[
                "Tweet_id",
                "Created_at",
                "Tweet",
                "Likes",
                "Retweets",
                "Impression_Count",
                "Profile_Clicks",
                "Link",
            ]
        )
        _me = client.get_me().data
        query = f"from:{_me}"
        text = "see tweet"

        response = client.get_users_tweets(
            id=config.dingersid,
            tweet_fields=["organic_metrics", "non_public_metrics", "created_at"],
            max_results=100,
            user_auth=True,
        )

        for tweet in response.data:

            tweet_link = f"https://www.twitter.com/twitter/statuses/{tweet.id}"
            url = f'<a target="_blank" href="{tweet_link}">{text}</a>'

            df = df.append(
                {
                    "Tweet_id": tweet.id,
                    "Created_at": tweet.created_at,
                    "Tweet": tweet.text,
                    "Likes": tweet["organic_metrics"].get("like_count"),
                    "Retweets": tweet["organic_metrics"].get("retweet_count"),
                    "Impression_Count": tweet["organic_metrics"].get(
                        "impression_count"
                    ),
                    "Profile_Clicks": tweet["organic_metrics"].get(
                        "user_profile_clicks"
                    ),
                    "Link": url,
                },
                ignore_index=True,
            )
            #

        # df = df.to_html(escape=False)

        return df

    def convert_user_id_to_name(self, id):
        screen_name = client.get_user(id=id)

        return screen_name.data

    def get_most_active_users(self, data):
        user_list = []
        name_list = []
        for tweet in data:
            u = tweet.author_id
            user_list.append(u)

        return user_list

    def get_user_list_names(self, user_list):
        active_list = []
        for index in range(0, len(user_list)):
            temp = user_list[index]
            uid = user_list[index][0]
            m = api.get_user(user_id=uid)
            name = "@" + m.screen_name
            real_name = m.name
            followers_count = m.followers_count

            posts = temp[1]
            temp_list = [real_name, name, followers_count, posts]
            active_list.append(temp_list)

        return active_list

    def print_stats_graphic(
        self, tlist, topx, title, filename, headers, width, font_size
    ):
        top_list = []
        top_list.append(headers)

        i = 0
        for x in tlist:
            if i <= topx:
                top_list.append(tlist[i])
            i = i + 1
        data = top_list

        fig = ff.create_table(data)
        fig.update_layout({"margin": {"t": 80}})
        fig.update_layout(title_text=title, title_x=0.5)
        fig.update_layout(font_size=20)
        fig["layout"]["title"]["font"] = dict(size=font_size)
        fig.update_layout(width=width)

        fig.write_image(filename)

        return
