import numpy as np 
import pandas as pd 
import os
import re
import gensim
import string
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from keras.preprocessing import text
from keras.utils import np_utils
from keras.preprocessing import sequence
import keras.backend as K
from keras.models import Sequential
from keras.layers import Dense, Embedding, Lambda
from keras.preprocessing.text import Tokenizer
import nltk
nltk.download('punkt')

corpus = ["".join([char for char in list(doc) if not (char in ponctuations)]) for doc in corpus]

tokenizer = text.Tokenizer()
tokenizer.fit_on_texts(d)
word2id = tokenizer.word_index


# build vocabulary of unique words
#word2id['PAD'] = 0
id2word = {v:k for k, v in word2id.items()}
wids = [[word2id[w] for w in text.text_to_word_sequence(doc)] for doc in corpus]

vocab_size = len(word2id)
#embed_size = 100
window_size = 2 # context window size

print('Vocabulary Size:', vocab_size)
print('Vocabulary Sample:', list(word2id.items()))

def generate_context_word_pairs(corpus, window_size, vocab_size):
    context_length = window_size*2
    for words in corpus:
        sentence_length = len(words)
        for index, word in enumerate(words):
            context_words = []
            label_word   = []            
            start = index - window_size
            end = index + window_size + 1
            
            context_words.append([words[i] 
                                 for i in range(start, end) 
                                 if 0 <= i < sentence_length 
                                 and i != index])
            label_word.append(word)

            x = sequence.pad_sequences(context_words, maxlen=context_length)
            y = np_utils.to_categorical(label_word, vocab_size)
            yield (x, y)
            
            
# Test this out for some samples
i = 0
for x, y in generate_context_word_pairs(corpus=wids, window_size=window_size, vocab_size=vocab_size):
    if 0 not in x[0]:
        print('Context (X):', [id2word[w] for w in x[0]], '-> Target (Y):', id2word[np.argwhere(y[0])[0][0]])
    
        if i == len(corpus):
            break
        i += 1

cbow = Sequential()
cbow.add(Embedding(input_dim=vocab_size, output_dim=100, input_length=window_size*2))
cbow.add(Lambda(lambda x: K.mean(x, axis=1), output_shape=(100,)))
cbow.add(Dense(vocab_size, activation='softmax'))
cbow.compile(loss='categorical_crossentropy', optimizer='rmsprop')

print(cbow.summary())
    
dimensions=100
vect_file = open('/Users/djouldebarry/Desktop/test/vectors.txt' ,'w') 
vect_file.write('{} {}\n'.format(vocab_size,dimensions))

weights = cbow.get_weights()[0]
for text, i in tokenizer.word_index.items():
    final_vec = ' '.join(map(str, list(weights[i-1,:])))
    #final_vec.append(map(str, list(weights[i,:])))
    vect_file.write('{} {}\n'.format(text, final_vec))
vect_file.close()

cbow_output = gensim.models.KeyedVectors.load_word2vec_format('/Users/djouldebarry/Desktop/test/vectors.txt', binary=False)
cbow_output.most_similar(positive=['good'])

weights = cbow.get_weights()[0]
weights = weights[1:]
print(weights.shape)

pd.DataFrame(weights, index=list(id2word.values())[1:]).head()