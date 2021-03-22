# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 21:24:36 2021

@author: ting
"""

import pandas as pd
import numpy as np
import re
from gensim.models.word2vec import Word2Vec
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Embedding, GRU, Dense
from keras.models import Model, Input
from keras.layers import LSTM, Embedding, Dense, TimeDistributed, Dropout, Bidirectional

train_df = pd.read_csv('train.csv')
test_df = pd.read_csv('test.csv')
train_df['poi'] = train_df["POI/street"].str.split("/", n = 0, expand = True) [0]
train_df['street'] = train_df["POI/street"].str.split("/", n = 0, expand = True) [1]
    

# build dictionary
# tokenized
def addTag(column):
    tag = []
    err = [] # street can not be found in raw_data
    for x in range(0,len(train_df)):
        word = train_df.iloc[x,1].split()
        keyword = train_df.iloc[x,column]
        if train_df.iloc[x,column]!='' and train_df.iloc[x,column]!=' ':
            if len([i for i, e in enumerate(word) if e in keyword]) >0:
                start = [i for i, e in enumerate(word) if e in keyword][0]
                key_len = len(keyword.split())
            else:
                start = -1
                key_len = 0  
        else:
            start = -1
            key_len = 0   
        # 增加word list 的 tag存在temp裡 
        temp = []
        for i in range(0,len(word)):
            if i == start:           
                temp.append('B')
            elif i > start and i < start + key_len:
                temp.append('I')
            else:    
                temp.append('O')
        tag.append(temp)    
    return tag

# street tag
tag = addTag(4)
# poi tag
tag = addTag(3)

# create a list of all words in train_df and test_df
corpus = pd.concat([train_df.raw_address, test_df.raw_address]).sample(frac=1)
corpus = corpus.apply(lambda x: x.split(' ')).tolist()
corpus.append('pad')
model = Word2Vec(corpus)

embedding_matrix = np.zeros((len(model.wv.vocab.items()) + 1, model.vector_size))
word2idx = {}

vocab_list = [(word, model.wv[word]) for word, _ in model.wv.vocab.items()]
for i, vocab in enumerate(vocab_list):
    word, vec = vocab
    embedding_matrix[i + 1] = vec
    word2idx[word] = i + 1

def text_to_index(corpus):
    new_corpus = []
    for doc in corpus:
        new_doc = []
        for word in doc:
            try:
                new_doc.append(word2idx[word])
            except:
                new_doc.append(0)
        new_corpus.append(new_doc)
    return np.array(new_corpus)

# find the value of 'pad'
v = word2idx['pad']
PADDING_LENGTH = 40
X = text_to_index(train_df.raw_address.apply(lambda x: x.split(' ')).tolist())
X = pad_sequences(X, maxlen=PADDING_LENGTH, dtype='int32', value = v)


# create tags index
tags = ['O','B','I']
tag2idx = { t: i for i, t in enumerate(tags) }

def tag_to_index(corpus):
    new_corpus = []
    for doc in corpus:
        new_doc = []
        for word in doc:
            try:
                new_doc.append(tag2idx[word])
            except:
                new_doc.append(0)
        new_corpus.append(new_doc)
    return np.array(new_corpus)

Y = tag_to_index(tag)
Y = pad_sequences(pd.Series(Y), maxlen=PADDING_LENGTH, dtype='int32', value=0)

from keras.utils import to_categorical
Y = [to_categorical(i, num_classes=3) for i in Y]

# 建立雙向 LSTM 模型
def createModel(vocab_size, tag_size, max_len, emb_matrix=None):
    input = Input(shape=(max_len,))
    if emb_matrix is None:
        model = Embedding(input_dim=vocab_size, output_dim=100, input_length=max_len)(input)
    else:
        model = Embedding(input_dim=vocab_size, output_dim=100, weights=[emb_matrix], input_length=max_len, trainable=False)(input)
    model = Dropout(0.1)(model)
    model = Bidirectional(LSTM(units=100, return_sequences=True, recurrent_dropout=0.1))(model)
    out = TimeDistributed(Dense(tag_size, activation="softmax"))(model)  # softmax output layer

    model = Model(input, out)
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

    return model

# 建立雙向 LSTM 模型
model = createModel(len(word2idx)+1, 3, 40, embedding_matrix)

# 開始訓練
history = model.fit(X, np.array(Y), batch_size=32, epochs=3, validation_split=0.2, verbose=1)

# 將訓練好的模型存檔
model.save("ner_model.h5")
model.save("ner_model_poi.h5")

# 預測
# 載入已經訓練好的網路參數權重
model.load_weights("ner_model.h5")
model.load_weights("ner_model_poi.h5")

#  test_raw_address
raw_add = test_df.raw_address #keep this for the output
# test_df.raw_address = test_df.raw_address.str.replace('[^0-9a-zA-Z]+', ' ') 
X_test = text_to_index(test_df.raw_address.apply(lambda x: x.split(' ')).tolist())
X_test = pad_sequences(X_test, maxlen=PADDING_LENGTH, dtype='int32', value=v)

# 利用模型進行預測
p = model.predict(X_test, verbose=0)
p = np.argmax(p, axis=-1) # 取得預測出來機率最大的類別

# 還原 p 成原本的x_test長度
result = []  
test= test_df.raw_address.apply(lambda x: x.split(' ')).tolist()
for i in range(0,len(X_test)):
    origin_len = len(test[i])
    result.append( p[i][-origin_len:])

result_word = []
for i in range(0,len(result)):
    want = np.where(result[i] != 0)[0].tolist()
    result_word.append(
        pd.DataFrame(test[i]).iloc[want].transpose().loc[0].tolist()
        )
    
out = pd.DataFrame(list(zip(raw_add, result_word)), 
               columns =['raw_address', 'street']) 
out.to_csv('street.csv')

out = pd.DataFrame(list(zip(raw_add, result_word)), 
               columns =['raw_address', 'poi'])
out.to_csv('poi.csv')  

# output format
df = pd.read_csv('poi.csv')
df1 = pd.read_csv('street.csv')
df.poi = df.poi.apply(lambda x: x[1:-1])
df.poi = df.poi.apply(lambda x: x.replace(', ', ' '))
df.poi = df.poi.apply(lambda x: x.replace("'", ''))

df1.street = df1.street.apply(lambda x: x[1:-1])
df1.street = df1.street.apply(lambda x: x.replace(', ', ' '))
df1.street = df1.street.apply(lambda x: x.replace("'", ''))


output = df.poi + "/" + df1.street
pd.DataFrame(output).to_csv('output.csv',index_label = ['id','POI/street'], index=True)



