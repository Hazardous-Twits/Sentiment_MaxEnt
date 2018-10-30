#!/usr/bin/python3
import os
import subprocess

from sentiment.ExtractEmotionEmoji import *
from sentiment.JsonToRawText import *
from sentiment.JsonsToJson import *
from sentiment.MaxEntTrainData import *
from sentiment.bson_to_json import bson_to_json


def train_maxent(input_file):
    # 1. Pre-process train data
    # 1.1 Convert tweet BSON file to JSON objects
    # input_file = "data/historical_tweet.bson"
    train_data = input_file[:input_file.index(".bson")]
    output_file = train_data + "_jsons.txt"
    bson_to_json(input_file, output_file)

    # 1.2 Create Json file in the needed format
    input_file = output_file
    output_file = train_data + ".json"
    CreateTweetJson(input_file, output_file).start()

    # 1.3 Get raw sentiment text
    os.remove(input_file)
    input_file = output_file
    output_file = train_data + ".raw"
    JsonToRawText(input_file, output_file).start()

    # 1.4 Get text with emoji/emoticon
    os.remove(input_file)
    input_file = output_file
    output_file = "data/emoji_emoticon_only.raw"
    ExtractEmotionEmoji(input_file, output_file).start()

    # 1.5 Get train data set
    os.remove(input_file)
    input_file = output_file
    output_file = "data/maxent_train.input"
    MaxEntTrainData(input_file, output_file).start()

    # 2. Get trained classifier
    os.remove(input_file)
    input_file = output_file
    subprocess.Popen(["sentiment/train_maxent.sh", input_file]).wait()

    os.remove(input_file)


if __name__ == "__main__":
    import argparse

    PROGRAM_DESCRIPTION = "Train MaxEnt classifier"
    parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
    parser.add_argument('input_file', help='Input train data in bson')
    args = vars(parser.parse_args())

    train_maxent(args['input_file'])
