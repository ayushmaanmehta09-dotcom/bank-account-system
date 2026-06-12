import json
import os


class JsonStorage:
    """Saves and loads the whole bank to a JSON file.

    Keeping the file handling here means the model classes don't need to know
    anything about how they are stored.
    """

    def __init__(self, file_path="bank_data.json"):
        self.file_path = file_path

    def exists(self):
        return os.path.exists(self.file_path)

    def save(self, customers):
        data = {"customers": [c.to_dict() for c in customers]}
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self):
        if not self.exists():
            return {"customers": []}
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)
