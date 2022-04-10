#!/usr/bin/python

from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from traitement_comm_EN import main as traitement
from sklearn.pipeline import Pipeline
from matplotlib.pyplot import axis
from sklearn.utils import resample
from xmlrpc.client import boolean
from sklearn.svm import LinearSVC
from get_data import get_data
from textwrap import indent
from operator import index
import sklearn as sk
import pandas as pd
import numpy as np
import imblearn
import pickle
import joblib
import json
import os
import re

####################################### Modèle linéaire #######################################

svc = LinearSVC(penalty='l2', C=5, loss='squared_hinge') # Paramètres optimaux choisit grâce à tuning.py
tfidf = TfidfVectorizer()

# Output: {'Rate': int, 'Comment': str}

data = get_data()
data.drop('_id', inplace=True, axis=1)

data.columns = ['Rate', 'Comment']

# Retire les lignes avec des commentaires vides

data = data.replace(to_replace='', value=np.nan).dropna()

X = data['Comment']
y = data['Rate']

# tfidf sert à numeriser l'importance qu'à un mot dans un commentaire 
# et va ainsi vectoriser nos données par ce bias

X = tfidf.fit_transform(X)

# On sépare notre base de données en 70% apprentissage et 30% test

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, train_size=0.7)

# On entraine le modèle avec nos données d'apprentissage (train)

svc.fit(X_train, y_train)

# On évalue la précision de notre algorithme (test)

y_pred = svc.predict(X_test)
print(classification_report(y_test, y_pred))

# On enregistre notre modèle

pickle_file_name = "Model\my_model_opt.pkl"  

with open(pickle_file_name, 'wb') as file: # Write & Binary pour ne pas changer les données lors de l'écriture
    pickle.dump(svc, file)# On charge notre modèle

ex = ["i hate the movie it sucks"]

with open('Model\my_model_opt.pkl', 'rb') as file:
  pk_model = pickle.load(file)

def main(comment):
  com = [traitement(comment)]
  com = tfidf.transform(com)
  res = pk_model.predict(com)
  return(res)

if __name__ == "__main__":
    main()