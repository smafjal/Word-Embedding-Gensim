#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,codecs
import gensim, logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

corpus_path="corpus" # all files in this folder
new_corpus_path="new_corpus" # new corpus that is used for retrain the model
saved_model_path="saved_model" # where i save model
test_path=corpus_path+"/corpus_02.txt" # data for testing

def chomps(s):
    return s.rstrip('\n')

def get_unicode(input):
    input=chomps(input)
    if type(input) != unicode:
        input =  input.decode('utf-8')
        return input
    else:
         return input

# iterator that is used for read all files
# it return a list of each sentence by spliting it by space. it's memory efficient
class MySentences(object):
    def __init__(self,dirname):
        self.dirname=dirname
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname,fname)):
                lines=[x for x in line.split()]
                lines=[ get_unicode(x) for x in lines]
                yield lines

def train_model(path): # word-embedding code

    print '----[start embedding on data corpus ]---'

    # word2vec parameters
    min_count=1 # word frequency grater or equal 'min_count' can be embedded
    size=100 # word vector size.simply known as 'embedding size'
    workers=4 # number of threads
    window = 4 # contexual window

    # a memory-friendly iterator
    sentences = MySentences(path)
    model = gensim.models.Word2Vec(sentences,
        min_count=min_count,
        size=size,
        workers=workers,
        window=window
    )
    save_p=saved_model_path+'/model_corpus'
    model.save(save_p)
    return model,save_p

# assume model-trained file is saved on model_path
def retrain_model(model_path,corpus_path):
    sentences=MySentences(corpus_path)
    new_model = gensim.models.Word2Vec.load(model_path)
    new_model.train(sentences)
    return new_model

def read_file_for_test(path): # read test file
    sentences=[]
    with open(path,'r') as r:
        for x in r.readlines():
            words=[y for y in x.split()]
            words=[get_unicode(y) for y in words]
            sentences.append(words)
    return sentences

def output_test(model,path): # test model
    print "<>"*34
    words=read_file_for_test(path)

    # print first 2 words embedding-vector
    for i in range(min(2,len(words))):
        print "Words: ",words[i][0]," em-vec: ",model[words[i][0]]
        pass

    # print first 10 words embedding vectors similarity
    print "*"*80
    for i in range(min(10,len(words))):
        a=words[i][0]
        b=words[i+1][0]
        sim_vec=model.similarity(a,b)
        print "words-sim-vec between ",a," & ",b,"  ----->> ",sim_vec

def main():
    model,saved_model_path=train_model(corpus_path)
    print "Model Saved On: ",saved_model_path
    output_test(model,test_path)

    print "Load the model & retrain it by new data"
    model = retrain_model(saved_model_path,new_corpus_path)

if __name__=="__main__":
    main()

