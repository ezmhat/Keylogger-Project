import requests
from IWriter import IWriter

class NetworkWriter(IWriter):
    def send_data(self, data, server_url):
        """Envoie les données JSON au serveur Flask"""
        try:
            if isinstance(data, dict):

                response = requests.post(server_url, json=data)

                if response.status_code == 200:
                    print("Sent with success!")
                else:
                    print(f"Error: {response.status_code} - {response.text}")
            else:
                print("Data is not a valid dictionary!")
        except requests.exceptions.RequestException as e:
            print(f"Failed to connect: {e}")
