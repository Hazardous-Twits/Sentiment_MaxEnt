from sentiment.ExtractEmotionEmoji import *
from sentiment.JsonToRawText import *
from sentiment.JsonsToJson import *
from sentiment.MaxEntTrainData import *
from sentiment.bson_to_json import bson_to_json


def main():
    # Convert tweet bson file to Json objects
    input_file = "./data/historical_tweet.bson"
    output_file = "./data/historical_tweet_jsons.txt"
    bson_to_json(input_file, output_file)

    # Create Json file in the needed format
    input_file = output_file
    output_file = "./data/historical_tweet.json"
    CreateTweetJson(input_file, output_file).start()

    # Get raw sentiment text
    input_file = output_file
    output_file = "./data/historical_tweet.raw"
    JsonToRawText(input_file, output_file).start()

    # Get text with emoji/emoticon
    input_file = output_file
    output_file = "./data/emoji_emoticon_only.raw"
    ExtractEmotionEmoji(input_file, output_file).start()

    # Get train data set
    input_file = output_file
    output_file = "./data/maxent_train.input"
    MaxEntTrainData(input_file, output_file).start()


if __name__ == "__main__":
    main()
