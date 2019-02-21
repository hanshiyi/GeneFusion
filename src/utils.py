from bs4 import BeautifulSoup
import sys
import urllib

def downloadById(pair, cancer_type, medId, outPath):
    url = 'https://www.ncbi.nlm.nih.gov/pubmed/'
    url = url + str(medId)
    soup = BeautifulSoup(urllib.urlopen(url), 'html.parser')
    title = soup.find_all('h1')
    abstract = soup.find_all('p')
    if abstract[9].string is None:
        return
    with open(outPath+str(medId), 'w', encoding='UTF-8') as file:
        file.write(pair+'\t' + cancer_type+'\n')
        file.write(title[1].string+'\n')
        file.write(abstract[9].string + '\n')

def loadTSVAD(file_name, outPath):
    file = open(file_name)
    file.readline()
    count = 0
    for line in file.readlines():
        secs = line.split('\t')
        print(secs[11])
        if len(secs[11])>0:
            count += 1
            downloadById(secs[11],secs[2],secs[-2],outPath)
    #print(count)

if __name__=='__main__':
    loadTSVAD(sys.argv[1], sys.argv[2])
    #downloadById(sys.argv[1], sys.argv[2])
