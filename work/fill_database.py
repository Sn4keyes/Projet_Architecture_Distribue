#!/usr/bin/python

from pyspark.sql.types import StructType, StructField, FloatType, IntegerType, StringType
from traitement_comm_EN import main as traitement
from pyspark.ml.stat import Correlation
from pyspark.sql import SparkSession
from sklearn.utils import resample
from pymongo import MongoClient
import pandas as pd
import numpy as np

def post_in_token_db(df_token, imdb_tokenized_coll):
    post_db = imdb_tokenized_coll.insert_many(df_token.to_dict('records'))

def post_in_bully_db(df, imdb_bully_coll):
    post_db = imdb_bully_coll.insert_many(df.to_dict('records'))

def rate_bol(i):
    if i >= 5:
        i = 1
    else:
        i = 0
    return(i)

def data_treatment(imdb_bully_coll):
    with open('DataSet/Movie_dataframe.json', 'r') as df:
        data = pd.read_json(df)
    data.columns = ['Rate', 'Comment']
    # Retire les lignes avec des commentaires vides
    data = data.replace(to_replace='', value=np.nan).dropna()
    # DataFrame avec les données traitées
    df_token = pd.DataFrame(columns=['Rate', 'Comment'])
    df_token['Comment'] = data['Comment']
    df_token['Rate'] = data['Rate'].apply(rate_bol)
    print(df_token)
    post_in_bully_db(df_token, imdb_bully_coll)
    # On sépare les notes positives des notes négatives
    df_minor = df_token[df_token['Rate'] == 0] # Négatives
    df_major = df_token[df_token['Rate'] == 1] # Positives
    nb_minor= len(df_minor)
    # On réduit la taille de l'échantillon majoritaire à 3446 car on a 3446 commentaires négatifs
    df_major_downsize = resample(df_major, replace=False, n_samples=nb_minor, random_state=123)
    # On concatene l'échantillon majoritaire à effectif réduit et l'échantillon minoritaire complet
    df_downsized = pd.concat([df_major_downsize, df_minor])
    df_test = pd.DataFrame(columns=['Rate', 'Comment'])
    df_test['Comment'] = df_downsized['Comment'].apply(traitement)
    df_test['Rate'] = df_downsized['Rate']
    return df_test

def connect_imdb_mongodb():
    client = MongoClient('mongo', port = 27017, username = 'root', password = 'root')
    imdb_db = client.imdb
    imdb_bully_coll = imdb_db.imdb_bully
    imdb_tokenized_coll = imdb_db.imbd_tokenized
    return imdb_db, imdb_bully_coll, imdb_tokenized_coll

def main():
    try:
        print("########## ########## ########## ########## ########## ##########")
        print("- Creating IMDB DB...")
        imdb_db, imdb_bully_coll, imdb_tokenized_coll = connect_imdb_mongodb()
        print("- OK")
    except:
        print("- MongoDB IMDB database connection error")
    df_clean = data_treatment(imdb_bully_coll)
    print("DF CLEAN ==\n", df_clean)
    post_in_token_db(df_clean, imdb_tokenized_coll)
    return

if __name__ == "__main__":
    main()