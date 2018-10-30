#!/usr/bin/python3

from datetime import datetime
import os
import shutil
import subprocess
import sys
import tempfile

from sentiment.JsonToRawTextMaxEnt import *
from sentiment.SentimentToJson import *
from sentiment.create_hashtag_json import create_hashtag_json


# noinspection PyShadowingNames
def get_sentiment_data(hashtag, start_timestamp):
    tempdir = tempfile.mkdtemp()
    base_filename = "{}/{}".format(tempdir, hashtag)
    sentiment_filename = "{}/{}_{}_sentiment.json".format(
        os.getcwd(),
        hashtag,
        datetime.utcfromtimestamp(int(start_timestamp)//1000).strftime("%Y-%m-%d")
    )

    os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))

    # 3.1 Get JSON file containing tweets using the hashtag
    output_file = base_filename + "_tweets.json"
    print("Getting tweets")
    create_hashtag_json(hashtag, start_timestamp, output_file)

    # 3.2 Separate json file into raw text and index files for maxent
    input_file = output_file
    output_file = base_filename + ".input"
    index_file = base_filename + ".index"
    print("Separating tweets into raw test and index files")
    JsonToRawTextMaxEnt(input_file, output_file, index_file).start()

    # 4. Run maxent using trained classifier
    input_file = output_file
    print("Running maxent")
    subprocess.Popen(["sentiment/run_maxent.sh", "data/me.classifier", input_file]).wait()

    # 5. Put everything back into jason format
    input_file = base_filename + "_me.output"
    output_file = sentiment_filename
    print("Creating JSON file with sentiment data")
    SentimentToJson(input_file, output_file, index_file).start()

    shutil.rmtree(tempdir)


if __name__ == "__main__":
    import argparse
    import time

    PROGRAM_DESCRIPTION = "Get sentiment data for a given hashtag"
    parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
    parser.add_argument('hashtag', help='Hashtag to get sentiment data for')
    parser.add_argument('startday', type=str, help='The first day we include')
    args = vars(parser.parse_args())
    start_timestamp = str(int(time.mktime(datetime.strptime(args['startday'], "%m/%d/%Y").timetuple())) * 1000)

    get_sentiment_data(args['hashtag'], start_timestamp)
