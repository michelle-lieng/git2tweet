import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

class TwitterClient:
    def __init__(self):
        self.client = tweepy.Client(
            consumer_key=os.getenv("TW_CONSUMER_KEY"),
            consumer_secret=os.getenv("TW_CONSUMER_SECRET"),
            access_token=os.getenv("TW_ACCESS_TOKEN"), #ensure write access!
            access_token_secret=os.getenv("TW_ACCESS_TOKEN_SECRET")
        )

    def post_tweet(self, text: str):
        resp = self.client.create_tweet(text=text)
        return resp.data["id"]

# Usage
if __name__ == "__main__":
    twitter = TwitterClient()
    tweet_id = twitter.post_tweet("Test tweet from Tweepy v2!")
    print(tweet_id)
