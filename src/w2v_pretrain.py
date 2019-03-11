import gensim, random, sys, string, os, pickle, json
from gensim.models import Word2Vec
from os import listdir
from os.path import isfile, join
from utils import *

def loadPosLP(lp):
    lp = open(lp)
    pubPos = []
    posGene = []
    for line in lp.readlines():
        line = line.strip('\n').split()
        if line[0] not in posGene:
            posGene.append(line[0])
        if line[1] not in posGene:
            posGene.append(line[1])
        pubPos.append(line[-1])
    return pubPos, posGene

def createNegLP(negReport):
    negReport = open(negReport)
    negReport.readline()
    negrawlp = open(sourcepath+'labelPairNeg','w')
    while True:
        line = negReport.readline()
        if line == '':
            break
        secs = line.split('\t')
        geneName = secs[0]
        if geneName not in posGene:
            continue
        pubmed = secs[30]
        mutation = secs[19]
        cancer = secs[7]
        #if mutation == '' and random.random()>0.1:
        #    continue
        negrawlp.write(geneName+'\t'+mutation+'\t'+cancer+'\t'+pubmed+'\n')

def downloadNegPub(sourcepath):
    batchList = []
    BATCH_NUM = 150
    dic = {}
    negrawlp = open(sourcepath+'labelPairNeg')
    while True:
        line = negrawlp.readline()
        if line == '':
            break
        secs = line.strip('\n').split('\t')
        geneName = secs[0]
        pubmed = secs[-1]
        if len(pubmed)>0 and pubmed not in dic:
            batchList.append(pubmed)
            dic[pubmed] = 0
        if len(batchList) > BATCH_NUM:
            downloadById(sourcepath, batchList, dic)
            batchList = []
    if len(batchList)>0:
        downloadById(sourcepath, batchList, dic)
    return dic

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print ('usage: genepkl reversepkl downloadpath cookedpath labelpairpos')
        exit()
    gene_dict, gene_reverse_dict = pickle.load(open(sys.argv[1])), pickle.load(open(sys.argv[2]))
    vocab = open(sys.argv[5])
    vocab = [line.strip('\n').split('\t')[0] for line in vocab.readlines()]
    sourcepath = sys.argv[3]
    targetpath = sys.argv[4]
    sourcefiles = [join(sourcepath,f) for f in listdir(sourcepath) if isfile(join(sourcepath, f)) and 'label' not in f]
    total_replaced = 0
    print(len(sourcefiles))
    '''corpus = open(targetpath+'w2vcorpus.txt','w')
    for sfile in sourcefiles:
        words = []
        count = 0
        with open(sfile) as p:
            words += remove_punc(p.readline()).split()
            words += remove_punc(p.readline()).split()
        outwords, count = replacePubMed(gene_dict, gene_reverse_dict, words)
        for ow in outwords:
          if ow in vocab:
            corpus.write(ow+' ')
        corpus.write('\n')
        total_replaced += count
        print("%s read with length %d - %d replacements made" % (sfile, len(words), count))
    print("%d total replacements made. Here are the top 50:" % total_replaced)'''
    corpus = open(targetpath+'w2vcorpus.txt')
    sens = []
    for line in corpus:
        sens.append(line.strip('\n').split())
    model = Word2Vec(min_count=1, size=64, window=10, negative=20, seed=1234, workers=4)
    test_vocab = model.build_vocab(corpus_file=targetpath+'w2vcorpus.txt')
    model.train(sentences=sens,epochs=100, total_examples=7246)
    model.wv.save(targetpath+'w2v.txt')
