#import packages
import json
import torch
import torchtext
import numpy as np
import pandas as pd
from src import constants
from transformers import BertModel
from transformers.tokenization_bert import BertTokenizer

#csv paths
article_summary_path = f'{constants.CLEAN_DIR}/{constants.Text_Prefix}summary.csv'
image_summary_path = f'{constants.CLEAN_DIR}/{constants.Media_Prefix}summary.csv'
#read as df
df_article = pd.read_csv(article_summary_path)
df_image = pd.read_csv(image_summary_path)
#pretrained bert weights
print('loading pretrained bert model \n')
pretrained_weights = 'bert-base-uncased'
bert_tokenizer = BertTokenizer.from_pretrained(pretrained_weights)
bert_model = BertModel.from_pretrained(pretrained_weights)

# set up fields
preprocess_text = torchtext.data.Field(lower=True, \
                                       fix_length = 128,
                                       batch_first=True,
                                       truncate_first=True,
                                       tokenize = tokenizer.tokenize,
                                       pad_token='[PAD]',
                                       unk_token='[UNK]',
                                       init_token='[CLS]',
                                       eos_token='[SEP]')

test = df_article.summary.values[0]

print(bert_tokenizer.tokenize(test))

# print(bert_model().embeddings)
