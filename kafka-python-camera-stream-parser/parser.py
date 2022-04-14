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

#function for ai face recognise
def detect_faces(cascade, test_image, scaleFactor = 1.1):

        # create a copy of the image to prevent any changes to the original one.
        image_copy = test_image.copy()

        #convert the test image to gray scale as opencv face detector expects gray images
        gray_image = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)

        # Applying the haar classifier to detect faces
        faces_rect = cascade.detectMultiScale(gray_image, scaleFactor=scaleFactor, minNeighbors=5)

        for (x, y, w, h) in faces_rect:
            cv2.rectangle(image_copy, (x, y), (x+w, y+h), (0, 255, 0), 15)

        return image_copy

#connect to consumer so that receive data from necessary topic
consumer = KafkaConsumer('mongotest7', bootstrap_servers='192.168.1.12:9092', auto_offset_reset='latest')

for message in consumer:

    #parse JSON lines from our topic, which we choosed on consumer
    parseJSON = json.loads(message.value)

    #access elements in the object
    timestamp_temp = parseJSON['timestamp']
    value_temp = parseJSON['value']

    #in this place we print values, which we took from topic json lines
    #print('timestamp: ', timestamp_temp, 'value: ', value_temp[:80])

    #translate binary code back to image
    with open("decode_images/decode_image.jpg", "wb") as new_file:
        new_file.write(base64.decodebytes(value_temp.encode('UTF-8')))

    cascade = cv2.CascadeClassifier('models for ai face recognise/haarcascade_frontalface_default.xml')
    test_image = cv2.imread('decode_images/decode_image.jpg')

    #call function for ai face recognise
    faces = detect_faces(cascade, test_image)

    #Put data in new topic for streaming
    producer = KafkaProducer(bootstrap_servers='192.168.1.12:9092')
    topic = 'mongotest8'

    # png might be too large to emit
    faces_new = cv2.imencode('.jpg', faces)[1].tobytes()

    #send data to streaming topic
    future = producer.send(topic, faces_new)

    #check correct transfer line to binary code
    #print(jpg_original)

    #Зафиксировать смещение
consumer.commit()
