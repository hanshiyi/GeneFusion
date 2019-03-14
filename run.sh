#!/bin/bash
export PYTHONPATH=. 
curDir=`pwd`
protos=${curDir}/data/protos
logDir=${curDir}/saved_models/`date +%Y-%m-%d-%H`/${RANDOM}_${RANDOM}
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
--embeddings ${curDir}/data/processed/w2v.txt \
--ner_prob 0.5 \
--ner_weight 10.0 \
--ner_test ${protos}/ner_test.txt.proto \
--ner_train ${protos}/ner_train.txt.proto \
--dropout_loss_weight 0 \
--word_unk_dropout 0.85 \
--beta1 .1 \
--beta2 .9 \
--kb_pretrain 0 \
--ner_batch 16 \
--text_batch 32 \
--kb_batch 16 \
--num_classes 2 \
--kb_vocab_size 2 \
--text_encoder transformer_cnn_all_pairs \
--position_dim 0 \
--epsilon=1e-4 \
--neg_noise=.20 \
--pos_noise=.33 \
--negative_test_test=${protos}/NegTest.csv.proto \
--positive_test_test=${protos}/PosTest.csv.proto \
--negative_test=${protos}/NegTrain.csv.proto \
--positive_test=${protos}/PosTrain.csv.proto \
--negative_train=${protos}/NegTrain.csv.proto \
--positive_train=${protos}/PosTrain.csv.proto \
--logdir=${logDir}
