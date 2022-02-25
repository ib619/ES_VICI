import paho.mqtt.client as paho
import sys

client = paho.Client()

if client.connect("test.mosquitto.org", 1883, 60) != 0:
    print("Could not connect to broker!")
    sys.exit(-1)

client.publish("VICI/test/arm", "arm")

client.disconnect()
