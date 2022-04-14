from flask import Flask, Response
from kafka import KafkaConsumer

consumer = KafkaConsumer('mongotest8', bootstrap_servers='192.168.1.12:9092', auto_offset_reset='latest')

app = Flask(__name__)


def kafkastream():
    for message in consumer:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + message.value + b'\r\n\r\n')


@app.route('/')
def index():
    return Response(kafkastream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run()
