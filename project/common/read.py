import csv

# read from csv file
# return
#           number of samples
#           number of features
#           feature matrix
#           label matrix
def read_data( filename='samples.csv' ):
    filepath = '../data/' + filename
    try:
        infile = open(filepath, "r")
    except IOError as e:
        print("input file wrong!\n")
        exit(-1)

    reader = csv.reader(infile)
    sample_index = 0
    feature_index = 0
    features = []
    labels = []
    for row in reader:
        feature_sample = []
        feature_index = 0
        for col in row:
            if col == "false":
                feature = 0
            elif col == "true":
                feature = 1
            else:
                feature = int(col)
            if feature == 0:
                feature_sample.append([1, 0, 0, 0])
            if feature == 1:
                feature_sample.append([0, 1, 0, 0])
            if feature == 2:
                feature_sample.append([0, 0, 1, 0])
            if feature == 3:
                feature_sample.append([0, 0, 0, 1])
            feature_index += 1
        # handle the label value
        if feature_sample[feature_index - 1][0] == 1:
            feature_sample.pop()
            features.append(feature_sample)
            labels.append([1, 0])
        else:
            feature_sample.pop()
            features.append(feature_sample)
            labels.append([0, 1])
        sample_index += 1

    infile.close()
    # feature_index now contains label
    feature_index -= 1
    return sample_index, feature_index, features, labels

