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
topic = 'mongotest9'

#timestamp
#timestamp = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
timestamp = time_ns()

#start
def emit_video(path_to_video):
    print('start')


    cascPath = "models/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)

    video_capture = cv2.VideoCapture(path_to_video)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            #flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    #video_capture.release()
    #cv2.destroyAllWindows()

        # png might be too large to emit
        data = cv2.imencode('.jpg', frame)[1].tobytes()

        # Convert to base64 encoding and show start of data
        jpg_as_text = base64.b64encode(data)

        # Convert back to binary
        #jpg_original = base64.b64decode(jpg_as_text)

        #send to kafka topic
        future = producer.send(topic, value = {'value': jpg_as_text.decode('UTF-8'), 'timestamp': timestamp})
        #value = {'value': jpg_as_text.decode('UTF-8'), 'timestamp': timestamp}

        #print value so that confirm transfer data from kafka producer to kafka broker (topic)
        print('value: ', jpg_as_text[:80], 'timestamp: ', timestamp)

        try:
            future.get(timeout=10)
        except KafkaError as e:
            print(e)

    #break

    video_capture.release()
    cv2.destroyAllWindows()


emit_video("rtsp://192.168.1.201:554/ch01_sub.264")
# zero is for open webcam or usb webcam
# can play a video just add video file in emit_video function
# rtsp camera stream add rtsp feed in emit_video function
#"rtsp://192.168.1.201:554/ch01_sub.264"

