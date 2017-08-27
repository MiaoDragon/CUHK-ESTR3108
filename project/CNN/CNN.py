'''
Project: synthetic gene data
Background: Use CNN to classify illness by gene features
This program: implementation of CNN to identify synthetic data
    features: normal distribution
    label   : 0 or 1
Author: Miao Yinglong
Reference: 
    https://github.com/aymericdamien/TensorFlow-Examples/ @Aymeric Damien
'''

"""
Arguments:
    [test_filename] [train_filename]
"""
import csv
import math
import sys
sys.path.append('../common/')
import tensorflow as tf
from read import read_data
#filename default
train_filename = "synthetic.csv"
test_filename = "real.csv"
if len(sys.argv) > 1:
    test_filename = sys.argv[1]
if len(sys.argv) > 2:
    train_filename = sys.argv[2]

# parameters
learning_rate = 0.001
training_iters = 100
batch_size = 10
display_step = 10

# Network Parameters
n_sample, n_input, features, labels = read_data(train_filename)
# features * 4 (img size: n_input * 4)
n_classes = 2  # 0 and 1
keep_rate = 0.75  # Dropout, probability to keep units
filter_width = 5 # filter size
p1_width = 10 # pooling rate for first pooling
p2_width = 10 # pooling rate for second pooling
remain = math.ceil(float(n_input) / float(p1_width)) # remaining items after pooling
remain = math.ceil(float(remain) / float(p2_width))
remain = remain * 4

# tf Graph input
x = tf.placeholder(tf.float32, [None, n_input, 4])
y = tf.placeholder(tf.float32, [None, n_classes])
keep_prob = tf.placeholder(tf.float32) # keep probability for dropout

# Create some wrappers for simplicity
def conv2d(x, W, b, strides=1):
    # Conv2D wrapper, with bias and relu activation
    x = tf.nn.conv2d(x, W, strides=[1, strides, strides, 1], padding='SAME')
    x = tf.nn.bias_add(x, b)
    return tf.nn.relu(x)

def maxpool2d(x, k=2):
    # MaxPool2D wrapper
    # Pooling for each feature value
    return tf.nn.max_pool(x, ksize=[1, k, 1, 1], strides=[1, k, 1, 1], padding='SAME')

# Store layers weight & bias
weights = {
    # f_w*f_w conv, 1 input, 32 outputs
    'wc1':  tf.Variable(tf.random_normal([filter_width, 4, 1, 32])),
    # f_w*f_w conv, 32 inputs, 64 outputs
    'wc2':  tf.Variable(tf.random_normal([filter_width, 4, 32, 64])),
    # fully connected, 8*5*64 inputs, 100 outputs
    'wf1':  tf.Variable(tf.random_normal([remain * 64, 100])),
    # fully connected, 100 inputs, 2 outputs (classification)
    'out':  tf.Variable(tf.random_normal([100, n_classes]))
}

biases = {
    'bc1':  tf.Variable(tf.random_normal([32])),
    'bc2':  tf.Variable(tf.random_normal([64])),
    'bf1':  tf.Variable(tf.random_normal([100])),
    'out':  tf.Variable(tf.random_normal([n_classes]))
}

# Create model
def conv_net(x, weights, biases, keep_rate):
    # Reshape input
    x = tf.reshape(x, shape=[-1, n_input, 4, 1])

    # Convolution Layer
    conv1 = conv2d(x, weights['wc1'], biases['bc1'])
    # Max Pooling
    conv1 = maxpool2d(conv1, k=p1_width)

    # Convolution Layer
    conv2 = conv2d(conv1, weights['wc2'], biases['bc2'])
    # Max Pooling
    conv2 = maxpool2d(conv2, k=p2_width)

    # Fully Connected Layer
    # Reshape conv2 output
    fc1 = tf.reshape(conv2, [-1, weights['wf1'].get_shape().as_list()[0]])
    # multiply and plus bias
    fc1 = tf.add(tf.matmul(fc1, weights['wf1']), biases['bf1'])
    fc1 = tf.nn.relu(fc1)
    # Apply Dropout
    fc1 = tf.nn.dropout(fc1, keep_rate)

    # Output, Classification
    out = tf.add(tf.matmul(fc1, weights['out']), biases['out'])
    return out

# Construct model
pred = conv_net(x, weights, biases, keep_prob)

# Define loss and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(pred, y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# Evaluate model
correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# Initializing the variables
init = tf.initialize_all_variables()

# Launch the graph
with tf.Session() as sess:
    sess.run(init)
    step = 0
    start = 0  # batch start position
    empty = 0  # remaining empty or not
    # training
    while not(empty):
        # Run optimization
        x_batch = []
        y_batch = []
        if start >= n_sample:
            empty = 1
            break
        for i in range(0, batch_size):
            if start <  n_sample:
                x_batch.append(features[start])
                y_batch.append(labels[start])
                start += 1
            else:
                empty = 1
                break
        sess.run(optimizer, feed_dict={x: x_batch, y: y_batch, keep_prob: keep_rate})
        # Calculate accuracy for 100 samples
        step += 1
        if step %  display_step == 0:
            print("accuracy for step [%d]" % (step), sess.run(accuracy, feed_dict={x: x_batch, y: y_batch, keep_prob: 1}))
    # test
    n_sample, n_input, features, labels = read_data(test_filename)
    print("Testing Accuracy:", \
            sess.run(accuracy, feed_dict={x: features, 
                                          y:labels, 
                                          keep_prob:1.}))
