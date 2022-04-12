import math
from collections import Counter
from datetime import datetime, timedelta
from re import U


import config

# import matplotlib.pyplot as plt
import numpy as np
import tweepy
from PIL import Image, ImageDraw, ImageFont

# from twit import makeitastring
# from wordcloud import ImageColorGenerator, WordCloud

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
bearer_token = config.bearer_token
api = tweepy.API(auth)
client = tweepy.Client(bearer_token=config.bearer_token)


class MoLegTwitter:
    def __init__(self):
        self.query = "(moleg OR mogov OR mosenate OR mosen) -is:retweet"
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
        ).flatten(limit=1000)

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
        # my_image = Image.open("cloud.png")

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
                            hashtag_list.append(h[index].get("tag"))

            except:
                print("no tag")

        return hashtag_list

    def get_mentions(self, data):

        mentions_list = []
        for tweet in data:
            try:
                m = tweet["entities"]
                m = m.get("mentions")

                if m:
                    for index in range(0, len(m)):

                        mentions_list.append(m[index].get("username"))

            except:
                pass

        return mentions_list

    def get_my_mentions(self, username):

        tweet_list = []

        my_query = f"(@{username}) -is:retweet"

        response = tweepy.Paginator(
            client.search_recent_tweets,
            my_query,
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
        ).flatten(limit=1000)

        return response

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


# m = MoLegTwitter()
# response = m.hydrate_tweets()

# twitter_lists = m.get_user_lists("dingersandks")
# print(twitter_lists)
# for x in twitter_lists:
#     print(x.name, x.id)

# # tweets = m.hydrate_tweets()
# # hashtags = m.get_hashtags(tweets)
# # print(m.get_most_common(hashtags, 20))
# # mentions = m.get_mentions(tweets)
# # print(mentions)
# # print(m.get_most_common(mentions, 20))

# my_mentions = m.get_my_mentions("LauraANNSTL")
# # l = m.get_my_moleg_mentions((my_mentions))
# l = m.get_my_moleg_mentions(my_mentions)


# # print(m.get_most_common(l, 20))

# for index in range(0, len(l)):
#     print(l[index])
#     print("\n")


# # for tweet in my_mentions:
# #     tweet_text = tweet.text
# #     word = tweet_text.find("#moleg")
# #     print(word)

# mentions = m.get_mentions((response))
# top_mentions = m.get_most_common(mentions, 50)


# for index in range(0, len(top_mentions)):
#     tm = top_mentions[index]
#     print(tm[1], tm[0])

# a = 1

# h = m.get_hashtags(response)
# th = m.get_most_common(h, 20)

# print(th)
