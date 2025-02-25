import json
import os
from datetime import datetime
from IWriter import IWriter

class FileWriter(IWriter):
    def send_data(self, data, computer_id):
        """Saves logs in the same JSON Lines format as the network logs."""
        try:
            log_dir = f"data/{computer_id}/"
            log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.jsonl")

            # Create directory if it doesn't exist
            os.makedirs(log_dir, exist_ok=True)

            with open(log_file, "a", encoding="utf-8") as f:
                for entry in data:
                    # Each entry should be written as a single JSON object per line
                    json.dump(entry, f)
                    f.write("\n")  # Ensure JSONL format (one object per line)

            print(f"✅ Data successfully written to {log_file}")

        except Exception as e:
            print(f"❌ Error writing data to file: {e}")
