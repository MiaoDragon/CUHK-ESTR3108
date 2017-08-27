#!/bin/bash
source ~/tensorflow/bin/activate
# this shell script runs the loop to train CNN with synthetic data
# 1. model_generator/model.py:
#       arguments: 
#                   [input_filename] (real data) -n m1 m2 m3 ... mn
#       --- analyze the input file, and output the model file
#           n is the number of correlated variables, which are m1, m2, ..., mn
#       input:  input_filename (default="real.csv")
#       output: model.txt
# 2. data_generator/normal, data_generator/discrete
#       arguments: 
#           discrete: [output_filename] (synthetic data)
#       normal    -- input:  model.txt
#                 -- output: normal.txt
#       discrete  -- input:  normal.txt
#                 -- output: output_filename (default="synthetic.csv")
#           
# 3. CNN/CNN.py
#       arguments:
#                   [test_filename] [train_filename]
#       input:
#           test_filename  (default="synthetic.csv")
#           train_filename (default="real.csv")
#
number=$1
if [ $((number)) -ne 0 ]; then
# need to generate model
    cor_list=""
    i=0
    shift
    while [ "$1" != "" ]; do
        cor_list=${cor_list}" "$1
        shift
    done
    cd model_generator;
    python model.py ${number}${cor_list};
    cd ..;
fi
# still searching or
# best model found
cd data_generator;
./normal;
./discrete;
cd ..;
cd CNN;
if [ $((number)) -ne 0 ]; then
    python CNN.py
else
    [ ! -f data/CNN_result.txt ] && touch ../data/CNN_result.txt
    python CNN.py > ../data/CNN_result.txt
fi
cd ..;
deactivate
