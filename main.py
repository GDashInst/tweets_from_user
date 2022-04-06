# Tweepy
import tweepy
import pandas as pd
from tweepy import OAuthHandler
from tweepy import Cursor
import matplotlib.pyplot as plt

"""
Twitter Authentication
"""
cons_key = "2gc6EY8zCdLqEp1aqyeeFJgLz"
cons_secret = "dzSLyoVJJBHNt8G9KkZcuONTs6w0pBE17FxJHksECZ1vXZP4YN"
acc_token = "3439326610-r0rmnjPMwE5O8wq4O24pRLmbFW3EojHiVkzI0bA"
acc_secret = "GG3HN5yS9f3PGlZf0i0lQgEWq1GRBjPkAZ48Y0DNHhHM4"


def get_twitter_auth():
    """
    @return:
        - the authentication to Twitter
    """
    try:
        consumer_key = cons_key
        consumer_secret = cons_secret
        access_token = acc_token
        access_secret = acc_secret

    except KeyError:
        sys.stderr.write("Twitter Environment Variable not Set\n")
        sys.exit(1)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    return auth


def get_twitter_client():
    """
    @return:
        - the client to access the authentication API
    """
    auth = get_twitter_auth()
    client = tweepy.API(auth, wait_on_rate_limit=True)
    return client


def get_tweets_from_user(twitter_user_name, page_limit=16, count_tweet=200):
    """
    @params:
        - twitter_user_name: the Twitter username of a user (company, etc.)
        - page_limit: the total number of pages (max=16)
        - count_tweet: maximum number to be retrieved from a page

    @return
        - all the tweets from the user twitter_user_name
    """
    client = get_twitter_client()

    all_tweets = []

    for page in Cursor(client.user_timeline,
                       screen_name=twitter_user_name,
                       count=count_tweet).pages(page_limit):
        for tweet in page:
            parsed_tweet = {'date': tweet.created_at, 'author': tweet.user.name, 'twitter_name': tweet.user.screen_name,
                            'text': tweet.text, 'number_of_likes': tweet.favorite_count,
                            'number_of_retweets': tweet.retweet_count}

            all_tweets.append(parsed_tweet)

    # Create dataframe
    df = pd.DataFrame(all_tweets)

    # Remove duplicates if there are any
    df = df.drop_duplicates("text", keep='first')

    df.to_csv('Tweets.csv', index=False)

    # This is for the graph

    ylabels = ["number_of_likes", "number_of_retweets"]

    fig = plt.figure(figsize=(13, 3))
    fig.subplots_adjust(hspace=0.01, wspace=0.04)

    # Looking at graphing some of this data using matplotlib

    n_row = len(ylabels)
    n_col = 1
    for count, ylabel in enumerate(ylabels):
        ax = fig.add_subplot(n_row, n_col, count + 1)
        ax.plot(df["date"], df[ylabel])
        ax.set_ylabel(ylabel)
    plt.show()

    return df


# Who are we looking at

InstituteGC = get_tweets_from_user("InstituteGC")
print("Data Shape: {}".format(InstituteGC.shape))
InstituteGC.head(10)

