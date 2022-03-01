from kivy.app import App
import paho.mqtt.client as mqtt
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, Clock
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
import time
import ssl


class MyScreenManager(ScreenManager):
    protect_status = StringProperty("Your drink is not protected!")
    arm_button_disabled = BooleanProperty(False)
    arm_button_text = StringProperty("Arm")
    arm_button_state = StringProperty("normal")

    connect_status = StringProperty("Please connect to your device")
    connect_button_text = StringProperty("Connect")

    shield_protected_width = NumericProperty(0)
    shield_unprotected_width = NumericProperty(1)
    warning_width = NumericProperty(0)

    disconnected_icon_width = NumericProperty(1)
    connected_icon_width = NumericProperty(0)
    arm_bool = True

    #protect_msg_color = (227/255, 40/255, 40/255, 1)
    protect_msg_color = (0, 0, 0, 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def timer_callback(self, dt):
        self.arm_bool = False
        self.ids.arm_toggle.state = "normal"
        self.arm_button_disabled = False
        self.protect_status = "Could not arm: Please check connection status"
        Clock.schedule_once(self.enable_arm, 1)

    def enable_arm(self, dt):
        self.arm_bool = True


class SPIKE(App):
    def build(self):
        self.manager = MyScreenManager()
        return self.manager

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mqttc = mqtt.Client()

    def on_start(self):

        def onConnect(client, userdata, flags, rc):
            self.mqttc.subscribe("VICI/test/armed", 0)
            self.mqttc.subscribe("VICI/test/disarmed", 0)
            self.mqttc.subscribe("VICI/test/spike", 0)

        def onMessage(client, userdata, msg):
            msg.payload = msg.payload.decode("utf-8")
            if msg.topic == "VICI/test/armed":
                Clock.unschedule(self.arm_event)
                self.manager.protect_status = "Your drink is protected!"
                self.manager.arm_button_disabled = False
                self.manager.warning_width = 0
                self.manager.shield_protected_width = 1
                self.manager.shield_unprotected_width = 0
            elif msg.topic == "VICI/test/disarmed":
                self.manager.protect_status = "Your drink is not protected!"
                self.manager.arm_button_disabled = False
                self.manager.warning_width = 0
                self.manager.shield_protected_width = 0
                self.manager.shield_unprotected_width = 1
            elif msg.topic == "VICI/test/spike":
                self.manager.protect_status = "DANGER:\n \n Your drink may have been SPIKED!"
                self.manager.arm_button_disabled = False
                self.manager.warning_width = 1
                self.manager.shield_protected_width = 0
                self.manager.shield_unprotected_width = 0

        self.mqttc.on_connect = onConnect
        self.mqttc.on_message = onMessage

    def connect_to_mqtt(self, widget):
        if widget.state == "down":
            if self.mqttc.connect("ec2-13-40-209-250.eu-west-2.compute.amazonaws.com", 1883, 3600) != 0:
                print("Could not connect to broker!")
            self.mqttc.loop_start()
            self.manager.connect_status = "Connected!"
            self.manager.connect_button_text = "Disconnect"
            self.manager.connected_icon_width = 1
            self.manager.disconnected_icon_width = 0
            self.manager.current = "arm"
        else:
            self.mqttc.disconnect()
            self.mqttc.loop_stop()
            self.manager.connect_status = "Please connect to your device"
            self.manager.connect_button_text = "Connect"
            self.manager.connected_icon_width = 0
            self.manager.disconnected_icon_width = 1

    def send_arm_message(self, widget):
        if self.manager.arm_bool:
            if widget.state == "normal":
                self.mqttc.publish("VICI/test/disarm", "disarm")
                self.manager.protect_status = "Disarming..."
                self.manager.arm_button_text = "Arm"
                self.manager.arm_button_disabled = True

            else:
                self.mqttc.publish("VICI/test/arm", "arm")
                self.manager.protect_status = "Arming..."
                self.manager.arm_button_text = "Disarm"
                self.manager.arm_button_disabled = True
                self.arm_event = Clock.schedule_once(self.manager.timer_callback, 8)


if __name__ == '__main__':
    Window.size = (360, 720)
    SPIKE().run()
