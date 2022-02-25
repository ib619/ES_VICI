from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import StringProperty
import time

class FirstWindow(Screen):
    pass

class SecondWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class MainApp(MDApp):
    current_screen = StringProperty("first")
    def build(self):
        self.title = "VICI"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.primary_hue = "300"
        self.theme_cls.theme_style = "Light"

        return Builder.load_file('vici_app.kv')

    def change_screen(self):
        self.current_screen = "second"


if __name__ == '__main__':
    Window.size = (360, 720)
    MainApp().run()
