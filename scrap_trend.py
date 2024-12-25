import tweepy
from collections import Counter
import re

def extract_mentions(text):
    """Extract mentions from a tweet's text."""
    return re.findall(r"@\w+", text)

def main():
    # Twitter API credentials (replace with your credentials)
    api_key = "your_api_key"
    api_secret = "your_api_secret"
    access_token = "your_access_token"
    access_token_secret = "your_access_token_secret"

    # Authenticate with Twitter
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    # Query parameters
    query = "your search query here"  # e.g., "Python programming"
    max_tweets = 100  # Adjust the number of tweets to scrape

    # Scrape tweets
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en", tweet_mode="extended").items(max_tweets)

    # Extract mentions
    mentions = []
    for tweet in tweets:
        mentions.extend(extract_mentions(tweet.full_text))

    # Count and rank mentions
    mention_counts = Counter(mentions)
    ranked_mentions = mention_counts.most_common()

    # Display results
    print("Most Mentioned Users:")
    for mention, count in ranked_mentions:
        print(f"{mention}: {count}")

if __name__ == "__main__":
    main()
