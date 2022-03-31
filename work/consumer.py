#!/usr/bin/python

from pyspark.sql.types import StructType, StructField, FloatType, IntegerType, StringType
from pyspark.ml.stat import Correlation
from pyspark.sql import SparkSession
from pandas.tseries import offsets
from kafka import KafkaConsumer
from datetime import datetime
import pandas as pd
import json
import time

BROKER = 'kafka:9093'
TOPIC = 'crypto5'

if __name__ == "__main__":

    try:
        print("########## Création de la base de données ##########")
    except:
        print("Erreur de connexion à MongoDB")
    consumer = KafkaConsumer(TOPIC, bootstrap_servers=[BROKER], api_version=(2,6,0))
    for msg in consumer:
        print("########## Received Data From Producer : OK ##########")
        df = pd.DataFrame.from_dict(json.loads(msg.value))
        print("\n########## DataFrame Pandas : ##########\n")
        print(df)