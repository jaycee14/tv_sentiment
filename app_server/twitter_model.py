from tweepy import OAuthHandler
from tweepy.api import API as Twitter
from tweepy.parsers import JSONParser
from dateutil import parser
from pytz import utc

import json


class Twitter_Retrieve:
    """Wrapper class to add twitter management functionality required."""

    def __init__(self):
        with open('twitter_api_creds.json', "rb") as f:
            self.conf = json.load(f)

            self.auth = OAuthHandler(self.conf["twitter"]["api"]["app"]["key"],
                                     self.conf["twitter"]["api"]["app"]["secret"])
            self.auth.set_access_token(self.conf["twitter"]["api"]["app"]["token"],
                                       self.conf["twitter"]["api"]["app"]["token_secret"])
            self.twitter = Twitter(self.auth, parser=JSONParser())

    def search(self, search_str, since_id=-1, num_entries=15):
        """Twitter search that performs search since last id, timezone conversion and json reduction."""

        results = self.twitter.search(search_str, lang='en', count=num_entries, tweet_mode='extended',
                                      since_id=since_id)

        texts = []
        ids_seen = []
        ids_seen.append(since_id)
        for tweet in results['statuses']:
            dt = parser.parse(tweet['created_at'])
            dt_utc = dt.astimezone(utc)
            responce = {'text': tweet['full_text'], 'date': dt_utc}
            texts.append(responce)
            ids_seen.append(tweet['id'])

        return texts, max(ids_seen)
