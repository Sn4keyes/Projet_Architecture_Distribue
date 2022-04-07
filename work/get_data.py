#!/usr/bin/python

from pymongo import MongoClient
from sqlite3 import Connection
import pandas as pd
import sqlite3

# Collecte des données de notre DataBase
def get_data():
    client = MongoClient('mongo', port = 27017, username = 'root', password = 'root')
    db = client.imdb
    collection = db.imbd_tokenized
    data = pd.DataFrame(list(collection.find()))
    return data

def main():
    data = get_data()
    df = pd.DataFrame(columns=['Rate', 'Comment'])
    df['Comment'] = data['Comment']
    df['Rate'] = data['Rate']
    return df

if __name__ == "__main__":
    main()