import py
import sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("lp_file", help="The label pair need to be converted")
parser.add_argument("dir2pubmed", help="The directory to the place for pubmed articles")
args = parser.parse_args()

def main():
    lp = open(args.lp_file)
    out_file = open(args.dir2pubmed + args.lp_file[9:], 'w')
    writer = csv.writer(out_file, delimiter='\t')
    for line in lp.readlines():
        line = line.strip('\n').split('\t')
        gene1, gene2, rel, pubmedid = line[0], line[1], line[2], line[3]
        gene1_occ = [i for i, w in enumerate(open(args.dir2pubmed+pubmedid).readline().strip('\n').split() if w == gene1]
        gene1_start = ":".join([str(i) for i in gene1_occ])
        gene1_end = ":".join([str(i+1) for i in gene1_occ])
        gene2_occ = [i for i, w in enumerate(open(args.dir2pubmed+pubmedid).readline().strip('\n').split() if w == gene2]
        gene2_start = ":".join([str(i) for i in gene2_occ])
        gene2_end = ":".join([str(i+1) for i in gene2_occ])
        text = open(args.dir2pubmed+pubmedid).readline().strip('\n')
        writer.writerow([gene1, 'Gene', gene1, gene1_start, gene1_end,
            gene2, 'Gene', gene2, gene2_start, gene2_end,
            pubmedid, rel, text])
    out_file.close()


if __name__ == __main__:
    main()
