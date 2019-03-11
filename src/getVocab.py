import sys


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
    for can in cancerdic:
        if cancerdic[can] > 50:
            cancertype+=1
    for line in lpPos:
        line = line.strip('\n').split('\t')
        if cancerlist[line[2]] < 50:
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
    worddic = {}
    for id in pubmedids:
        with open(outpath+id) as file:
            for word in file.readline().split():
                worddic[word] = worddic.get(word,0) + 1
    vocab = open(outpath + 'vocab.txt','w')
    for word in worddic:
        if worddic[word] > 5 or word in geneList:
            vocab.write(word+'\t'+str(worddic[word])+'\n')
    vocab.close()


if __name__ == '__main__':
    labelPos = sys.argv[1]
    labelNeg = sys.argv[2]
    outpath = sys.argv[3]
    extractVocab(labelPos, labelNeg, outpath)
