import random, sys, string, os, pickle, json
import utils

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
        if mutation == '' and random.random()>0.1:
            continue
        negrawlp.write(geneName+'\t'+mutation+'\t'+cancer+'\t'+pubmed+'\n')

def downloadNegPub(sourcepath):
    negrawlp = open(sourcepath+'labelPairNeg')
    while True:
        line = newgrawlp.readline()
        if line == '':
            break
        secs = line.strip('\n').split('\t')
        geneName = secs[0]
        pubmed = secs[-1]
        batchList.append(pubmed)
        if len(batchList) > BATCH_NUM:
            downloadById(sourcepath)
            batchList = []
    if len(batchList)>0:
        downloadById(sourcepath)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print ('usage: genepkl reversepkl downloadpath cookedpath labelpairpos')
        exit()
    gene_dict, gene_reverse_dict = pickle.load(open(sys.argv[1])), pickle.load(open(sys.argv[2]))
    lp = sys.argv[5]
    negReport = sys.argv[6]
    sourcepath = sys.argv[3]
    targetpath = sys.argv[4]
    total_replaced = 0
    pubPos, posGene = loadPosLP(lp)
    createNegLP(negReport)
    downloadNegPub(sourcepath)
    print(posGene)
    lp = open(sourcepath+'labelPairNeg')
    successlp = open(targetpath+'labelPairNeg')
    for line in lp.readlines():
        word = []
        count = 0
        line = line.strip('\n').split() #gene1 gene2 cancer pubmedid
        gene1, mutation, cancer = line[0], line[1], line[2]
        pubmedid = line[3]
        if pubmedid in pubPos:
            continue
        with open(sourcepath+pubmedid) as p:
            word += remove_punc(p.readline()).split()
            word += remove_punc(p.readline()).split()
        outwords, count = replacePubMed(gene_dict, gene_reverse_dict, words)
        g1e, g2e = False, False
        for ow in outwords:
            if gene1 == ow:
                g1e = True
            elif ow in gene_dict:
                g2e = True
                gene2 = ow
        if not g1e or not  g2e:
            continue
        sucesslp.write(gene1+'\t'+gene2+'\t'+cancer+'\t'+pubmedid+'\t'+mutation+'\n')
        with open(targetpath+pubmedid, 'w') as of:
           for ow in outwords:
              of.write(ow+' ')
        total_replaced += count
        print("%s read with length %d - %d replacements made" % (pubmedid, len(word), count))
    print("%d total replacements made. Here are the top 50:" % total_replaced)

