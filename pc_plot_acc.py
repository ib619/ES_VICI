import threading
import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Initialise constants
ACCEL_AXIS_MIN = -0.5
ACCEL_AXIS_MAX = 0.5


# Initialise containers for plotting accelerometer data
x_acceleration = []
y_acceleration = []
z_acceleration = []
t_values = []


def on_message(client, userdata, msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    m_in = json.loads(m_decode)

    # decode X axis data from string to float list
    x_lst = m_in["x"].split(',')
    x_float_list = list(map(float, x_lst))

    # decode Y axis data from string to float list
    y_lst = m_in["y"].split(',')
    y_float_list = list(map(float, y_lst))

    # decode z axis data from string to float list
    z_lst = m_in["z"].split(',')
    z_float_list = list(map(float, z_lst))

    # append received data to our containers
    global x_acceleration
    x_acceleration = x_acceleration + x_float_list

    global y_acceleration
    y_acceleration = y_acceleration + y_float_list

    global z_acceleration
    z_acceleration = z_acceleration + z_float_list

    # extend the time axis
    for el in x_lst:
        t_values.append(len(t_values))


def animate(i):
    plt.cla()
    plt.plot(t_values, x_acceleration, label="X-Axis")
    plt.plot(t_values, y_acceleration, label="Y-Axis")
    plt.plot(t_values, z_acceleration, label="Z-Axis")
    plt.legend(loc="center left")


class MqttThread (threading.Thread):
    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name

    def run(self):
        client = mqtt.Client("igor_pc")
        client.connect("broker.hivemq.com", port=1883)
        client.on_message = on_message
        client.subscribe("IC.embedded/VICI/#")
        client.loop_forever()


mqtt_thread = MqttThread(1, "MQTT-Thread")
mqtt_thread.start()

plt.style.use("fivethirtyeight")
ani = FuncAnimation(plt.gcf(), animate, interval=2000)
plt.tight_layout()
plt.ylim(ACCEL_AXIS_MIN, ACCEL_AXIS_MAX)
plt.show()
