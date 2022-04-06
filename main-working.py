# Tweepy
import tweepy
from tweepy import OAuthHandler
from tweepy import Cursor
import matplotlib.pyplot as plt
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

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

#Values that allows me to clean the data up
emoticons_happy = {':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}', ':^)', ':-D', ':D', '8-D',
                   '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D', '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P',
                   ':-P', ':P', 'X-P', 'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)', '<3'}

emoticons_sad = {':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<', ':-[', ':-<', '=\\', '=/',
                 '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c', ':c', ':{', '>:\\', ';('}

emoji_pattern = re.compile("["
         u"\U0001F600-\U0001F64F"  # emoticons
         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
         u"\U0001F680-\U0001F6FF"  # transport & map symbols
         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
         u"\U00002702-\U000027B0"
         u"\U000024C2-\U0001F251"
         "]+", flags=re.UNICODE)

emoticons = emoticons_happy.union(emoticons_sad)

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

    df.to_csv('Tweets-working.csv', index=False)

    #cleaning

    stop_words = set(stopwords.words('english'))
    word_tokens = nltk.word_tokenize(tweet)

    # after tweepy preprocessing the colon symbol left remain after
    # removing mentions
    tweet = re.sub(r':', '', tweet)
    tweet = re.sub(r'‚Ä¶', '', tweet)

    # replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+', ' ', tweet)

    # remove emojis from tweet
    tweet = emoji_pattern.sub(r'', tweet)

    # filter using NLTK library append it to a string
    filtered_tweet = [w for w in word_tokens if not w in stop_words]

    # looping through conditions
    filtered_tweet = []
    for w in word_tokens:
        # check tokens against stop words , emoticons and punctuations
        if w not in stop_words and w not in emoticons and w not in string.punctuation:
            filtered_tweet.append(w)

    return ' '.join(filtered_tweet)

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

