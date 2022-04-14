FROM python:3

COPY requirements/requirements.txt .

RUN pip install -r requirements.txt


#fixed this error ImportError: libGL.so.1: cannot open shared object file: No such file or directory
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

EXPOSE 5000

ADD consumer.py /
CMD ["python3", "consumer.py"]


