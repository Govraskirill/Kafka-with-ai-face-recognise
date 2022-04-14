from time import strftime, gmtime, time_ns
import sys
import cv2
import base64
import json

from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(bootstrap_servers='192.168.1.12:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
#value_serializer=lambda m: json.dumps(m).encode('ascii')
#value_serializer=lambda v: json.dumps(v).encode('utf-8')
topic = 'mongotest7'

#timestamp
#timestamp = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
timestamp = time_ns()

#start
def emit_video(path_to_video):
    print('start')


    #take video from such source as emit_video
    video = cv2.VideoCapture(path_to_video)

    while video.isOpened():
        success, frame = video.read()
        if not success:
            break

        # png might be too large to emit
        data = cv2.imencode('.jpg', frame)[1].tobytes()

        # Convert to base64 encoding and show start of data
        jpg_as_text = base64.b64encode(data)

        # Convert back to binary
        #jpg_original = base64.b64decode(jpg_as_text)

        #send to kafka topic
        future = producer.send(topic, value = {'value': jpg_as_text.decode('UTF-8'), 'timestamp': timestamp})

        #print value so that confirm transfer data from kafka producer to kafka broker (topic)
        print('value: ', jpg_as_text[:80], 'timestamp: ', timestamp)
        try:
            future.get(timeout=10)
        except KafkaError as e:
            print(e)
            break



emit_video("rtsp://192.168.1.201:554/ch01_sub.264")
# zero is for open webcam or usb webcam
# can play a video just add video file in emit_video function
# rtsp camera stream add rtsp feed in emit_video function
#"rtsp://192.168.1.201:554/ch01_sub.264"