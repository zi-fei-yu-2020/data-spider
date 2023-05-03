import csv
import json
from enum import Enum
from .exceptions import StorageError


class StorageType(Enum):
    JSON = "json"
    CSV = "csv"


class Storage:
    def __init__(self, file_path, storage_type):
        self.file_path = file_path
        self.storage_type = storage_type

    def store(self, data):
        if self.storage_type == StorageType.JSON:
            self.store_as_json(data)
        elif self.storage_type == StorageType.CSV:
            self.store_as_csv(data)
        else:
            raise StorageError(f"Unsupported storage type: {self.storage_type}")

    def store_as_json(self, data):
        with open(self.file_path, "a", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
            f.write("\n")

    def store_as_csv(self, data):
        with open(self.file_path, "a", newline='') as f:
            writer = csv.writer(f)
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        row = [key] + value if key != "null" else value
                        writer.writerow(row)
                    elif isinstance(value, str):
                        row = [key, value]
                        writer.writerow(row)
                    else:
                        raise ValueError("Unsupported value type for storing as CSV")
            elif isinstance(data, list):
                for item in data:
                    writer.writerow([item])

