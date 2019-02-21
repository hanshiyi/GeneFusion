import sys, os, pickle, json


def get_gene_dictionary(path):

    gene_json = json.load(open(path, 'r'))
    gene_list = gene_json.get('response').get('docs')
    gene_dict = {}
    gene_reverse_dict = {}
    print("Gene List parsed with %d entries" % len(gene_list))
    for g in gene_list:
        gene_symbol = g.get('symbol').replace('.', '').replace("'", "")
        gene_dict[gene_symbol] = []
        for a in g.get('alias_symbol', []):
            alternate = a.replace('.', '').replace("'", "")
            if len(alternate) < 3:
                continue
            gene_dict[gene_symbol].append(alternate)
            gene_reverse_dict[alternate] = gene_symbol
        for a in g.get('prev_symbol', []):
            alternate = a.replace('.', '').replace("'", "")
            if len(alternate) < 3:
                continue
            gene_dict[gene_symbol].append(alternate)
            gene_reverse_dict[alternate] = gene_symbol
    return gene_dict, gene_reverse_dict

def get_from_hugo(path):
    hugo = open(path)
    hugo.readline()
    dic = {}
    reversedic = {}
    for line in hugo.readlines():
        line = line.strip('\n').split('\t')
        if line[0] not in dic:
            dic[line[0]] = []
            for syn in line[3].split(', '):
                dic[line[0]].append(syn)
                reversedic[syn] = line[0]
            #print(dic[line[0]])
    return dic,reversedic

if __name__ == "__main__":
    gene_dict, gene_reverse_dict = get_from_hugo(sys.argv[1])
    pkls_foler = sys.argv[2]
    pickle.dump(gene_dict, open(pkls_foler+'gene_dict.pkl','w'))
    pickle.dump(gene_reverse_dict, open(pkls_foler+'reverse_gene_dict.pkl','w'))
    exit()
