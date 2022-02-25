import paho.mqtt.client as paho
import sys

client = paho.Client()

def onMessage(client, userdata, msg):
    print(msg.topic + ": " + msg.payload.decode())

client = paho.Client()
client.on_message = onMessage

if client.connect("test.mosquitto.org", 1883, 60) != 0:
    print("Could not connect to broker!")
    sys.exit(-1)

client.subscribe("VICI/test/spike")

try:
    print("Press CTRL+C to exit...")
    client.loop_forever()
except:
    print("Disconnected from broker!")

client.disconnect()
