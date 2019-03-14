#!/bin/bash

curDir=`pwd`
protos=${curDir}/data/protos

python src/train.py \
--vocab_dir=${protos} \
--optimizer=adam \
--model_type=classifier \
--lr=.0005 --margin=1.0 --l2_weight=0 --word_dropout=.5 --lstm_dropout=.95 --final_dropout=.35 \
--clip_norm=10 --text_weight=1.0 --text_prob=1.0 --token_dim=64 --lstm_dim=64 --embed_dim=64 \
--kb_epochs=100000 --text_epochs=100000 --eval_every=15000 --max_seq=2000 --neg_samples=200 --random_seed=1111 \
--in_memory \
--bidirectional \
--train_dev_percent .85 \
--doc_filter /users/shan43/data/shan43/bran/data/cdr/CDR_pubmed_ids/CDR_Train_Dev_pubmed_ids.txt \
--noise_std 0.1 \
--block_repeats 2 \
--embeddings /users/shan43/data/shan43/bran/data/embeddings/just_train_2500_64d
--ner_prob 0.5
--ner_weight 10.0
--ner_test
/users/shan43/data/shan43/bran/data/cdr/processed/just_train_2500/protos/ner_CDR_dev.txt.proto
--ner_train
/users/shan43/data/shan43/bran/data/cdr/processed/just_train_2500/protos/ner_CDR_train.txt.proto
--dropout_loss_weight 0
--word_unk_dropout 0.85
--beta1 .1
--beta2 .9
--kb_pretrain 0
--ner_batch 16
--text_batch 32
--kb_batch 16
--num_classes 2
--kb_vocab_size 2
--text_encoder transformer_cnn_all_pairs
--position_dim 0
--epsilon=1e-4
--neg_noise=.20
--pos_noise=.33
--negative_test_test=/users/shan43/data/shan43/bran/data/cdr/processed/just_train_2500/protos/negative_*test_filtered.txt.proto
--positive_test_test=/users/shan43/data/shan43/bran/data/cdr/processed/just_train_2500/protos/positive_*test.txt.proto
--negative_test=/users/shan43/data/shan43/bran/data/cdr/processed/just_train_2500/protos/negative_*train*_filtered.txt.proto
--positive_test=/users/shan43/data/shan43/bran/data/cdr/processed/just_train_2500/protos/positive_*train*.txt.proto
--negative_train=/users/shan43/data/shan43/bran/data/cdr/processed/just_train_2500/protos/negative_*train*_filtered.txt.proto
--positive_train=/users/shan43/data/shan43/bran/data/cdr/processed/just_train_2500/protos/positive_*train*.txt.proto
--logdir=/users/shan43/data/shan43/bran/saved_models/cdr/relex/cdr_2500/2019-03-10-23//32023_9720
