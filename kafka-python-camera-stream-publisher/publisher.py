# Import some necessary modules for KafkaConsumer
from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads
import json

topic = 'mongotest14'

# Connect to MongoDB and consumerDB database
try:
   client = MongoClient('localhost',27017)
   db = client.consumerDB
   series_collection=db.consumerCollection
   print("Connected successfully to {}!".format(series_collection))
except:
   print("Could not connect to {}.".format(series_collection))

# connect kafka consumer to desired kafka topic
try:
    consumer = KafkaConsumer(topic,bootstrap_servers=['192.168.1.12:9092'], auto_offset_reset='latest', value_deserializer=lambda x: loads(x.decode('ISO-8859-1')))
    print("Connect to topic {}".format(topic))
except:
    print("Could not connect to topic {}".format(topic))

#copy data from KafkaConsumer to MongoDB
for message in consumer:
    message_in_mongoDB = message.value
    series_collection.insert_one(message_in_mongoDB)
    print('{} added to {}'.format(message_in_mongoDB, series_collection))