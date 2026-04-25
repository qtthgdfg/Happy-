
from jnius import autoclass
from main import AndroidServiceWrapper

PythonService = autoclass('org.kivy.android.PythonService')

class SystemForegroundService(PythonService):
    def start_service(self):
        self.wrapper = AndroidServiceWrapper(self)
        self.wrapper.on_start()
    
    def stop_service(self):
        if hasattr(self, 'wrapper'):
            self.wrapper.on_stop()

if __name__ == '__main__':
    SystemForegroundService().start_service()
