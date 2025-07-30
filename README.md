# MQTT Python Example

##### By Jonathan Zasada-James 

------------------------------
## Setup

#### Prerequisites:  
Check Python is installed
> **`python --version`**

Install 'paho-mqtt' library
> **`pip3 install paho-mqtt`** 

-----------
## How To Use

Download and extract the code or clone the project to your machine in terminal using...
> **`git clone https://github.com/jzasjam/mqtt-example.git`**

### **`publisher_client.py`** 
This is the MQTT publisher script which connects to the broker with a defined topic and allows you to enter a message to publish

Open a new terminal in the project directory and run
> **`python publisher_client.py`**

### **`subscriber_client.py`** 
This is the MQTT subscriber script which connects to the broker and allows you to subscribe to a topic and receive published messages

Open another new terminal in the project directory and run
> **`python subscriber_client.py`**
-------------------------------
