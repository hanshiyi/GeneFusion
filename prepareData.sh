#!/bin/bash
#SBATCH -t 24:00:00
#SBATCH -o download_pubmed_JOB%j.out
#SBATCH -n 4 --mem=12GB

curDir=`pwd`
rawData=${curDir}/data/rawpos/
processedData=${curDir}/data/processed/
pkls=${curDir}/pkls/
mkdir ${curDir}/data
mkdir ${rawData}
mkdir -r ${processedData}
source /users/shan43/data/shan43/venv2/bin/activate
fusionPair=${curDir}/data/CosmicFusionExport.tsv

#python ${curDir}/src/utils.py $fusionPair $rawData

#python ${curDir}/src/filter_pair.py ${rawData}labelPairRaw ${rawData}noAbsList ${rawData}labelPairPure

##Hugo format:  Approved symbol>Previous symbols>---Pubmed IDs>-Synonyms
#python ${curDir}/src/parse_hugo.py  ${curDir}/data/Hugo.txt ${pkls}

#usage: genepkl reversepkl sourcepath targetpath labelpair
#python ${curDir}/src/preprocessPos.py ${pkls}gene_dict.pkl ${pkls}reverse_gene_dict.pkl ${rawData} ${processedData} ${rawData}labelPairPure

#usage: genepkl reversepkl downloadpath cookedpath labelpairpos
#python ${curDir}/src/preprocessNeg.py ${pkls}gene_dict.pkl ${pkls}reverse_gene_dict.pkl ${rawData} ${processedData} ${processedData}labelPairPos ${curDir}/data/CosmicCompleteTargetedScreensMutantExport.tsv

python ${curDir}/src/getVocab.py ${processedData}labelPairPos ${processedData}labelPairNeg ${processedData}

#python ${curDir}/src/w2v_pretrain.py ${pkls}gene_dict.pkl ${pkls}reverse_gene_dict.pkl ${rawData} ${processedData} ${processedData}vocab.txt ${curDir}/data/CosmicCompleteTargetedScreensMutantExport.tsv
