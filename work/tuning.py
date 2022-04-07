from operator import index
from re import I
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
from lineaire import rate_bol

####################################### Tuning de notre modèle linéaire #######################################

svc = LinearSVC()
tfidf = TfidfVectorizer()
classifier = LinearSVC()

# Output: {'Rate': int, 'Comment': str}

with open('Movie_dataframe.json', 'r') as df:
  data = pd.read_json(df)

data.columns = ['Rate', 'Comment']

# Retire les lignes avec des commentaires vides

data = data.replace(to_replace='', value=np.nan).dropna()

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

# tfidf sert à numeriser l'importance qu'à un mot dans un commentaire compte tenu de tous les commentaires

X = tfidf.fit_transform(X)

# On sépare notre base de données en 70% apprentissage et 30% test

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, train_size=0.7)

# Modèle Tuning - optimisation des paramètres du modèle

# Paramètres à combiner

param = {
  'loss': ['hinge', 'squared_hinge'],
  'C': [1, 5, 10],
  'penalty': ['l1', 'l2']
}

# Création de l'objet qui va automatiser les tests en combinant nos différents paramètres

searchCV = GridSearchCV(estimator=svc, scoring='roc_auc', param_grid=param, cv=5)

# Exécution

searchCV.fit(X_train, y_train)

# Affichage des résultats

print('Best index:', searchCV.best_index_) # Quelle itération était la plus optimale
print('Best score:', searchCV.best_score_) # Quel était son score
print('Best params:', searchCV.best_params_) # Quels étaient les paramètres associés