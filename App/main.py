from kivy.app import App
import paho.mqtt.client as mqtt
from kivy.properties import StringProperty, BooleanProperty, NumericProperty


class SPIKE(App):
    protect_status = StringProperty("Your drink is not protected")
    arm_button_disabled = BooleanProperty(False)
    arm_button_text = StringProperty("Arm")

    connect_status = StringProperty("Please connect to your device")
    connect_button_text = StringProperty("Connect")

    shield_protected_width = NumericProperty(0)
    shield_unprotected_width = NumericProperty(1)
    warning_width = NumericProperty(0)

    disconnected_icon_width = NumericProperty(1)
    connected_icon_width = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mqttc = mqtt.Client(client_id="igor_pc")

    def on_start(self):

        def onConnect(client, userdata, flags, rc):
            self.mqttc.subscribe("VICI/test/armed", 0)
            self.mqttc.subscribe("VICI/test/disarmed", 0)
            self.mqttc.subscribe("VICI/test/spike", 0)


        def onMessage(client, userdata, msg):
            msg.payload = msg.payload.decode("utf-8")
            if msg.topic == "VICI/test/armed":
                self.protect_status = "You drink is protected!"
                self.arm_button_disabled = False
                self.warning_width = 0
                self.shield_protected_width = 1
                self.shield_unprotected_width = 0
            if msg.topic == "VICI/test/disarmed":
                self.protect_status = "You drink is not protected!"
                self.arm_button_disabled = False
                self.warning_width = 0
                self.shield_protected_width = 0
                self.shield_unprotected_width = 1
            if msg.topic == "VICI/test/spike":
                self.protect_status = "DANGER:\n You drink was SPIKED!!!"
                self.arm_button_disabled = False
                self.warning_width = 1
                self.shield_protected_width = 0
                self.shield_unprotected_width = 0

        self.mqttc.on_connect = onConnect
        self.mqttc.on_message = onMessage

    def send_arm_message(self, widget):
        if widget.state == "normal":
            self.mqttc.publish("VICI/test/arm", "arm")
            self.protect_status = "Disarming..."
            self.arm_button_text = "Arm"
            self.arm_button_disabled = True
        else:
            self.mqttc.publish("VICI/test/disarm", "disarm")
            self.protect_status = "Arming..."
            self.arm_button_text = "Disarm"
            self.arm_button_disabled = True

    def connect_to_mqtt(self, widget):
        if widget.state == "down":
            self.mqttc.connect("test.mosquitto.org", 1883)
            self.mqttc.loop_start()
            self.connect_status = "Connected"
            self.connect_button_text = "Disconnect"
            self.connected_icon_width = 1
            self.disconnected_icon_width = 0
        else:
            self.mqttc.disconnect()
            self.mqttc.loop_stop()
            self.connect_status = "Please connect to your device"
            self.connect_button_text = "Connect"
            self.connected_icon_width = 0
            self.disconnected_icon_width = 1


SPIKE().run()
