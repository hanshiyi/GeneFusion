#!/bin/bash
#SBATCH -t 24:00:00
#SBATCH -o download_pubmed_JOB%j.out
#SBATCH -n 4 --mem=12GB

curDir=`pwd`
rawData=${curDir}/data/rawpos/
processedData=${curDir}/data/processed/
pkls=${curDir}/pkls/
finalDir=${curDir}/data/protos/
mkdir ${curDir}/data
mkdir ${rawData}
mkdir -r ${processedData}
mkdir ${finalDir}
fusionPair=${curDir}/data/CosmicFusionExport.tsv
max_len=50000
min_count=5

#python ${curDir}/src/utils.py $fusionPair $rawData

#python ${curDir}/src/filter_pair.py ${rawData}labelPairRaw ${rawData}noAbsList ${rawData}labelPairPure

##Hugo format:  Approved symbol>Previous symbols>---Pubmed IDs>-Synonyms
#python ${curDir}/src/parse_hugo.py  ${curDir}/data/Hugo.txt ${pkls}

#usage: genepkl reversepkl sourcepath targetpath labelpair
#python ${curDir}/src/preprocessPos.py ${pkls}gene_dict.pkl ${pkls}reverse_gene_dict.pkl ${rawData} ${processedData} ${rawData}labelPairPure

#usage: genepkl reversepkl downloadpath cookedpath labelpairpos
#python ${curDir}/src/preprocessNeg.py ${pkls}gene_dict.pkl ${pkls}reverse_gene_dict.pkl ${rawData} ${processedData} ${processedData}labelPairPos ${curDir}/data/CosmicCompleteTargetedScreensMutantExport.tsv

#python ${curDir}/src/getVocab.py ${processedData}labelPairPos ${processedData}labelPairNeg ${processedData}
#mv ${processedData}/pubmedid_train.txt  ${finalDir}/pubmedid_train.txt
#python ${curDir}/src/w2v_pretrain.py ${pkls}gene_dict.pkl ${pkls}reverse_gene_dict.pkl ${rawData} ${processedData} ${processedData}vocab.txt ${curDir}/data/CosmicCompleteTargetedScreensMutantExport.tsv


#python ${curDir}/src/labelpair2csv.py ${processedData}labelPair\*Train\* ${processedData} ${finalDir}
#python ${curDir}/src/labelpair2csv.py ${processedData}labelPair\*Test\* ${processedData} ${finalDir}

python ${curDir}/src/labeled_tsv_to_tfrecords.py --text_in_files ${finalDir}/\*.csv --out_dir ${finalDir} --max_len ${max_len} --num_threads 10 --multiple_mentions --tsv_format --min_count ${min_count} 
python ${curDir}/src/ner_to_tfrecords.py --in_files ${finalDir}/ner_t\*.txt --out_dir ${finalDir} --load_vocab ${finalDir} --num_threads 5



