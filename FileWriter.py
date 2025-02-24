import json
import os
from datetime import datetime
from IWriter import IWriter

class FileWriter(IWriter):
    def send_data(self, data, name_machine):
        # Récupérer la date du jour au format YYYY-MM-DD
        today_date = datetime.today().strftime("%Y-%m-%d")

        # Construire le chemin du dossier: data/name_machine/today_date/
        directory = os.path.join("data", name_machine,)

        # Créer les dossiers s'ils n'existent pas
        os.makedirs(directory, exist_ok=True)

        # Nom du fichier dans le dossier créé
        filename = os.path.join(directory, f"{today_date}.txt")

        # Écrire les données dans le fichier
        with open(filename, "a", encoding="utf-8") as file:
            file.write(json.dumps(data, indent=4) + "\n")

        print(f"Data written to {filename}")

