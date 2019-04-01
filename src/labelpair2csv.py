import sys
import csv
import glob
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("lp_files", help="The label pair need to be converted")
parser.add_argument("dir2pubmed", help="The directory to the place for pubmed articles")
parser.add_argument('out_path', help="The path to store finaltraining data")
args = parser.parse_args()

def main():
    lp_files = sorted(glob.glob(args.lp_files))
    outpath = args.out_path
    pubids = []
    for lp_file in lp_files:
        lp = open(lp_file)
        print(lp_file)
        print(lp_file[lp_file.find('labelPair'):])
        out_file = open(outpath + lp_file[9+lp_file.find('labelPair'):]+'.csv', 'w')
        writer = csv.writer(out_file, delimiter='\t')
        for line in lp.readlines():
            line = line.strip('\n').split('\t')
            gene1, gene2, rel, pubmedid = line[0], line[1], line[2], line[3]
            tep = open(args.dir2pubmed+pubmedid).readline().strip('\n').split()
            if pubmedid not in pubids:
                pubids.append(pubmedid)
            gene1_occ = [i for i, w in enumerate(tep)
                    if w == gene1]
            gene1_start = ":".join([str(i) for i in gene1_occ])
            gene1_end = ":".join([str(i+1) for i in gene1_occ])
            gene2_occ = [i for i, w in enumerate(open(args.dir2pubmed+pubmedid).readline().strip('\n').split()) if w == gene2]
            gene2_start = ":".join([str(i) for i in gene2_occ])
            gene2_end = ":".join([str(i+1) for i in gene2_occ])
            text = open(args.dir2pubmed+pubmedid).readline().strip('\n')
            writer.writerow([gene1, 'Gene', gene1, gene1_start, gene1_end,
                gene2, 'Gene', gene2, gene2_start, gene2_end,
                pubmedid, rel, text])
        out_file.close()
    cancerlist = [line.strip('\n').split('_') for line in open(args.dir2pubmed+'rel.txt').readlines()]
    genelist = [line.strip('\n').split('\t')[0] for line in open(args.dir2pubmed+'gene_list.txt').readlines()]
    #print(genelist)
    if 'Train' in args.lp_files:
        nerfile = open(outpath + 'ner_train.txt', 'w')
    else:
        nerfile = open(outpath + 'ner_test.txt', 'w')
    for pubid in pubids:
        content = open(args.dir2pubmed+pubid).readline().strip('\n').split()
        for widx, w in enumerate(content):
            if w in genelist:
                nerfile.write('%s\t%s\t%s\t%s\n' % (w,'B-GENE',str(genelist.index(w)),pubid))
            else:
                nerfile.write('%s\t%s\t%s\t%s\n' % (w, 'O', '-1', pubid))
        nerfile.write('\n')
    nerfile.close()


if __name__ == '__main__':
    main()
