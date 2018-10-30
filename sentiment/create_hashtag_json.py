import json

from pymongo import MongoClient

from sentiment.add_tweet import add_tweet


def create_hashtag_json(hashtag, start_timestamp, output):
    output_file = open(output, 'w')
    database = MongoClient()['stream_store']
    query_string = {'timestamp_ms': {"$gte": start_timestamp}, 'entities.hashtags.text': hashtag}
    tweets = {}
    for tweet in database.tweets.find(query_string):
        add_tweet(tweet, tweets)
    output_file.write(json.dumps(tweets))
    output_file.close()


if __name__ == "__main__":
    import argparse
    import datetime
    import time

    PROGRAM_DESCRIPTION = "Create JSON file of tweets containing a given hashtag"
    parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
    parser.add_argument('hashtag', type=str, help='TV show we are looking for')
    parser.add_argument('startday', type=str, help='The first day we include')
    parser.add_argument('output', type=str, help='Output file')
    args = vars(parser.parse_args())
    hashtag = args['hashtag']
    start_timestamp = str(int(time.mktime(datetime.datetime.strptime(args['startday'], "%m/%d/%Y").timetuple())) * 1000)
    output = args['output']
    create_hashtag_json(hashtag, start_timestamp, output)