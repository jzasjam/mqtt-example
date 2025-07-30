import paho.mqtt.client as mqtt
from datetime import datetime
from time import sleep

# This class implements a publisher client for MQTT protocol
# It connects to a broker, publishes messages to a topic, and handles connection events
class Publisher_Client:
    # Constructor to initialise the publisher client with device name and data context
    def __init__(self, client_device, data_context):
        self.mqtt_broker = "broker.hivemq.com"      # MQTT Broker Address (Alternatives: "mqtt.eclipse.org", "test.mosquitto.org", "broker.emqx.io")
        self.mqtt_broker_port = 1883                # MQTT Broker Port
        self.keepalive = 60                         # Keepalive interval in seconds
        self.client_device = client_device          # Device name for the publisher client
        self.data_context = data_context            # Topic to which the client will publish messages
        self.connection_rc_flag = None              # Connection result code flag (to be set after connection)

        # Setup MQTT client
        self.mqtt_client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2) # With Paho 2.0, use CallbackAPIVersion.VERSION2
        self.mqtt_client.on_connect = self.on_connect # On connect call the on_connect method

    # Helper method to get the current date and time in a specific format
    def mydatetime(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # The callback function for when the client receives the CONNACK response from the server
    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("\n[i] CONNECTED AT " + self.mydatetime(), ": Result Code [" + str(rc) + "]")
        self.connection_rc_flag = rc

    # This method connects to the MQTT broker and starts the client loop
    def connect_and_start(self):
        print("[i] CONNECTING TO MQTT BROKER: " + self.mqtt_broker + ":" + str(self.mqtt_broker_port))
        print("[~] CONNECTING: ..", end=".", flush=True)
        self.mqtt_client.connect(self.mqtt_broker, self.mqtt_broker_port) # Connect to the MQTT broker (will call on_connect when done)
        
        self.mqtt_client.loop_start()  # Start networking loop in background

    # This method publishes a message to the specified topic
    def event_publish(self, data):
        info = self.mqtt_client.publish(self.data_context, data) # Publish message to the topic
        info.wait_for_publish() # Wait for the publish to complete
        print("[i] MESSAGE PUBLISHED AT " + self.mydatetime(), ": " + data)

    # This method is called to stop the publisher client
    def stop(self):
        self.mqtt_client.disconnect()
        self.mqtt_client.loop_stop()


# ------------------------------------------

# Main Method
# This is the entry point of the script
if __name__ == '__main__':

    print("================================================")
    print(" MQTT Publisher Client")
    print("================================================")

    # Get Name of the Publisher Client
    device = "publisher_client"

    # Get Topic to which the publisher client will publish messages
    topic = "python/mqtt/jzj"

    # Try to connect to the MQTT broker and start the publisher client
    pc = Publisher_Client(device, topic)
    pc.connect_and_start()

    # Wait until connected to the MQTT broker
    while pc.connection_rc_flag is None:
        print("..", end=".", flush=True)
        sleep(1)

    # Try to publish messages
    print("[i] READY TO PUBLISH MESSAGES TO TOPIC: " + topic)
    print("[i] Press Ctrl+C to stop the publisher client.")
    try:
        # Loop to continuously get input from the user and publish messages
        while True:
            data = input("\n[+] ENTER A MESSAGE:\n[>] ")
            if data != "":
                pc.event_publish(data)
    except KeyboardInterrupt:
        # If Ctrl+C is pressed, stop the publisher client
        print("[X] Stopping publisher...")
        pc.stop()
    except Exception as e:
        # If any other exception occurs, print the error and stop the publisher client
        print("[X] An error occurred: ", str(e))
        pc.stop()
