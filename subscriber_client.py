import paho.mqtt.client as mqtt # MQTT Library for Pub/Sub Clients

from datetime import datetime   # Support date/time functions
from time import sleep          # Support time and delay

# This class implements a subscriber client for MQTT protocol
# It connects to a broker, subscribes to a topic, and listens for messages
class Subscriber_Client:
    mqtt_broker = "broker.hivemq.com"   # MQTT Broker Address (Alternatives: "mqtt.eclipse.org", "test.mosquitto.org", "broker.emqx.io")
    mqtt_broker_port = 1883     # MQTT Broker Port
    keepalive = 60              # Keepalive interval in seconds  
    mqtt_client = None          # MQTT Client instance (to be created in main method)
    topic_interested = None     # Topic to which the client is subscribed

    # Constructor to initialise the subscriber client with a name and topic
    def __init__(self, client_name, topic_interested):
        self.subscriber_client_name = client_name
        self.topic_interested = topic_interested

    # Helper method to get the current date and time in a specific format
    def mydatetime(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # The callback function for when the client receives the CONNACK response from the server
    def on_connect(self, client, userdata, flags, rc, properties=None):
        
        # Print the connection result code
        print("[i] CONNECTED AT " + self.mydatetime() + ": Result Code [" + str(rc) + "]")
        # Subscribe to the topic of interest
        print("[i] SUBSCRIBING TO TOPIC: " + self.topic_interested)
        self.mqtt_client.subscribe(self.topic_interested)
        # Print confirmation of subscription
        print("[i] SUBSCRIPTION COMPLETED AT " + self.mydatetime() + "")
        print("[i] Press Ctrl+C to stop the subscriber client.")
        print("\n[!] WAITING FOR MESSAGES...")

    # Called when message sent from MQTT broker to subscriber
    def on_message(self, client, userdata, msg):
        # Print the message received from the broker
        print("\n[+] MESSAGE RECEIVED AT " + self.mydatetime() + "")
        print("[>] " + str(msg.payload.decode("utf-8")))

    # This method is called to stop the subscriber client
    def stop(self): 
        self.mqtt_client.disconnect()
        self.mqtt_client.loop_stop()

# ------------------------------------------

# Main Method
# This is the entry point of the script
if __name__ == '__main__':
    print("================================================")
    print(" MQTT Subscriber Client")
    print("================================================")

    # Get Name of the Subscriber Client
    #name = input("[>] Please enter the name of a subscriber client: ")
    name = "subscriber_client1"

    # Get Topic to which the subscriber client will subscribe
    #topic = input("Enter the topic/s to which to subscribe: ")       
    topic = "python/mqtt/jzj"

    # Try to connect to the MQTT broker and start the subscriber client
    print("[i] CONNECTING TO MQTT BROKER: " + Subscriber_Client.mqtt_broker + ":" + str(Subscriber_Client.mqtt_broker_port))
    print("[~] CONNECTING: ...")
    try:
        # Create an instance of Subscriber_Client class
        cc = Subscriber_Client(name, topic)  # writing an instance of a class and initialising of class variables.
        cc.mqtt_client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)  # create an instance of a client class. This client class is part of MQTT client library. Most of the functionality required to interact with the MQTT broker will be carried out through the reference of Client class.
        cc.mqtt_client.on_connect = cc.on_connect  # Setting the trigger events for connecting and message receiving from the MQTT broker
        cc.mqtt_client.on_message = cc.on_message  # Setting the trigger event for message receiving from the MQTT broker
        cc.mqtt_client.connect(cc.mqtt_broker, cc.mqtt_broker_port, cc.keepalive)  # Connect with the MQTT server by passing several arguments. In these arguments, the first argument mqtt_broker (host address of mqtt server is compulsory)
        cc.mqtt_client.loop_forever()  # Start the MQTT client loop to process network traffic and dispatch callbacks. This method will block until the client disconnects.
    except KeyboardInterrupt:
        # If Ctrl+C is pressed, stop the subscriber client
        print("[X] Stopping subscriber client...")
        cc.stop()
    except Exception as e:
        # If any other exception occurs, print the error and stop the subscriber client
        print("[X] An error occurred: ", str(e))
        cc.stop()
