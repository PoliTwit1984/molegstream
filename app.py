import streamlit as st
import tweepy
import config
from moleg import MoLegTwitter


st.sidebar.title("Moleg Twitter Analysis Tools")
page = st.sidebar.selectbox(
    "Select Tool",
    [
        "Top Hashtags",
        "Top Mentions",
        "Twitter User Liked Posts WordCloud",
        "Twitter Lists a User Belongs",
        "Twitter database tests",
        "Real time Biden Sentiment",
        "Real time WordCloud",
        "St. Louis Twitter Trends",
    ],
)
st.title("Politwit1984 Twitter Analytic Tools")

m = MoLegTwitter()

response = m.hydrate_tweets()


if page == "Top Hashtags":
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

    mentions = m.get_mentions(response)
    top_mentions = m.get_most_common(mentions, 50)
    for index in range(0, len(top_mentions)):
        tm = top_mentions[index]
        url = "https://twitter.com/search?q=(%" + str(tm[0] + ")&f=live")
        m = str(tm[0])
        m1 = str(tm[1])
        st.write("%s -" % m1 + " @" + "%s" % m + " [see here](%s)" % url)
