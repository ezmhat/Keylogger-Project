from IWriter import IWriter
import requests

class NetworkWriter(IWriter):
    def send_data(self, data, server_url):
        """Envoie les données JSON au serveur Flask"""
        try:

            if isinstance(data, (dict, list)):
                response = requests.post(server_url, json=data)

                if response.status_code == 200:
                    print("Données envoyées avec succès !")
                else:
                    print(f"Erreur : {response.status_code} - {response.text}")
            else:
                print("Les données ne sont pas un dictionnaire ou une liste valide !")
        except requests.exceptions.RequestException as e:
            print(f"Échec de la connexion : {e}")  