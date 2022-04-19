from kafka import KafkaConsumer
from kafka import TopicPartition
import json
import base64

#libraries for cv
import numpy as np
import cv2
import matplotlib.pyplot as plt

from kafka import KafkaProducer
from kafka.errors import KafkaError

#connect to consumer so that receive data from necessary topic
consumer = KafkaConsumer('mongotest9', bootstrap_servers='192.168.1.12:9092', auto_offset_reset='latest')

for message in consumer:

    #parse JSON lines from our topic, which we choosed on consumer
    parseJSON = json.loads(message.value)

    #access elements in the object
    timestamp_temp = parseJSON['timestamp']
    value_temp = parseJSON['value']

    #in this place we print values, which we took from topic json lines
    print('timestamp: ', timestamp_temp, 'value: ', value_temp[:80])

    jpg_original = base64.b64decode(value_temp)

    #Put data in new topic for streaming
    producer = KafkaProducer(bootstrap_servers='192.168.1.12:9092')
    topic = 'mongotest10'

    #send data to streaming topic
    future = producer.send(topic, jpg_original)

    #check correct transfer line to binary code
    #print(jpg_original)

    #Зафиксировать смещение
consumer.commit()
