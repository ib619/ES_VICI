import smbus2
import time
import paho.mqtt.client as mqtt
import json


# Initialise constants
MEASURE_INTERVAL = 0.1
FILTER_WINDOW_SIZE = 16
PACKET_SIZE = 16
NUMBER_OF_PACKETS = 6
REMOVE_GRAVITY_OFFSET = True

client = mqtt.Client("igor")
client.connect("broker.hivemq.com", port=1883)

# Initialise containers for the accelerometer
x_arr = []
y_arr = []
z_arr = []

# Initialise a counter for packets sent over mqtt
packet_counter = 0


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


# Initialise the filters for each axis readings
x_filter = StreamingMovingAverage(FILTER_WINDOW_SIZE)
y_filter = StreamingMovingAverage(FILTER_WINDOW_SIZE)
z_filter = StreamingMovingAverage(FILTER_WINDOW_SIZE)


def get_data(bus):
    # Get X axis acceleration
    xdata0 = bus.read_byte_data(0x18, 0x28)
    xdata1 = bus.read_byte_data(0x18, 0x29)
    xaccl = xdata1 * 256 + xdata0
    if xaccl > 32767:
        xaccl -= 65536
    xaccl = (xaccl / 16300) * 9.806
    x_out = x_filter.process(xaccl)

    # Fill the X axis packet
    global x_arr
    x_arr.append(x_out)

    # Get Y axis acceleration
    ydata0 = bus.read_byte_data(0x18, 0x2A)
    ydata1 = bus.read_byte_data(0x18, 0x2B)
    yaccl = ydata1 * 256 + ydata0
    if yaccl > 32767:
        yaccl -= 65536
    yaccl = (yaccl / 16300) * 9.806
    y_out = y_filter.process(yaccl)

    # Fill the Y axis packet
    global y_arr
    y_arr.append(y_out)

    # Get Y axis acceleration
    zdata0 = bus.read_byte_data(0x18, 0x2C)
    zdata1 = bus.read_byte_data(0x18, 0x2D)
    zaccl = zdata1 * 256 + zdata0
    if zaccl > 32767:
        zaccl -= 65536
    zaccl = (zaccl / 16300) * 9.806
    if REMOVE_GRAVITY_OFFSET:
        zaccl -= 9.806
    z_out = z_filter.process(zaccl)

    # Fill the Z axis packet
    global z_arr
    z_arr.append(z_out)

    # if data packets are full send the data via MQTT and empty the containers
    if len(x_arr) == PACKET_SIZE:
        # convert arrays to strings to be sent in JSON format
        datastring_x = ','.join(map(str, x_arr))
        datastring_y = ','.join(map(str, y_arr))
        datastring_z = ','.join(map(str, z_arr))

        # empty the containers
        x_arr = []
        y_arr = []
        z_arr = []

        # increment the counter
        global packet_counter
        packet_counter += 1

        # convert the accelerometer data to JSON
        json_data = {
            "x": f"{datastring_x}",
            "y": f"{datastring_y}",
            "z": f"{datastring_z}"
        }

        data_out = json.dumps(json_data)

        # send the accelerometer data via MQTT
        MSG_INFO = client.publish("IC.embedded/VICI/data", data_out)


# Get I2C bus
bus = smbus2.SMBus(1)

# Setup the accelerometer for reading in interval -2g/2g
bus.write_byte_data(0x18, 0x20, 0x27)
bus.write_byte_data(0x18, 0x23, 0x00)
time.sleep(0.5)

# main loop
# measures data with MEASURE_INTERVAL period, sends NUMBER_OF_PACKETS of data packets via MQTT
while packet_counter < NUMBER_OF_PACKETS:
    get_data(bus)
    time.sleep(MEASURE_INTERVAL)

print("Terminated")