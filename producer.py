#!/usr/bin/python

from kafka import KafkaProducer
import sys
import time
import json

BROKER = 'localhost:9092'
TOPIC = 'crypto5'

if __name__ == "__main__":
    
    try:
        producer = KafkaProducer(bootstrap_servers=BROKER)                                                                         
    except Exception as e:
        print(f"ERROR --> {e}")
        sys.exit(1)
    
    # while True:
    print("########## Send Data To Kafka: OK ##########")
    json_full = {'col1': [1, 2], 'col2': [3, 4]}
    producer.send(TOPIC, json.dumps(json_full).encode('utf-8'))
    producer.flush()
    # sleep(5)