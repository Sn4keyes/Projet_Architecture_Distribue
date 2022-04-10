#!/usr/bin/python

import pip
from pyspark.sql.types import StructType, StructField, FloatType, IntegerType, StringType
from pyspark.ml.stat import Correlation
from pyspark.sql import SparkSession
from pandas.tseries import offsets
from kafka import KafkaConsumer
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import pymongo
import json
import time
from get_data import main as get_data
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.ml.classification import LogisticRegression, LogisticRegressionModel
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline, pipeline, PipelineModel
import pickle

# Création d'une session spark

def spark_connect():
    spark = SparkSession    \
            .builder    \
            .master('local')    \
            .appName('IAMDB')  \
            .config("spark.mongodb.input.uri", "mongodb://root:root@mongo:27017/crypto.*?authSource=admin")  \
            .config("spark.mongodb.output.uri", "mongodb://root:root@mongo:27017/crypto.*?authSource=admin") \
            .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.0") \
            .config("spark-jars-packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1")  \
            .getOrCreate()
    spark.sparkContext
    return spark

spark = spark_connect()
data = get_data()
spark_df = spark.createDataFrame(data)
# Suppression des lignes aux valeurs nulles
spark_df = spark_df.dropna()
spark_df.show(5)
spark_df.printSchema()
(train_set, test_set) = spark_df.randomSplit([0.7, 0.3])

# TF-IDF

# Tokenisation
tokenizer = Tokenizer(inputCol="Comment", outputCol="words")
# Associe un Hashcode aux termes en fonction de leur nombre d'occurence
hashtf = HashingTF(inputCol="words", outputCol='tf')
# Vectorisation
idf = IDF(inputCol='tf', outputCol="features")
# Création de la Pipeline
steps =  [tokenizer, hashtf, idf]
pipeline = Pipeline().setStages(steps)
# Entrainement de la pipeline
pipelineFit = pipeline.fit(train_set)
train_df = pipelineFit.transform(train_set)

# Mise en place de la régression
lr = LogisticRegression(labelCol="Rate", featuresCol="features")

# Entrainement du modèle
lrModel = lr.fit(train_df)

# Tests
test_set = pipelineFit.transform(test_set)
predictions = lrModel.transform(test_set)

# Résultats
evaluator = BinaryClassificationEvaluator(rawPredictionCol="prediction", labelCol="Rate")
print("Prédiction: \n", evaluator.evaluate(predictions))

accuracy = predictions.filter(predictions.Rate == predictions.prediction).count() / float(test_set.count())
print("Précision: \n", accuracy)

# On enregistre les modèles de pipeline et lr
# lrModel.save("my_spark_model")
# pipeline_model = pipelineFit.save("pipeline_model")

# On le charge 
loadedModel_LR = LogisticRegressionModel.load("/home/work/my_spark_model")

# ex = ["i hate the movie it sucks"]

# def main(comment):
#     pipelineFit = pipeline.fit([comment])
#     com = pipelineFit.transform(comment)
#     res = loadedModel_LR.transform(com)
#     return(res)

# if __name__ == "__main__":
#     main(ex[0])