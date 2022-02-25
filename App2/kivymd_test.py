from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
Window.size = (360, 720)


class MainApp(MDApp):
    def build(self):
        self.title = "VICI"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.primary_hue = "300"
        self.theme_cls.theme_style = "Light"

        return Builder.load_file('kivymd_test.kv')


MainApp().run()
