from __future__ import print_function
from hyperparams import Hyperparams as hp
import tensorflow as tf
import numpy as np
from prepro import *
from data_load import load_vocab, load_test_data, load_test_string
from train import Graph
import codecs
import distance
import os



#Evaluate on testing batches
def main_batches():  
    g = Graph(is_training=False)
    
    # Load data
    nums, X, ys = load_test_data()
    pnyn2idx, idx2pnyn, hanzi2idx, idx2hanzi = load_vocab()
    
    with g.graph.as_default():    
        sv = tf.train.Supervisor()
        with sv.managed_session(config=tf.ConfigProto(allow_soft_placement=True)) as sess:
            # Restore parameters
            sv.saver.restore(sess, tf.train.latest_checkpoint(hp.logdir)); print("Restored!")

            # Get model
            mname = open(hp.logdir + '/checkpoint', 'r').read().split('"')[1] # model name
            
            with codecs.open('eval/{}_{}.csv'.format(mname, "qwerty" if hp.isqwerty else "nine"), 'w', 'utf-8') as fout:
                fout.write("NUM,EXPECTED,{}_{},# characters,edit distance\n".format(mname, "qwerty" if hp.isqwerty else "nine"))
                
                total_edit_distance, num_chars = 0, 0
                for step in range(len(X)//hp.batch_size):
                    num = nums[step*hp.batch_size:(step+1)*hp.batch_size] #number batch
                    x = X[step*hp.batch_size:(step+1)*hp.batch_size] # input batch
                    y = ys[step*hp.batch_size:(step+1)*hp.batch_size] # batch of ground truth strings
                    
                    preds = sess.run(g.preds, {g.x: x})
                    for n, xx, pred, expected in zip(num, x, preds, y): # sentence-wise
                        #got = "".join(idx2hanzi[str(idx)] for idx in pred)[:np.count_nonzero(xx)].replace("_", "")
                        got = "".join(idx2hanzi[idx] for idx in pred)[:np.count_nonzero(xx)].replace("_", "")
                        edit_distance = distance.levenshtein(expected, got)
                        total_edit_distance += edit_distance
                        num_chars += len(expected)
                
                        fout.write(u"{},{},{},{},{}\n".format(n, expected, got, len(expected), edit_distance))
                fout.write(u"Total CER: {}/{}={},,,,\n".format(total_edit_distance, 
                                                        num_chars, 
                                                        round(float(total_edit_distance)/num_chars, 2)))
                                

#For user input test                
def main():  
    g = Graph(is_training=False)
    
    # Load vocab
    pnyn2idx, idx2pnyn, hanzi2idx, idx2hanzi = load_vocab()
    
    with g.graph.as_default():    
        sv = tf.train.Supervisor()
        with sv.managed_session(config=tf.ConfigProto(allow_soft_placement=True)) as sess:
            # Restore parameters
            sv.saver.restore(sess, tf.train.latest_checkpoint(hp.logdir)); print("Restored!")

            # Get model
            mname = open(hp.logdir + '/checkpoint', 'r').read().split('"')[1] # model name
            while True:
                line = input("请输入测试拼音：")
                if len(line) > hp.maxlen:
                    print('最长拼音不能超过50')
                    continue
                x = load_test_string(pnyn2idx, line)
                #print(x)
                preds = sess.run(g.preds, {g.x: x})
                #got = "".join(idx2hanzi[str(idx)] for idx in preds[0])[:np.count_nonzero(x[0])].replace("_", "")
                got = "".join(idx2hanzi[idx] for idx in preds[0])[:np.count_nonzero(x[0])].replace("_", "")
                print(got)

                                                                                                   
if __name__ == '__main__':
    main(); print("Done")

