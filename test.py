from flask import json
from cutword import cutw
import numpy as np
import tensorflow as tf
from incorectword import keyword

reverse_dictionary = json.load(open("reverse_dictionaryCNNnew.txt"))
final_embeddings = np.loadtxt('final_embeddingsCNNnew.txt')
dictionary = {v: int(k) for k, v in reverse_dictionary.items()}
def readFile1():
    a=[]
    with open("8.txt", mode='r', encoding='utf-8-sig') as f:
        s = f.readlines()
        for line in s:
            movie_name = line.replace(' ','').replace('\n','')
            a.append(movie_name)
    return a

def ran(sentence):
        #cut = cutw(sentence)
        cut= keyword(sentence)
        words = []
        for row in cut:
            words.append(row)
        max = 15
        word = ''
        for line in words:
            cut_len = len(line) - 1
            # print(cut)
            if cut_len >= max:
                max = cut_len

        cut_len = len(cut)
        count1 = max - cut_len
        # word = []
        for line2 in range(count1):
            str = 'PAD'
            words.append(str)
        inputs = {'input': [words], 'cate': [['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']]}
        inputs2 = []
        for poemCount in range(len(inputs['input'])):
            poem = []
            for count in range(15):
                search = inputs['input'][poemCount][count]
                search = search.replace('\ufeff', '')

                if search != 'PAD':
                    # print(search)
                        index = dictionary[search]
                        # [i for i, word in reverse_dictionary.items() if word == search]
                        if index != None:

                            # print(index)
                            poem = np.concatenate((poem, final_embeddings[index]))
                            # print(poem.shape)
                        else:
                            print(search)
                            # print(poem)

                else:
                    poem = np.concatenate((poem, np.zeros(22)))
            inputs2.append(poem)
        graph = tf.Graph()
        with graph.as_default():
            wordCount = 15
            cateDimension = 17
            weightColumn1 = 22
            weightColumn2 = 64
            weightRow = 3
            features1 = 64
            features2 = 64

            sess = tf.InteractiveSession()
            pooled_outputs = []
            x = tf.placeholder(tf.float32, shape=[None, wordCount * weightColumn1])
            y_ = tf.placeholder(tf.float32, shape=[None, cateDimension])
            # y_ = tf.placeholder(tf.float32, shape=[None, cateDimension])
            for i, filter_size in enumerate([2, 3, 4]):
                l2_loss = tf.constant(0.0)
                l2_reg_lambda = 0.0
                with tf.name_scope("conv-maxpool-%s" % filter_size):
                    # Convolution Layer
                    filter_shape = [filter_size, weightColumn1, 1, features1]
                    W = tf.Variable(tf.truncated_normal(filter_shape, stddev=0.1), name="W")
                    b = tf.Variable(tf.constant(0.1, shape=[features1]), name="b")

                    # print(x.get_shape())
                    # print(W.get_shape())
                    x_image = tf.reshape(x, [-1, wordCount, weightColumn1, 1])
                    conv = tf.nn.conv2d(x_image, W, strides=[1, 1, 1, 1], padding='VALID')

                    # Apply nonlinearity

                    h = tf.nn.relu(tf.nn.bias_add(conv, b), name="relu")
                    # Maxpooling over the outputs
                    pooled = tf.nn.max_pool(
                        h,
                        ksize=[1, 15 - filter_size + 1, 1, 1],
                        strides=[1, 1, 1, 1],
                        padding='VALID',
                        name="pool")
                    pooled_outputs.append(pooled)

            # Combine all the pooled features
            num_filters_total = features1 * len([2, 3, 4])
            print(pooled_outputs)

            # h_pool = tf.concat(3, pooled_outputs)
            h_pool = tf.concat(pooled_outputs, 3)
            h_pool_flat = tf.reshape(h_pool, [-1, num_filters_total])

            # Add dropout
            with tf.name_scope("dropout"):
                keep_prob = tf.placeholder(tf.float32)

                h_drop = tf.nn.dropout(h_pool_flat, keep_prob)

            # Final (unnormalized) scores and predictions
            with tf.name_scope("output"):
                W = tf.get_variable(
                    "W",
                    shape=[num_filters_total, cateDimension],
                    initializer=tf.contrib.layers.xavier_initializer())
                b = tf.Variable(tf.constant(0.1, shape=[cateDimension]), name="b")
                l2_loss += tf.nn.l2_loss(W)
                l2_loss += tf.nn.l2_loss(b)
                # scores = tf.nn.xw_plus_b(h_drop, W, b, name="scores")
                scores = tf.nn.relu(tf.nn.xw_plus_b(h_drop, W, b, name="scores"))
                # predictions = tf.argmax(scores, 1, name="predictions")

            # CalculateMean cross-entropy loss
            with tf.name_scope("loss"):
                losses = tf.nn.softmax_cross_entropy_with_logits(logits=scores, labels=y_)
                loss = tf.reduce_mean(losses) + l2_reg_lambda * l2_loss

            correct_prediction = tf.equal(tf.argmax(scores, 1), tf.argmax(y_, 1))
            train_step = tf.train.AdamOptimizer(1e-4).minimize(losses)  #######///
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))  ########///

            saver = tf.train.Saver()  # Gets all variables in `graph`.
            with tf.Session(graph=graph) as sess:
                saver.restore(sess, 'model.ckpt')
                p = sess.run(tf.argmax(scores, 1), feed_dict={x: inputs2, keep_prob: 1.0})
            print(cut)
            print(sentence)
            print(p)

def qq():
   for i in readFile1():
       ran(i)


qq()
