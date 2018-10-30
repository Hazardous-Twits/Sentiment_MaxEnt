import json

from sentiment.Pipeline import Pipeline
from sentiment.add_tweet import add_tweet


class CreateTweetJson(Pipeline):
    def process(self):
        tweets = {}
        for line in self.input.readlines():
            add_tweet(json.loads(line), tweets)
        self.output.write(json.dumps(tweets))