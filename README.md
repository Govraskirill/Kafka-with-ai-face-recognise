# Kafka-with-ai-face-recognise
Repository where you can find necessary information for work with kafka producer, consumer, publisher which allow work with ai face recognise

In this repository you can find four directories at the moment: 
1. kafka producer
2. kafka consumer
3. kafka publisher for transfer data from Kafka broker topic to MongoDB collection

<b>Let's making your Ubuntu up to date</b>
<pre>
sudo apt-get update -y
sudo apt-get upgrade -y
</pre>


<b>Installing Java</b>

1. Before installing Kafka, you will need to install Java, add this repository
```{r klippy, echo=FALSE, include=TRUE}
sudo add-apt-repository -y ppa:webupd8team/java
```
2. Next, update the metadata of the new repository and install JDK 8
<pre>
sudo apt-get update
sudo apt-get install oracle-java8-installer -y
</pre>
<b>Install ZooKeeper</b>
```{r klippy, echo=FALSE, include=TRUE}
sudo apt-get install zookeeperd
```
<b>Install and start kafka broker</b>

For work with kafka you should install kafka broker

1. You can find installation file on official site: https://kafka.apache.org/quickstart
2. Make directory for Kafka installation:
<pre>
sudo mkdir /opt/Kafka
cd /opt/Kafka
</pre>
3. Extract the downloaded archive in /opt/Kafka
```{r klippy, echo=FALSE, include=TRUE}
sudo tar -xvf kafka_2.13-3.1.0.tgz -C /opt/Kafka/
```
4. Start kafka broker 
```{r klippy, echo=FALSE, include=TRUE}
sudo /opt/Kafka/kafka_2.13-3.1.0/bin/kafka-server-start.sh /opt/Kafka/kafka_2.13-3.1.0/config/server.properties
```
5. Create topics for storage data by use the next command:
<pre>
sudo /opt/Kafka/kafka_2.13-3.1.0/bin/kafka-topics.sh --create --topic mongotest12 --bootstrap-server localhost:9092
sudo /opt/Kafka/kafka_2.13-3.1.0/bin/kafka-topics.sh --create --topic mongotest14 --bootstrap-server localhost:9092
</pre>

Topic which you will be create depends on which you will be using in producer

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

<b>Download project</b>

For work with project firstly needed downland into your local machine
1. Go to directory where you wanna laid project
<pre>cd your/directory</pre>
2. Run the next command
```{r klippy, echo=FALSE, include=TRUE}
sudo git clone https://github.com/Govraskirill/Kafka-with-ai-face-recognise ./
```

<b>Kafka producer</b>

You can find in kafka-python-camera-stream-producer directory. What necessary:
1. Go to directory with kafka-python-camera-stream-producer on your local machine/server
2. Run the next command:
```{r klippy, echo=FALSE, include=TRUE}
python3 producer.py
```
3. In this file, depends on what external device (usb camera/IP camera) you will be use, change line on code
<pre>ap.add_argument("-v", "--video", default = "rtsp://192.168.1.6:1935" (change this link on link with your camera)</pre>

4. By default when start producer.py will be show window with videostream from camera. You can change this one using parameter <b>-d 0 </b>(not display); also can change source: <b>-v your_link</b>

<b>Kafka consumer</b>

You can find in kafka-python-camera-stream-consumer directory. What necessary:
1. Go to directory with kafka-python-camera-stream-consumer on your local machine/server
2. Run the next command:
```{r klippy, echo=FALSE, include=TRUE}
python3 consumer.py
```
3. Go to link 127.0.0.1:5000 on your browser

<b>Kafka publisher</b>

You can find in kafka-python-camera-stream-publisher directory. What necessary:
1. Go to directory with kafka-python-camera-stream-publisher on your local machine/server
2. Run the next command:
```{r klippy, echo=FALSE, include=TRUE}
python3 publisher.py
```
<b>Work with MongoDB</b>

Use .py code of this project we can copy data from kafka broker topic and transfer to MongoDB
<ul>
  <li>So that start work we need to install MongoDB. All necesary instruction you can find on official site by link: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/</li>
  <li>Also will be useful next link for more convenient work with MongoDB: 
https://www.mongodb.com/docs/compass/current/install/</li>
  <li>In case some problem with connect to MongoDB directly from another device:
https://syntaxfix.com/question/448/mongonetworkerror-failed-to-connect-to-server-localhost-27017-on-first-connect-mongonetworkerror-connect-econnrefused-127-0-0-1-27017 
</ul>

After install necessary dependencies (for step 1 and 2 use mongoDB compass):
1. Create <b>consumerDB</b> database on MongoDB
2. Create collection <b>consumerCollection</b> on <b>consumerDB</b> database
3. Go to directory kafka-python-camera-stream-publisher
4. Run the next code:
```{r klippy, echo=FALSE, include=TRUE}
python3 publisher.py
```
<b>Notice</b>
<ul>
  <li>In line  client = MongoClient('192.168.1.124',27017). Change ip address. Use ip address of your machine, where ran MongoDB. Port should be as default = 27017</li>
  <li>In line consumer = KafkaConsumer change parameter bootstrap_servers=['192.168.1.12:9092']. Assign ip address of your mashine/server where ran kafka broker. If start code on one machine write localhost:9092</li>
</ul>

For build dockerfiles for each element of kafka, run the next commands (only separately, line by line):
1. Download from dockerhub images:
<pre>
docker pull kirillgovras/kafka_producer:3.0
docker pull kirillgovras/kafka_consumer:3.0
docker pull kirillgovras/publisher:3.0
</pre>
1.1. You can build containers appropriate from directories. Only use commands (from necessary directories, all have dockerfiles):
<pre>
docker build -t nameofproducerimage .
</pre>
2. Run docker containers:
<pre>
docker run -e "DISPLAY=$DISPLAY" -v "XAUTHORITY=~/.Xauthority" --network host --name producer kirillgovras/kafka_producer:3.0
docker run -p 5000 --name consumer --network=host kirillgovras/kafka_consumer:3.0
docker run --network=host --name publisher kirillgovras/publisher:3.0
</pre>
3. For stop containers you can run commands:
<pre>
docker stop producer
docker stop consumer
docker stop publisher
</pre>

<b>Work in Kubernetes</b>

For orchestry this docker containers will be use kubernetes
1. Firstly need install kubectl and minikube(local Kubernetes). Use next links:
https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/
https://minikube.sigs.k8s.io/docs/start/ 
2. If will be problem with start on ubuntu go to link:
https://stackoverflow.com/questions/65397050/minikube-does-not-start-on-ubuntu-20-04-lts-exiting-due-to-guest-provision

Start work with kubernetes:
1. Run command:
```{r klippy, echo=FALSE, include=TRUE}
minikube start
```
2. Build deployments (pods will be create automatically) so that work with containers from previous steps. Run this command by separately:
<pre>
kubectl create deployment producer --image=kirillgovras/kafka_producer:3.0
kubectl create deployment consumer --image=kirillgovras/kafka_consumer:3.0
kubectl create deployment publisher --image=kirillgovras/publisher:3.0
</pre>
3. For open our consumer on browser we need forward a port. Run first command so that define pod with consumer's container and run the second command so that forward a port:
<pre>
kubectl get pods
kubectl port-forward name_of_consumer_pod 5000:5000
</pre>
4. In some cases when we work in local network need to change .yaml files for our pods with containers. Edit deployment with the next command:
```{r klippy, echo=FALSE, include=TRUE}
KUBE_EDITOR="nano" kubectl edit deployment name_deployment 
```
In deployment find function spec and add line <b>hostNetwork: true</b>:
<pre>
spec:
      hostNetwork: true
      containers:
      - image: kirillgovras/kafka_producer:2.0
        imagePullPolicy: IfNotPresent
</pre>

<b>NOTICE</b>
1. Necessary to check work in kubernetes with producer and publisher (consumer are working)
2. Add makefie in some directories (namely in producer)

