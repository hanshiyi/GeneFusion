#########################################################################
## File Name: downloadData.sh
## Author: hanshiyi
## Mail: hanshiyi123@gmail.com
## Created Time: Thu 21 Feb 2019 12:03:03 AM EST
#########################################################################
#!/bin/bash
#SBATCH -t 24:00:00
#SBATCH -o download_pubmed_JOB%j.out
#SBATCH -n 4 --mem=12GB

curDir=`pwd`
rawData=${curDir}/data/rawpos/
processedData=${curDir}/data/processedpos/
pkls=${curDir}/pkls/
mkdir ${curDir}/data
mkdir ${rawData}
mkdir -r ${processedData}

fusionPair=${curDir}/data/CosmicFusionExport.tsv

#python ${curDir}/src/utils_api.py $fusionPair $rawData

#python ${curDir}/src/filter_pair.py ${rawData}labelPairRaw ${rawData}noAbsList ${rawData}labelPairPure

##Hugo format:  Approved symbol>Previous symbols>---Pubmed IDs>-Synonyms
#python ${curDir}/src/parse_hugo.py  ${curDir}/data/Hugo.txt ${pkls}
#usage: genepkl reversepkl sourcepath targetpath labelpair
python ${curDir}/src/preprocessPos.py ${pkls}gene_dict.pkl ${pkls}reverse_gene_dict.pkl ${rawData} ${processedData} ${rawData}labelPairPure
#usage: genepkl reversepkl downloadpath cookedpath labelpairpos
python ${curDir}/src/preprocessNeg.py ${pkls}gene_dict.pkl ${pkls}reverse_gene_dict.pkl ${rawData} ${processedData} ${processedData}labelPairPos ${curDir}/data/CosmicCompleteTargetedScreensMutantExport.tsv
/
