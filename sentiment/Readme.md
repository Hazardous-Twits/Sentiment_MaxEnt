Since Maxent algorithm is written in Java, we need to use Python to do some preprocessing.

# Input Json format

~~~json
{
    "user_id_1": {
        "timestamp1": "tweets_text",
        "timestamp2": "tweets_text",
    },
    "user_id_2": {
        "timestamp1": "tweets_text",
        "timestamp2": "tweets_text",
    }
}
~~~

# To Get Trained Classifier Only
run `python3 train_maxent.py [train_bson_file]`, get trained classifier `me.classifier`

# To Get Sentiment Data with Existing Classifier
run `python3 get_sentiment_data [test_bson_file]`

# To Train Classifier and Get Sentiment Data
~~~bash
python3 sentiment_train_and_test [train_bson_file] [test_bson_file]
~~~

# Step 1
run `python3 main.py`

# Step 2
run `train_maxent.sh data/maxent_train.input`, get trained classifier `me.classifier`

# Step 3
Preprocessing test data, since maxent tool only take raw text, we have to have a index file to keep the userid and timestamp of a raw tweet text

~~~bash
python3 JsonToRawTextMaxEnt.py data/tvshow_tweet.json data/tvshow_tweet_textonly.input data/tvshow_tweet_textonly.index
~~~

# Step 4
Run maxent using trained classifier `me.classifier`

~~~bash
./run_maxent.sh data/tvshow_tweet_textonly.input
~~~

# Step 5
Put everything(Sentiment/userid/timestmap) back into json format
~~~bash
python3 SentimentToJson.py data/tvshow_tweet_textonly_me.output data/tvshow_tweet_sentiment.json data/tvshow_tweet_textonly.index
~~~
