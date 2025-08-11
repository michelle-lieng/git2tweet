import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

client = tweepy.Client(
    consumer_key=os.getenv("TW_CONSUMER_KEY"),
    consumer_secret=os.getenv("TW_CONSUMER_SECRET"),
    access_token=os.getenv("TW_ACCESS_TOKEN"),            # user token (write-enabled)
    access_token_secret=os.getenv("TW_ACCESS_TOKEN_SECRET")
)

resp = client.create_tweet(text="Test tweet from Tweepy v2!")
print(resp.data["id"])
print(resp.data["text"])

