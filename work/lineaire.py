from operator import index
import re
from textwrap import indent
from xmlrpc.client import boolean
from matplotlib.pyplot import axis
import pandas as pd
import numpy as np
import sklearn as sk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.pipeline import Pipeline
import json
from sklearn.utils import resample
from traitement_comm_EN import main as traitement
import pickle
import imblearn
import os

####################################### Modèle linéaire #######################################

svc = LinearSVC(penalty='l2', C=5, loss='squared_hinge') # Paramètres optimaux choisit grâce à tuning.py
tfidf = TfidfVectorizer()

# Output: {'Rate': int, 'Comment': str}

with open('Movie_dataframe.json', 'r') as df:
  data = pd.read_json(df)

data.columns = ['Rate', 'Comment']

# Retire les lignes avec des commentaires vides

data = data.replace(to_replace='', value=np.nan).dropna()

# Traiter les notes pour qu'elles soient à 1 ou 0 respectivement pos ou neg

def rate_bol(x):
  if x >=5:
    x = 1
  else:
    x = 0
  return(x)

# DataFrame avec les données

df_token = pd.DataFrame(columns=['Rate', 'Comment'])

df_token['Comment'] = data['Comment']
df_token['Rate'] = data['Rate'].apply(rate_bol)

# On a trop de commentaires positifs, donc on downsize notre dataset afin d'avoir une analyse plus
# équilibrée et cohérente

# On sépare les notes positives des notes négatives

df_minor = df_token[df_token['Rate'] == 0] # Négatives
df_major = df_token[df_token['Rate'] == 1] # Positives

# On réduit la taille de l'échantillon majoritaire à 3446 car on a 3446 commentaires négatifs

df_major_downsize = resample(df_major, replace=False, n_samples=3446, random_state=123)

# On concatene l'échantillon majoritaire à effectif réduit et l'échantillon minoritaire complet

df_downsized = pd.concat([df_major_downsize, df_minor])

# On traite les commentaires pour réduire le bruit de nos données

df_downsized['Comment'] = df_downsized['Comment'].apply(traitement)

X = df_downsized['Comment']
y = df_downsized['Rate']

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

pickle_file_name = "my_model_opt.pkl"  

with open(pickle_file_name, 'wb') as file: # Write & Binary pour ne pas changer les données lors de l'écriture
    pickle.dump(svc, file)