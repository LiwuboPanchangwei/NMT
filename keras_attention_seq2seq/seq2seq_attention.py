#-*- coding:utf-8 -*-

from numpy import array
from numpy import argmax
from numpy import array_equal
from keras.models import Sequential
from keras.layers import LSTM
from attention_decoder import AttentionDecoder


n_features = 50
n_timesteps_in = 5
n_timesteps_out = 2
vocab_size = 10000
embedding_dim = 128

model = Sequential()
model.add(Embedding(vocab_size, embedding_dim, input_length=n_timesteps_in))
model.add(LSTM(150, input_shape=(n_timesteps_in, embedding_dim), return_sequences=True))
model.add(AttentionDecoder(150, n_features))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])

model.summary()
