import datetime
import time


def add_tweet(tweet, tweets):
    user_id = tweet["user"]["id_str"]
    creation_date = tweet["created_at"]
    timestamp = str(int(time.mktime(datetime.datetime.strptime(creation_date, "%a %b %d %H:%M:%S %z %Y").timetuple())))
    text = tweet["text"]

    if user_id in tweets:
        user = tweets[user_id]
    else:
        user = {}
        tweets[user_id] = user

    user[timestamp] = text
