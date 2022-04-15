# Kafka-with-ai-face-recognise
Repository where you can find necessary information for work with kafka producer, consumer, KafkaBrokerTopic to Mongo Connector and Parser which allow work with ai face recognise

In this repository you can find four directories at the moment: 
1. kafka producer
2. kafka consumer
3. kafka parser, which allow work with ai face recognice
4. connector for transfer data from Kafka broker topic to MongoDB collection

<b>Let's making your Ubuntu up to date</b>

<pre>sudo apt-get update -y
sudo apt-get upgrade -y</pre>

<b>Installing Java</b>

1. Before installing Kafka, you will need to install Java, add this repository

sudo add-apt-repository -y ppa:webupd8team/java

2. Next, update the metadata of the new repository and install JDK 8

sudo apt-get update
sudo apt-get install oracle-java8-installer -y

<b>Install ZooKeeper</b>

sudo apt-get install zookeeperd

<b>Install and start kafka broker</b>

For work with kafka you should install kafka broker. You can find instruction on official site: https://kafka.apache.org/quickstart

<b>Tips for work with kafka broker</b>

If you will be start producer, consumer, kafka broker server on the different devices you should in config/server.properties (in kafka broker files) manage: 

a. Broker address: advertised.listeners=PLAINTEXT://192.168.1.12:9092 (instead 192.168.1.12:9092 you should write you ip_address:port)</br>
b. Producer and consumer addresses. For example if you wanna working in local network you should assign this one in line: listeners=PLAINTEXT://0.0.0.0:9092 (0.0.0.0: port)</br>
c. If need install libraries for readme file in kafka broker directory. In some case maybe need install: sudo apt-get install -y sox

Kafka producer

You can find in kafka-python-camera-stream-producer directory. What necessary:
1. Make directory for this goal:
mkdir 

In future I add files for organization work in kubernetes
