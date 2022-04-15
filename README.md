# Kafka-with-ai-face-recognise
Repository where you can find necessary information for work with kafka producer, consumer, KafkaBrokerTopic to Mongo Connector and Parser which allow work with ai face recognise

In this repository you can find four directories at the moment: 
1. kafka producer
2. kafka consumer
3. kafka parser, which allow work with ai face recognice
4. connector for transfer data from Kafka broker topic to MongoDB collection

<b>Let's making your Ubuntu up to date</b>
```{r klippy, echo=FALSE, include=TRUE}
sudo apt-get update -y
sudo apt-get upgrade -y
```


<b>Installing Java</b>

1. Before installing Kafka, you will need to install Java, add this repository
```{r klippy, echo=FALSE, include=TRUE}
sudo add-apt-repository -y ppa:webupd8team/java
```
2. Next, update the metadata of the new repository and install JDK 8
```{r klippy, echo=FALSE, include=TRUE}
sudo apt-get update
sudo apt-get install oracle-java8-installer -y
```
<b>Install ZooKeeper</b>
```{r klippy, echo=FALSE, include=TRUE}
sudo apt-get install zookeeperd
```
<b>Install and start kafka broker</b>

For work with kafka you should install kafka broker

1. You can find installation file on official site: https://kafka.apache.org/quickstart
2. Make direrctory for Kafka installation:
```{r klippy, echo=FALSE, include=TRUE}
sudo mkdir /opt/Kafka
cd /opt/Kafka
```
3. Extract the downlanded archive in /opt/Kafka
```{r klippy, echo=FALSE, include=TRUE}
sudo tar -xvf kafka_2.13-3.1.0.tgz -C /opt/Kafka/
```
4. Start kafka broker 
```{r klippy, echo=FALSE, include=TRUE}
sudo /opt/Kafka/kafka_2.13-3.1.0/bin/kafka-server-start.sh /opt/Kafka/kafka_2.13-3.1.0/config/server.properties
```
5. If you need to create some topic for storage data you can use next command
```{r klippy, echo=FALSE, include=TRUE}
sudo /opt/Kafka/kafka_2.13-3.1.0/bin/kafka-topics.sh --create --topic topicname --bootstrap-server localhost:9092
```

<b>Tips for work with kafka broker</b>

If you will be start producer, consumer, kafka broker server on the different devices you should in config/server.properties (in kafka broker files) manage: 
<ul>
  <li> Broker address: 
  <pre>advertised.listeners=PLAINTEXT://192.168.1.12:9092</pre> 
  <b>(instead 192.168.1.12:9092 you should write you ip_address:port, where ip_address this is appropriate computer ip_address you kafka broker are running)</b></li>
  <li> Producer and consumer addresses. For example if you wanna working in local network you should assign this one in line:          <pre>listeners=PLAINTEXT://0.0.0.0:9092</pre></li>
  <li> If need install libraries for readme file in kafka broker directory.</li>
  <li>In some case maybe need install:
  <pre> sudo apt-get install -y sox</pre></li>
</ul>

<b>Downland project</b>

For work with project firstly needed downland into your local machine
1. Go to directory where you wanna laid project
<pre>cd your/directory</pre>
2. Run the next command
```{r klippy, echo=FALSE, include=TRUE}
sudo git clone https://github.com/Govraskirill/Kafka-with-ai-face-recognise ./
```

<b>Kafka producer</b>

You can find in kafka-python-camera-stream-producer directory. What necessary:
1. Got to directory with kafka-python-camera-stream-producer on your local machine/server
2. Run the next command:
```{r klippy, echo=FALSE, include=TRUE}
python3 producer.py
```
3. In this file, depends on what external device (usb camera/IP camera) you will be use, change last line on code
<pre>emit_video(0) for usb camera (or other sign depends on your device number; can check with command <b>ls /dev</b> your devices)</pre>

<b>Kafka consumer</b>

You can find in kafka-python-camera-stream-consumer directory. What necessary:
1. Got to directory with kafka-python-camera-stream-consumer on your local machine/server
2. Run the next command:
```{r klippy, echo=FALSE, include=TRUE}
python3 consumer.py
```

<b>Kafka parser</b>

You can find in kafka-python-camera-stream-parser directory. What necessary:
1. Got to directory with kafka-python-camera-stream-parser on your local machine/server
2. Run the next command:
```{r klippy, echo=FALSE, include=TRUE}
python3 parser.py
```
<b>Work with MongoDB</b>

Use .py code of this project we can copy data from kafka broker topic and transfer to MongoDB

So that start work we need to install MongoDB. All necesary instruction you can find on official site by link: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/

In future I add files for organization work in kubernetes
