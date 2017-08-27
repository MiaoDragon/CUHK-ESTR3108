from analyzer import analyze
import sys
sys.path.append('../common/')
from read import read_data

"""
arguments:  [input_filename]
default:    input_filename -- real.csv

functions:
guess()
--------------------------------------------------------
    parameters:
        sample_num, feature_num
    return:
        n, feature_list     : feature index list to analyze convariance
--------------------------------------------------------
analyze()
--------------------------------------------------------
    parameters:
        sample_num, feature_num, features    : data
        n, feature_list                      : from guesser
        
--------------------------------------------------------

"""
#default
input_filename = 'real.csv'
output_filename = 'model.txt'
feature_list = []
if len(sys.argv) >= 2:
    if sys.argv[1][0] != '-':
        input_filename = sys.argv[1]
        n = -int(sys.argv[2])
        start = 3
    else:
        n = -int(sys.argv[1])
        start = 2
for i in range(start, len(sys.argv)):
    feature_list.append( int(sys.argv[i]) )
output_filepath = '../data/' + output_filename
sample_num, feature_num, features, NULL = read_data(input_filename)
convs = analyze(sample_num, feature_num, features, n, feature_list)
# print out in a file
output = open(output_filepath, "w")
buf = ""
buf += str(sample_num) + ' ' + str(feature_num) + '\n'
buf += str(n) + '\n'
for xi in range(0, n):
    buf += str(feature_list[xi])
    if xi < n-1:
        buf += ' '

buf += '\n'
output.write(buf)
for xi in range(0, n):
    buf = ""
    for yi in range(0, n):
        if xi <= yi:
            buf += str(round(convs[xi][yi-xi], 4))
        else:
            buf += str(round(convs[yi][xi-yi], 4)) 
        if yi < n-1:
            buf = buf + ' '
    buf = buf + '\n'
    output.write(buf)

output.close()
