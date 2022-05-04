from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import base64
import json
from time import strftime, gmtime, time_ns
import sys
from kafka import KafkaProducer
from kafka.errors import KafkaError

thres = 0.65 #Threshold to detect object

producer = KafkaProducer(bootstrap_servers='192.168.1.2:9092')#, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
#value_serializer=lambda m: json.dumps(m).encode('ascii')
#value_serializer=lambda v: json.dumps(v).encode('utf-8')
topic = 'mongotest12'

#second topic for timestamp, video and subject
producer1 = KafkaProducer(bootstrap_servers='192.168.1.2:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
topic1 = 'mongotest14'


#timestamp
#timestamp = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
timestamp = time_ns()

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", default = "rtsp://admin:admin@192.168.1.6:1935",
	help="path to input video file")
ap.add_argument("-d", "--display", type = int, default = "1",
	help="show video or not: 0 - no, 1 - yes")
args = vars(ap.parse_args())

#link on RTSP
cap = cv2.VideoCapture(args["video"])

#parameters of stream
cap.set(3,640)
cap.set(4,480)

#array for class names which will be detect on video stream
classNames = []
#file with list of class names
classFile = 'coco.names'

#open file for reading, after put in array classNames class names
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

#copy necessary settings for future work
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

#load dnn detection model
net = cv2.dnn_DetectionModel(weightsPath, configPath)
#necessary settings for start model
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

while True:
    #send image to model and receive predictions (necessary information)
    success,img = cap.read()
    #classIds, confidence configuration, boundary box (id класса, конфигурация достоверности, ограничивающая рамка)
    classIds, confs, bbox = net.detect(img, confThreshold = thres) #define threshold to detect object (should be >= our value)
    print(classIds, confs, bbox)


    if len(classIds) != 0:
        #use zip so that use one loop
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            #send image (our stream), coordinates of boundary box and her color, and value of thickness
            cv2.rectangle(img, box, color=(0,255,0), thickness=2)
            cv2.putText(img, classNames[classId - 1].upper(), (box[0]+10,box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2) #font, scale,color,thickness

            cv2.putText(img, str(confidence), (box[0]+150,box[1]+30),
                                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

            #send to topic for mongoDB
            future = producer1.send(topic1, value = {'timestamp': timestamp, 'subject': classNames[classId - 1]})

    # show the frame and update the FPS counter
    if args["display"] > 0:
        cv2.imshow("Output",img)
        cv2.waitKey(1)

    # png might be too large to emit
    encode_param = [int (cv2.IMWRITE_JPEG_QUALITY), 90]
    data = cv2.imencode('.jpg', img, encode_param)[1]#.tobytes()

    # Converting the image into numpy array
    data_encode = np.array(data)

    # Converting the array to bytes.
    byte_encode = data_encode.tobytes()

    #send to kafka topic
    future = producer.send(topic, byte_encode)




# do a bit of cleanup
cv2.destroyAllWindows()



