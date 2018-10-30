#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Input parameter is not correct. ./train_maxent.sh [train_data]"
    exit
fi

mallet_folder="sentiment/mallet/mallet-2.0.8RC3/bin"
input="$1"
output="${input%%/*}/me.classifier"
temp_directory=`mktemp -d`
temp_input="${temp_directory}/temp.input"
mallet_train="${temp_directory}/mallet_train.mallet"

# Delete old train file
rm -f me.classifier

# Preprocessing
python3 sentiment/preprocessing/pre_addname.py "$input" "$temp_input"

#import train file
"$mallet_folder"/mallet import-file --input "$temp_input" --output "$mallet_train"

# train classifier
"$mallet_folder"/mallet train-classifier --trainer MaxEnt --input "$mallet_train" --output-classifier "$output"

rm -rv "$temp_directory"
