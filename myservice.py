from kivy.app import App
from kivy.uix.label import Label
from android import AndroidService

class SystemForegroundService(AndroidService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def start_service(self):
        self.start_foreground("System Service Running")
    
    def stop_service(self):
        self.stop_foreground()
        self.stop_self()

class MyApp(App):
    def build(self):
        return Label(text="System Service Running")

if __name__ == '__main__':
    MyApp().run()
