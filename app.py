import streamlit as st
import tweepy
import config
from moleg import MoLegTwitter

m = MoLegTwitter()
response = m.hydrate_tweets()


st.sidebar.title("Moleg Twitter Analysis Tools")
page = st.sidebar.selectbox(
    "Select Tool",
    [
        "User Information",
        "Top Hashtags",
        "Top Mentions",
        "Top Moleg Tweeters",
        "My Tweet Performance",
        "User List Memberships",
        "St. Louis Twitter Trends",
    ],
)
st.title("Politwit1984 Twitter Analytic Tools")


if page == "User Information":
    st.header("Moleg Utilities - Get User Info")
    twitter_user = st.text_input(
        "Enter Twitter screenname to get information about Twitter user."
    )
    if twitter_user:
        user_dict = m.get_user_information(twitter_user)
        st.write("User Twitter screen name: ", user_dict["screen_name"])
        st.write("User Name: ", user_dict["user_name"])
        st.write("User Description: ", user_dict["user_description"])
        st.write("User location: ", user_dict["user_location"])
        st.write("User created on: ", user_dict["user_created_at"])
        st.write("User Tweets: ", user_dict["user_tweets"])
        st.write("User liked tweets: ", user_dict["user_liked_tweets"])
        st.write("User followers count: ", user_dict["user_followers_count"])
        st.write("User following count: ", user_dict["user_following_count"])
        st.write("User geo-enabled: ", user_dict["user_get_enabled"])
        st.write("User Twitter ID: ", user_dict["user_twitter_id"])
        st.write("User list memberships: ", user_dict["user_listed_count"])


elif page == "Top Hashtags":
    st.header("Moleg Utilities - Top Hashtags")
    hashtags = m.get_hashtags(response)
    top_hashtags = m.get_most_common(hashtags, 50)
    st.header("Moleg Current Top Hashtags")
    for index in range(0, len(top_hashtags)):
        th = top_hashtags[index]
        url = "https://twitter.com/search?q=(%23" + str(th[0] + ")&f=live")
        h = str(th[0])
        h1 = str(th[1])
        st.write("%s -" % h1 + " #" + "%s" % h + " [see here](%s)" % url)

elif page == "Top Mentions":
    st.header("Moleg Utilities - Top Mentions")
    mentions = m.get_mentions(response)
    top_mentions = m.get_most_common(mentions, 50)
    for index in range(0, len(top_mentions)):
        tm = top_mentions[index]
        url = "https://twitter.com/search?q=(%" + str(tm[0] + ")&f=live")
        m = str(tm[0])
        m1 = str(tm[1])
        st.write("%s -" % m1 + " @" + "%s" % m + " [see here](%s)" % url)

elif page == "St. Louis Twitter Trends":
    trends = m.get_stl_trends()
    for value in trends:
        for trend in value["trends"]:
            st.write(
                trend["name"] + " has tweet volume of: " + str(trend["tweet_volume"])
            )


elif page == "User List Memberships":
    st.header("Moleg Utilities - Get memberships")
    twitter_username = st.text_input(
        "Enter screen name to get list of Twitter list memberships."
    )
    if twitter_username:
        twitter_lists = m.get_user_lists(twitter_username)
        for x in twitter_lists:
            st.write(x.name, ("https://twitter.com/i/lists/" + str(x.id)))

elif page == "My Tweet Performance":
    st.header("Moleg Utilities - Get Tweet Performance")
    tweet_performance = m.get_tweet_performance()
    st.write(tweet_performance, unsafe_allow_html=True)
    # st.write(df, unsafe_allow_html=True)

elif page == "Top Moleg Tweeters":
    st.header("Moleg Utilities - Get Top Moleg Tweeters")
    user_list = m.get_most_active_users(response)
    top_users = m.get_most_common(user_list, 30)
    au = m.get_user_list_names(top_users)
    for index in range(0, len(au)):
        st.write(au[index][0], au[index][1])
