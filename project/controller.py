import sys
sys.path.append('common/')
import random
import subprocess
from read import read_data

# variables
MAX = 50
population = 10
generation = []
abandoned = []
mutate_rate = 0.3
cross_over_num = 10
old_score = 0
# class
class individual:
    score = 0
    num = 0
    feature_list = []
    def modify(self, num, feature_list):
        self.num = num
        self.feature_list = feature_list
# functions
def init(feature_num):
    # create classes
    for i in range(0, population+cross_over_num):
        generation.append(individual())
    # first generation
    random.seed(a=None, version=2)
    for i in range(0, population):
        for j in range(0, 10):
            rand = random.randint(0, feature_num-1)
            generation[i].feature_list.append(rand)
        generation[i].feature_list.sort()
        generation[i].num = len(set(generation[i].feature_list))

def crossover(p1, p2):
    # return the nums and feature_lists
    rand = random.randint(1, 9)
    # cross over from rand to 9
    crossed_list1 = []
    crossed_list2 = []
    for i in range(0, rand):
        crossed_list1.append(p1.feature_list[i])
        crossed_list2.append(p2.feature_list[i])
    for i in range(rand, 10):
        crossed_list2.append(p1.feature_list[i])
        crossed_list1.append(p2.feature_list[i])
    crossed_list1.sort()
    crossed_list2.sort()
    num1 = len(set(crossed_list1))
    num2 = len(set(crossed_list2))
    return num1, crossed_list1, num2, crossed_list2
        
def mutate(p):
    #return the num and feature_list
    if (random.random() >= mutate_rate):
        return p.num, p.feature_list
    ran = random.randint(0, 9)  # location
    mutation_list = p.feature_list
    mutation_list[ran] = random.randint(0, feature_num-1)
    mutation_list.sort()
    num = len(set(mutation_list))
    return num, mutation_list
def evaluate(p):
    cmd = ["./cycle.sh"]
    cmd.append("-" + str(p.num))
    for k in range(0, p.num):
        cmd.append(str(p.feature_list[k]))
    output = subprocess.check_output(cmd).decode("utf-8")
    spos = output.find("Testing Accuracy")
    output = output[spos:len(output)]
    for c in output:
        if not c in '.0123456789':
            output = output.replace(c, '')
    return float(output)
 
input_filename = 'real.csv'
NULL, feature_num, NULL, NULL = read_data(input_filename)
init(feature_num)
for i in range(0, MAX):
    # cross over
    for j in range(0, cross_over_num//2):
        random.seed(a=None, version=2)
        num1, crossed_list1, num2, crossed_list2 = crossover( generation[random.randint(0, population-1)], \
                                                              generation[random.randint(0, population-1)])
        generation[population+j*2].modify(num1, crossed_list1)
        generation[population+j*2+1].modify(num2, crossed_list2)
    # mutate
    for j in range(0, population):
        num, mutation_list = mutate(generation[j])
        generation[j].modify(num, mutation_list)
    # evaluate
    for j in range(0, population+cross_over_num):
        generation[j].score = evaluate(generation[j])
    sorted(generation, key=lambda individual: individual.score)
# output the best one
evaluate(generation[0])
