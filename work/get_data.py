from pymongo import MongoClient
import sqlite3
from sqlite3 import Connection
import streamlit as st

# Collecte des données de notre DataBase
def get_reviews(client_connect):
    mydb = client_connect["imdb"]
    mycol = mydb["imbd_tokenized"]
    df_db = {
        "Rate": [],
        "Comment": []
    }
    index = 0
    for x in mycol.find():
        df_db["_id"].insert(-1, index)
        df_db["Rate"].insert(-1, x["Rate"])
        df_db["Comment"].insert(-1, x["Comment"])
        index+=1
    return df_db

if __name__ == "main":
    client_connect = MongoClient('mongo', port = 27017, username = 'root', password = 'root')
    df_reviews = get_reviews(client_connect)
    print(df_reviews)