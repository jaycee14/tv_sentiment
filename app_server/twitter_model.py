from tweepy import OAuthHandler
from tweepy.api import API as Twitter
from tweepy.error import TweepError
from tweepy.parsers import JSONParser

import json


class Twitter_Retrieve:

    def __init__(self):
        with open('twitter_api_creds.json', "rb") as f:
            self.conf = json.load(f)

            self.auth = OAuthHandler(self.conf["twitter"]["api"]["app"]["key"],
                                     self.conf["twitter"]["api"]["app"]["secret"])
            self.auth.set_access_token(self.conf["twitter"]["api"]["app"]["token"],
                                       self.conf["twitter"]["api"]["app"]["token_secret"])
            self.twitter = Twitter(self.auth, parser=JSONParser())

    def search(self, search_str, since_id=-1, num_entries=15):
        results = self.twitter.search(search_str, lang='en', count=num_entries, tweet_mode='extended', since_id=since_id)

        texts = []
        for tweet in results['statuses']:
            text = tweet['full_text']
            texts.append(text)
            last_id = tweet['id']

        return texts, last_id
