import sys
import random
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("lpPos", help="positive label pair file")
parser.add_argument("lpNeg", help="negative label pair file")
parser.add_argument("outpath", help="output path")
parser.add_argument("--threshold_rel", help="the threshold for cancer type", type=int, default=50)
parser.add_argument("--train_ratio", help="train and test ration", type=float, default=0.8)
parser.add_argument("--threshold_word", help="the threshold for minimum word count", type=int , default=5)
args = parser.parse_args()

def extractVocab(labelPos, labelNeg, outpath):
    lpPos = open(labelPos)
    lpNeg = open(labelNeg)
    pubmedids = []
    geneList = []
    cancerdic = {}
    for line in lpPos:
        line = line.strip('\n').split('\t')
        cancerdic[line[2]] = cancerdic.get(line[2],0)+1
    cancertype = 0
    cancer_file = open(outpath+'rel.txt', 'w')
    for can in cancerdic:
        if cancerdic[can] > args.threshold_rel:
            cancer_file.write(can+'\n')
            cancertype+=1
    cancer_file.write('NOT_FUSION')
    lpPos = open(labelPos)
    for line in lpPos:
        line = line.strip('\n').split('\t')
        if cancerdic[line[2]] < args.threshold_rel:
            continue
        if line[3] not in pubmedids:
            pubmedids.append(line[3])
        if line[0] not in geneList:
            geneList.append(line[0])
        if line[1] not in geneList:
            geneList.append(line[1])
    print('cancertype:\t' + str(cancertype))
    for line in lpNeg:
        line = line.strip('\n').split('\t')
        if line[3] not in pubmedids:
            pubmedids.append(line[3])
        if line[0] not in geneList:
            geneList.append(line[0])
        if line[1] not in geneList:
            geneList.append(line[1])
    worddic = {}
    for id in pubmedids:
        with open(outpath+id) as file:
            for word in file.readline().split():
                worddic[word] = worddic.get(word,0) + 1
    vocab = open(outpath + 'vocab.txt','w')
    widx = 2
    vocab.write('<PAD>\t0\n')
    vocab.write('<UNK>\t1\n')
    #print(geneList)
    for word in worddic:
        if worddic[word] > args.threshold_word or word in geneList:
            vocab.write(word+'\t'+str(widx)+'\n')
            widx += 1
    vocab.close()
    gene_file = open(outpath+'gene_list.txt', 'w')
    gene_file.write('<UNK>\t0\n')
    for idx, gene in enumerate(geneList):
        gene_file.write(gene+'\t'+str(idx+1)+'\n')
    gene_file.close()
    lppos = open(labelPos)
    trainlppos = open(outpath+'labelPairPosTrain', 'w')
    testlppos = open(outpath+'labelPairPosTest', 'w')
    for line in lppos.readlines():
        cancer = line.split('\t')[2]
        if cancerdic[cancer] < args.threshold_rel:
            continue
        if random.random()<args.train_ratio:
            trainlppos.write(line)
        else:
            testlppos.write(line)
    lpneg = open(labelNeg)
    trainlpneg = open(outpath+'labelPairNegTrain', 'w')
    testlpneg = open(outpath+'labelPairNegTest', 'w')
    for line in lpneg.readlines():
        if random.random()<args.train_ratio:
            trainlpneg.write(line)
        else:
            testlpneg.write(line)
    ne_file = open(outpath+'ner_labels.txt', 'w')
    ne_file.write('<PAD>\t0\n')
    ne_file.write('<END>\t1\n')
    ne_file.write('<START>\t2\n')
    ne_file.write('B-GENE\t3\n')
    ne_file.write('I-GENE\t4\n')
    ne_file.close()


if __name__ == '__main__':
    labelPos = args.lpPos
    labelNeg = args.lpNeg
    outpath = args.outpath
    extractVocab(labelPos, labelNeg, outpath)
