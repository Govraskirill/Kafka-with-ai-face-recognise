# Import some necessary modules for KafkaConsumer
from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads
import json

# Connect to MongoDB and consumerDB database
try:
   client = MongoClient('192.168.1.124',27017)
   db = client.consumerDB
   series_collection=db.consumerCollection
   print("Connected successfully to consumerDB!")
except:
   print("Could not connect to MongoDB")

# connect kafka consumer to desired kafka topic
try:
    consumer = KafkaConsumer('mongotest7',bootstrap_servers=['192.168.1.12:9092'], auto_offset_reset='latest', value_deserializer=lambda x: loads(x.decode('ISO-8859-1')))
    print("Connect to topic my-topic")
except:
    print("Could not connect to topic my-topic")

#copy data from KafkaConsumer to MongoDB
for message in consumer:
    message_in_mongoDB = message.value
    series_collection.insert_one(message_in_mongoDB)
    print('{} added to {}'.format(message_in_mongoDB, series_collection))

    #ISO-8859-1
    #utf-8-sig
    #value_deserializer=lambda x: loads(x.decode('ISO-8859-1')
    #json.dumps(v).encode('utf-8')
