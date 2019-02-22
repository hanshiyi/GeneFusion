from bs4 import BeautifulSoup
import pickle,sys,string
import urllib

BATCH_NUM = 150
batchList = []
dic = {}

def remove_punc(s):
    return s.translate(string.maketrans('!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~', ' '*(len(string.punctuation)-1)))

def replacePubMed(gene_dict, gene_reverse_dict, words):
    outwords = []
    count = 0
    for i, w in enumerate(words):
        if '-' in w and w not in gene_dict:
            for sw in w.split('-'):
               if sw in gene_reverse_dict:
                   outwords.append(gene_reverse_dict[sw])
                   count+=1
               else:
                   outwords.append(sw)
        elif w in gene_reverse_dict:
            outwords.append(gene_reverse_dict[w])
            count += 1
        elif w in gene_dict:
            outwords.append(w)
        else:
            outwords.append(w.lower())
    return outwords, count


def downloadById(outPath):
    global batchList
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id='
    for pubid in batchList[:-1]:
        url+=pubid
        url+=','
    url+=batchList[-1]
    url +='&retmode=abstract&rettype=xml'
    soup = BeautifulSoup(urllib.urlopen(url).read(), 'lxml-xml')
    article = soup.findAll('PubmedArticle')
    print(len(batchList))
    #print(len(article))
    for idx, art in enumerate(article):
        medId = art.find('PMID').string
        title = art.find('ArticleTitle')
        abstract = art.find('AbstractText')
        if abstract is None or abstract.string is None:
            continue
        dic[medId] = 1
        #print(title)
        with open(outPath+medId, 'w') as file:
            file.write(title.string.encode('utf-8')+'\n')
            file.write(abstract.string.encode('utf-8') + '\n')
    batchList = []


def loadTSVAD(file_name, outPath):
    file = open(file_name)
    global batchList
    global BATCH_NUM
    global dic
    file.readline()
    count = 0
    labelPairFile = open(outPath+'labelPairRaw','w')
    for line in file.readlines():
        secs = line.split('\t')
        #print(secs[11])
        if len(secs[11])>0:
            count += 1
            labelPairFile.write(secs[11]+'\t'+secs[2]+'\t'+secs[-2]+'\n')
            if secs[-2] not in dic:
                dic[secs[-2]] = 0
                batchList.append(secs[-2])
        if len(batchList) == BATCH_NUM:
            #print(batchList)
            downloadById(outPath)
            print(count)
    if len(batchList) > 0:
        downloadById(outPath)
    noabs = open(outPath+'noAbsList','w')
    for pubmedid in dic:
        if dic[pubmedid] == 0:
            noabs.write(pubmedid+'\n')
    #print(count)

def loadNEG(file_name, outPath):
    file = open(file_name)
    global batchList
    global BATCH_NUM
    global dic
    file.readline()
    count = 0
    id2gene = {}
    for line in file.readlines():
        secs = line.split('\t')
        #print(secs[11])
        if len(secs[3])>0:
            count += 1
            ids = secs[2].split(', ')
            for pid in ids:
                id2gene[pid] = secs[0]
                batchList.append(pid)
        if len(batchList) == BATCH_NUM:
            #print(batchList)
            downloadById(outPath)
            print(count)
    if len(batchList) > 0:
        downloadById(outPath)
    pickle.dump(id2gene, open('pkls/id2geneneg.pkl','w'))
    #print(count)

if __name__=='__main__':
    loadTSVAD(sys.argv[1], sys.argv[2])
    #loadNEG(sys.argv[1], sys.argv[2])
    #downloadById('','',sys.argv[1], sys.argv[2])
