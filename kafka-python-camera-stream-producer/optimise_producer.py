# import the necessary packages
from imutils.video import FileVideoStream
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

producer = KafkaProducer(bootstrap_servers='192.168.1.12:9092')#, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
#value_serializer=lambda m: json.dumps(m).encode('ascii')
#value_serializer=lambda v: json.dumps(v).encode('utf-8')
topic = 'mongotest12'

#timestamp
#timestamp = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
timestamp = time_ns()

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", default = "rtsp://192.168.1.201:554/ch01_sub.264",
	help="path to input video file")
ap.add_argument("-d", "--display", type = int, default = "1",
	help="show video or not: 0 - no, 1 - yes")
args = vars(ap.parse_args())

# start the file video stream thread and allow the buffer to
# start to fill
print("[INFO] starting video file thread...")
fvs = FileVideoStream(args["video"]).start()
time.sleep(1.0)
# start the FPS timer
fps = FPS().start()

#put model for ai and put this file on function
cascPath = "models/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
face_buffer = None
counter = 10

# loop over frames from the video file stream
while True:
	if counter == 10:
		# grab the frame from the threaded video file stream, resize
		# it, and convert it to grayscale (while still retaining 3
		# channels)
		frame = fvs.read()
		#frame = imutils.resize(frame, width=450)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


		faces = faceCascade.detectMultiScale(
			gray,
			scaleFactor=1.1,
			minNeighbors=5,
			minSize=(30, 30),
			#flags=cv2.cv.CV_HAAR_SCALE_IMAGE
			flags=cv2.CASCADE_SCALE_IMAGE
		)
		face_buffer = faces
		counter = 0

	counter += 1
	for (x, y, w, h) in face_buffer:
	    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

	# show the frame and update the FPS counter
	if args["display"] > 0:
	    cv2.imshow("Frame", frame)
	    cv2.waitKey(1)

	fps.update()

	# png might be too large to emit
	encode_param = [int (cv2.IMWRITE_JPEG_QUALITY), 90]
	data = cv2.imencode('.jpg', frame, encode_param)[1]#.tobytes()

	# Converting the image into numpy array
	data_encode = np.array(data)

	# Converting the array to bytes.
	byte_encode = data_encode.tobytes()

	#send to kafka topic
	future = producer.send(topic, byte_encode)

	#fps.update()

# stop the timer and display FPS information
#fps.stop()
#print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
#print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
# do a bit of cleanup
cv2.destroyAllWindows()
fvs.stop()


