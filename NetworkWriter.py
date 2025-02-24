import requests
from datetime import datetime
from IWriter import IWriter


class NetworkWriter(IWriter):
    def send_data(self, data, name_machine):
        try:
            if isinstance(data, dict):
                today_date = datetime.today().strftime("%Y-%m-%d")

                url = f"{name_machine}/{today_date}"

                response = requests.post(url, json=data)

                if response.status_code == 200:
                    print("Sent with success!")
                else:
                    print(f"Error: {response.status_code} - {response.text}")
            else:
                print("Data is not a valid dictionary!")
                print(type(data))

        except requests.exceptions.RequestException as e:
            print(f"Failed to connect: {e}")
