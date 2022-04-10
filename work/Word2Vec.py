import gensim
import string
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from gensim.models import Word2Vec
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd 
import os
import re
import nltk
nltk.download('punkt')

# importation de la base
D = pd.read_csv("/Users/djouldebarry/Desktop/test/imdb_r.csv", encoding='latin-1')

#Nettoyage du corpus
corpus = D['commentaires'].tolist() #récupération sous forme de liste
for i in range(0,len(corpus)):
    print(corpus[i])

for doc in corpus:
    doc.lower()

ponctuations = list(string.punctuation)
print(ponctuations)

#retrait des ponctuations
for i in range(0,len(corpus)):
    corpus = ["".join([char for char in list(doc) if not (char in ponctuations)]) for doc in corpus]
    print(corpus[i])

#tokenisation
corpus_tk = [word_tokenize(doc) for doc in corpus]
for i in range (0,len(corpus)):
    print(corpus_tk[i])

#lematization
lem = WordNetLemmatizer()
for i in range (0,len(corpus)):
    corpus_lm = [[lem.lemmatize(mot) for mot in doc] for doc in corpus_tk]
    print(corpus_lm[i])

#suppression des mots vides (stopwords)
mots_vides = stopwords.words('english')
for i in range (0,len(corpus)):
    print(mots_vides)

#suppression des mots de moins de 3 lettres
corpus_sw = [[mot for mot in doc if len(mot) >= 3] for doc in corpus_sw]
for i in range (0,len(corpus_sw)):
    print(corpus_sw[i])

#Application du Word2Vec
modele = Word2Vec(corpus_sw,vector_size=2,window=5)
words = modele.wv

words.similarity('boring','love')
words.most_similar("boring")

df = pandas.DataFrame(words.vectors,columns=['V1','V2'],index=words.key_to_index.keys())
print(df)

mots = ['bad','good','plot','character','actor','dialogue','music']
dfMots = df.loc[mots,:]
print(dfMots)

plt.scatter(dfMots.V1,dfMots.V2,s=0.5)
for i in range(dfMots.shape[0]):
    plt.annotate(dfMots.index[i],(dfMots.V1[i],dfMots.V2[i]))
plt.show()
