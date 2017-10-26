#!/bin/sh

ori_val_en='./ai_challenger/ai_challenger_translation_validation_20170912/translation_validation_20170912/valid.en-zh.en.sgm'
ori_val_zh='./ai_challenger/ai_challenger_translation_validation_20170912/translation_validation_20170912/valid.en-zh.zh.sgm'
val='./data/val/'
train='./data/train/'

batch_size=8
encoder_layer=1
decoder_layer=1
encode_size=100
decode_size=100
embedding_size=100
num_iter=100

##parse val dataset
#python prep_data.py $ori_val_en > ${val}"val.en"
#python prep_data.py $ori_val_zh > ${val}"val.zh"

##process data and generate en_dic, zh_dic, dataset and dataset config information
#python process_data.py $val 'true' > ./data/zh_statistics/zh_dic.val
#python process_data.py $train 'true' > ./data/zh_statistics/zh_dic.train
#python process_data.py $train 'true'

##vectorize dataset(batch) and generate mask(batch) 
#python gen_dataset.py $train $batch_size

##train model
python train.py