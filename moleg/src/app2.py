from moleg import MoLegTwitter

m = MoLegTwitter()
response = m.hydrate_tweets()
au = []
user_list = m.get_most_active_users(response)
top_users = m.get_most_common(user_list, 30)
au = m.get_user_list_names(top_users)
m.print_stats_graphic(
    au,
    30,
    "Most Active #Moleg Tweeters over last 1000 Tweets 6-26-2022",
    "MAU.png",
    ["Name", "Username", "Followers Count", "No. of Tweets"],
    2000,
    40,
)


response = m.hydrate_tweets()
hashtag_list = m.get_hashtags(response)
print(hashtag_list)
top_hashtags = m.get_most_common(hashtag_list, 30)
print(top_hashtags)
m.print_stats_graphic(
    top_hashtags,
    30,
    "Most Active #Moleg Hashtags over last 1000 Tweets 6-26-2022",
    "hash.png",
    ["Hashtag", "Count"],
    800,
    20,
)

response = m.hydrate_tweets()
mention_list = m.get_mentions(response)
print(mention_list)
top_mentions = m.get_most_common(mention_list, 30)
print(top_mentions)
m.print_stats_graphic(
    top_mentions,
    30,
    "Most Active #Moleg @Mentions over last 1000 Tweets 6-26-2022",
    "mentions.png",
    ["Mention", "Count"],
    800,
    20,
)

# # df = m.get_tweet_performance()
# # with open("tweet_performance.csv", "w") as f:
# #     df.to_csv(f, index=False)
