#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Input parameter is not correct. ./run_maxent.sh [test_data]"
    exit
fi

mallet_folder="sentiment/mallet/mallet-2.0.8RC3/bin"
me_classifier="$1"
input_file="$2"
input_basename=$(basename $input_file)
output_file=${input_basename%.*}"_me.output"
output_folder=$(dirname $input_file)

# Check classifier exists
if [ ! -f  "$me_classifier" ]; then
    echo "Classifier $me_classifier not found! Please trian first"
    exit
fi

# Run on test file
"$mallet_folder"/mallet classify-file --input "$input_file" --output me_test.tmp --classifier $me_classifier
python sentiment/preprocessing/extract_mallet_result.py me_test.tmp "$output_folder"/"$output_file"
echo "Output write to ""$output_folder"/"$output_file"
echo "Remove temporary files"
rm -v me_test.tmp
