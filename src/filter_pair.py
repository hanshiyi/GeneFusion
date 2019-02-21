import sys

def filterLP(lpraw, noabs, lppure):
    lpraw = open(lpraw)
    noabs = open(noabs)
    lppure = open(lppure, 'w')
    noabs = [line.strip('\n') for line in noabs.readlines()]
    pairset = []
    for line in lpraw.readlines():
        line = line.strip('\n').split('\t')
        pair = line[0].split('_')
        gene1 = ''
        gene2 = ''
        for item in pair:
            if '{' in item:
                gene1 = item[:item.find('{')]
                break
        for item in pair[::-1]:
            if '{' in item:
                gene2 = item[:item.find('{')]
                break
        #print(line[0])
        #print(gene1+' '+gene2)
        if line[2] not in noabs:
            ppp = gene1+'\t'+gene2+'\t'+line[1]+'\t'+line[2]+'\n'
            if ppp in pairset:
                continue
            pairset.append(ppp)
            lppure.write(ppp)



if __name__=='__main__':
    filterLP(sys.argv[1], sys.argv[2], sys.argv[3])
