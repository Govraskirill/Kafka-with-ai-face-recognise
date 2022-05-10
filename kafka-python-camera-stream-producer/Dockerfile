FROM python:3

COPY . .

RUN pip install -r requirements/requirements.txt

#fixed this error ImportError: libGL.so.1: cannot open shared object file: No such file or directory
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

#fixed error: This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
RUN apt-get update && \
    apt-get install -y libqt5gui5 && \
    rm -rf /var/lib/apt/lists/*

ADD producer.py /
CMD ["python3", "producer.py"]

