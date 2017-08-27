# output:
#       file: convariance matrix
def value( features ):
    ans = features[0]*0 + features[1]*1 + features[2]*2 + features[3]*3
    return ans

def analyze( sample_num, feature_num, features, n, feature_list ):
# parameter: sample_num, feature_num, features  --  data
# n, feature_list                               --  n features to analyze convariance
#                                                   index from 0

    expects = []  # expectation of each feature
    convs = []  # convariances
    # get expectations of each feature
    for xi in range(0, n):
        x = feature_list[xi]
        expect = float(0)
        for i in range(0, sample_num):
            expect += value(features[i][x])
        expect = expect / sample_num
        expects.append(expect)
    # get convariances
    for xi in range(0, n):
        x = feature_list[xi]
        conv_x = [] # convariances of x
        for yi in range(xi, n):
            y = feature_list[yi]
            expect = float(0)
            for i in range(0, sample_num):
                expect += value(features[i][x]) * value(features[i][y])
            expect = expect / sample_num
            conv = expect - expects[xi]*expects[yi]
            conv_x.append(conv)
        convs.append(conv_x)
    return convs

