from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

def printCallback(client, userdata, message):
    print '[TOPIC] ' + message.topic
    print '[PAYLOAD] ' + message.payload

class AWSIoTClient:
    
    def __init__(self,host,rootCAPath,certificatePath,privateKeyPath):        
        # AWSIoTMQTTClient initialization
        self.client = AWSIoTMQTTClient("ORP_SENSOR")
        self.client.configureEndpoint(host, 8883)
	self.client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

        # AWSIoTMQTTClient connection configuration
        self.client.configureOfflinePublishQueueing(-1)
        self.client.configureDrainingFrequency(2)
        self.client.configureConnectDisconnectTimeout(10)
        self.client.configureMQTTOperationTimeout(5)

    def connect(self):
        self.client.connect()

    def publish(self, topic, message):
        self.client.publish(topic, message, 1)

    def subscribe(self,topic):
        self.client.subscribe(topic, 1, printCallback)
