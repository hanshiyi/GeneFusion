import sys, string, os, pickle, json
import random
from utils import *

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print ('usage: genepkl reversepkl sourcepath targetpath labelpair')
        exit()
    gene_dict, gene_reverse_dict = pickle.load(open(sys.argv[1])), pickle.load(open(sys.argv[2]))
    lp = open(sys.argv[5])
    sourcepath = sys.argv[3]
    targetpath = sys.argv[4]
    total_replaced = 0
    for line in lp.readlines():
        words = []
        line = line.strip('\n').split() #gene1 gene2 cancer pubmedid
        gene1, gene2, cancer = line[0], line[1], line[2]
        pubmedid = line[3]
        with open(sourcepath+pubmedid) as p:
            words += remove_punc(p.readline()).split()
            words += remove_punc(p.readline()).split()
        outwords, count = replacePubMed(gene_dict, gene_reverse_dict, words)
        with open(targetpath+pubmedid, 'w') as of:
            #of.write(gene1+'\t'+gene2+'\t'+cancer+'\n')
            for ow in outwords:
                of.write(ow+' ')
        total_replaced += count
        print("%s read with length %d - %d replacements made" % (pubmedid, len(words), count))

    print("%d total replacements made. Here are the top 50:" % total_replaced)
    lp = open(sys.argv[5])
    poslp = open(targetpath+'labelPairPos', 'w')
    for ll in lp.readlines():
        line = ll.strip('\n').split() #gene1 gene2 cancer pubmedid
        gene1, gene2, cancer = line[0], line[1], line[2]
        pubmedid = line[3]
        with open(targetpath+pubmedid) as f:
            g1e, g2e = False, False
            for arline in f.readlines():
                arline = arline.split()
                for aw in arline:
                    if aw == gene1:
                        g1e = True
                    if aw == gene2:
                        g2e = True
            if g1e and g2e:
                poslp.write(ll)
