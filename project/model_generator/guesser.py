import random
def guess( sample_num, feature_num ):
    random.seed(a=None, version=2)
    n = random.randint(2, 10)
    appear = [0] * feature_num
    feature_list = []
    i = 0
    while (i < n):
        rand = random.randint(0, feature_num-1)
        if not( appear[rand] ):
            appear[rand] = 1
            feature_list.append(rand)
            i += 1
    feature_list.sort()
    return n, feature_list
