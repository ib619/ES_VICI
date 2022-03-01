import smbus2
import time
import paho.mqtt.client as mqtt
import threading
import numpy as np
import math
from math import copysign

# Initialise constants
MEASURE_INTERVAL = 0.1
FILTER_WINDOW_SIZE = 4
ARRAY_SIZE = 16
NUMBER_OF_PACKETS = 32
REMOVE_GRAVITY_OFFSET = True

# Initialise flags
ARMED_FLAG = True
SPIKED_FLAG = False


class MqttThread(threading.Thread):
    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.client = mqtt.Client("igor_pc")
        self.client.connect("test.mosquitto.org", port=1883)

    def run(self):
        self.client.on_message = self.on_message
        self.client.subscribe("VICI/test/arm")
        self.client.subscribe("VICI/test/disarm")
        self.client.loop_forever()

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        command = msg.payload.decode()
        global ARMED_FLAG
        if topic == "VICI/test/arm":
            client.publish("VICI/test/armed", "armed")
            ARMED_FLAG = True

        if topic == "VICI/test/disarm":
            client.publish("VICI/test/disarmed", "disarmed")
            ARMED_FLAG = False


# Class implementing a real-time moving average filter
# Used to reduce the noise in accelerometer readings
class StreamingMovingAverage:
    def __init__(self, window_size):
        self.window_size = window_size
        self.values = []
        self.sum = 0

    def process(self, value):
        self.values.append(value)
        self.sum += value
        if len(self.values) > self.window_size:
            self.sum -= self.values.pop(0)
        return float(self.sum) / len(self.values)


def get_data_acc1(bus):
    # Get X axis acceleration
    xdata0 = bus.read_byte_data(0x18, 0x28)
    xdata1 = bus.read_byte_data(0x18, 0x29)
    xaccl = xdata1 * 256 + xdata0
    if xaccl > 32767:
        xaccl -= 65536
    xaccl = (xaccl / 16300) * 9.806
    x_out = x_filter_18.process(xaccl)

    # Fill the X axis packet
    global x_arr_18
    x_arr_18.append(x_out)

    # Check array overflow
    if len(x_arr_18) > ARRAY_SIZE:
        x_arr_18.pop(0)

    # Get Y axis acceleration
    ydata0 = bus.read_byte_data(0x18, 0x2A)
    ydata1 = bus.read_byte_data(0x18, 0x2B)
    yaccl = ydata1 * 256 + ydata0
    if yaccl > 32767:
        yaccl -= 65536
    yaccl = (yaccl / 16300) * 9.806
    y_out = y_filter_18.process(yaccl)

    # Fill the Y axis packet
    global y_arr_18
    y_arr_18.append(y_out)

    # Check array overflow
    if len(y_arr_18) > ARRAY_SIZE:
        y_arr_18.pop(0)

    # Get Y axis acceleration
    zdata0 = bus.read_byte_data(0x18, 0x2C)
    zdata1 = bus.read_byte_data(0x18, 0x2D)
    zaccl = zdata1 * 256 + zdata0
    if zaccl > 32767:
        zaccl -= 65536
    zaccl = (zaccl / 16300) * 9.806
    if REMOVE_GRAVITY_OFFSET:
        zaccl -= 9.806
    z_out = z_filter_18.process(zaccl)

    # Fill the Z axis packet
    global z_arr_18
    z_arr_18.append(z_out)

    # Check array overflow
    if len(z_arr_18) > ARRAY_SIZE:
        z_arr_18.pop(0)


def get_data_acc2(bus):
    # Get X axis acceleration
    xdata0 = bus.read_byte_data(0x19, 0x28)
    xdata1 = bus.read_byte_data(0x19, 0x29)
    xaccl = xdata1 * 256 + xdata0
    if xaccl > 32767:
        xaccl -= 65536
    xaccl = (xaccl / 16300) * 9.806
    x_out = x_filter_19.process(xaccl)

    # Fill the X axis packet
    global x_arr_19
    x_arr_19.append(x_out)

    # Check array overflow
    if len(x_arr_19) > ARRAY_SIZE:
        x_arr_19.pop(0)

    # Get Y axis acceleration
    ydata0 = bus.read_byte_data(0x19, 0x2A)
    ydata1 = bus.read_byte_data(0x19, 0x2B)
    yaccl = ydata1 * 256 + ydata0
    if yaccl > 32767:
        yaccl -= 65536
    yaccl = (yaccl / 16300) * 9.806
    y_out = y_filter_19.process(yaccl)

    # Fill the Y axis packet
    global y_arr_19
    y_arr_19.append(y_out)

    # Check array overflow
    if len(y_arr_19) > ARRAY_SIZE:
        y_arr_19.pop(0)

    # Get Y axis acceleration
    zdata0 = bus.read_byte_data(0x19, 0x2C)
    zdata1 = bus.read_byte_data(0x19, 0x2D)
    zaccl = zdata1 * 256 + zdata0
    if zaccl > 32767:
        zaccl -= 65536
    zaccl = (zaccl / 16300) * 9.806
    if REMOVE_GRAVITY_OFFSET:
        zaccl -= 9.806
    z_out = z_filter_19.process(zaccl)

    # Fill the Z axis packet
    global z_arr_19
    z_arr_19.append(z_out)

    # Check array overflow
    if len(z_arr_19) > ARRAY_SIZE:
        z_arr_19.pop(0)


# Initialise the filters for each axis readings
x_filter_18 = StreamingMovingAverage(FILTER_WINDOW_SIZE)
y_filter_18 = StreamingMovingAverage(FILTER_WINDOW_SIZE)
z_filter_18 = StreamingMovingAverage(FILTER_WINDOW_SIZE)

x_filter_19 = StreamingMovingAverage(FILTER_WINDOW_SIZE)
y_filter_19 = StreamingMovingAverage(FILTER_WINDOW_SIZE)
z_filter_19 = StreamingMovingAverage(FILTER_WINDOW_SIZE)

# Initialise containers for the accelerometer
x_arr_18 = [0]
y_arr_18 = [0]
z_arr_18 = [0]

x_arr_19 = [0]
y_arr_19 = [0]
z_arr_19 = [0]

# Get I2C bus
bus = smbus2.SMBus(1)

# Setup the accelerometer 1 for reading in interval -2g/2g
bus.write_byte_data(0x18, 0x20, 0x27)
bus.write_byte_data(0x18, 0x23, 0x00)
time.sleep(0.5)

# Setup the accelerometer 2 for reading in interval -2g/2g
bus.write_byte_data(0x19, 0x20, 0x27)
bus.write_byte_data(0x19, 0x23, 0x00)
time.sleep(0.5)

# Starting MQTT thread
mqtt_thread = MqttThread(1, "MQTT-Thread")
mqtt_thread.start()

def angle_calculator(x,y,z):
    sign = lambda a: copysign(1,a)
    u = 0.01
    pitch = np.arctan2(y,sign(z)*np.sqrt(np.power(z,2)+(u*np.power(x,2))))
    roll = np.arctan2((-x),(np.sqrt(np.power(y,2) + np.power(z,2))))
    yaw = np.arctan2(np.sqrt(np.power(x,2)+np.power(y,2)),z)
    return np.rad2deg(pitch),np.rad2deg(roll),np.rad2deg(yaw)

angle_roll = 0
angle_pitch = 0
angle_yaw = 0

x_angle = 0
y_angle = 0
z_angle = 0
# --------------------------------------- MAIN LOOP -------------------------------------------
while True:
    if ARMED_FLAG:
        get_data_acc1(bus)
        get_data_acc2(bus)
        time.sleep(MEASURE_INTERVAL)

    x_angle, y_angle, z_angle = angle_calculator(x_arr_19[-1], y_arr_19[-1], z_arr_19[-1])
    print(f"Differential X data - {x_arr_18[-1] - x_arr_19[-1]}")
    print(f"Differential Y data - {y_arr_18[-1] - y_arr_19[-1]}")
    print(f"Differential Z data - {z_arr_18[-1] - z_arr_19[-1]}\n")

    print(f" x_angle - {x_angle}\n")
    print(f" y_angle - {y_angle}\n")
    print(f" z_angle - {z_angle}\n")

    time.sleep(1)