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
        if isinstance(data, dict):
            data = [data]
        if not data:
            return

        column_names = set()
        for d in data:
            column_names.update(d.keys())
        column_names = sorted(column_names)

        with open(self.file_path, "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(column_names)

        with open(self.file_path, "a", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=column_names)
            for d in data:
                writer.writerow(d)

