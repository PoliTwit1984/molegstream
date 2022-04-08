import math
from collections import Counter
from datetime import datetime, timedelta


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
        ).flatten(limit=500)

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
        for tweet in tweets:
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
                            print(h[index].get("tag"))
            except:
                print("no tag")

        return hashtag_list


m = MoLegTwitter()

tweets = m.hydrate_tweets()
for x in tweets:
    print(x.created_at, x.text)

# hashtags = m.get_hashtags(tweets)
# print(hashtags)


# print(hashtag_list)

# # hashtag_list = m.makeitastring(hashtag_list)

print(m.get_most_common(hashtags, 20))

# hashtags = m.get_hashtags(tweets)
# print(hashtags)
# hashtags = m.get_hashtags(filename="hashtags-moleg.txt", number_hashtags=100)
# total = m.get_most_common(hashtags, 15)
# print(total)
# print(type(total))
