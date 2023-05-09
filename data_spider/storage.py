import csv
import json
import os
import requests
import hashlib
import threading
from enum import Enum
from .exceptions import StorageError
from .utils import DataProcess
from .scheduler import *


class BatchDownloader:
    def __init__(self, download_dir: str, thread_num: int):
        self.download_dir = download_dir
        self.thread_num = thread_num
        self.response = None
        self.main_scheduler = Scheduler()
        self.csv_scheduler = Scheduler()
        self.counter = Counter()
        self.index = 1
        self.chunk_size = 1024
        self.timeout = 120

    def __task_ready(self, items):
        for item in items:
            for filename, urls in item.items():
                if isinstance(urls, str):
                    print(f"You need to write an external process method to the rule to process the data into a "
                          f"list (split methods, etc.)."
                          f"\ndata:\n{urls}")
                    return False
                for url in urls:
                    self.main_scheduler.add_task(Task(url))
                    self.counter.add()
        return True

    def download(self, items):
        if self.__task_ready(items):
            if not os.path.exists(self.download_dir):
                os.makedirs(self.download_dir)
            for i in range(self.thread_num):
                work_thread = threading.Thread(target=self.download_files)
                work_thread.start()

    def download_files(self):
        while True:
            task = self.main_scheduler.get_task()
            if task is None:
                break
            url = task.url
            url_file = DataProcess.get_url_file(url)
            filename = url_file or f"file-{self.index}.{DataProcess.get_url_type(url)}"
            filepath = os.path.join(self.download_dir, filename)
            if os.path.exists(filepath):
                print(f"\r{filename} already exists, skipped.")
                continue
            try:
                self.download_file(url, filepath)
            except Exception as e:
                print(f"\rFailed to download {filename} ({str(e)}).")
                self.main_scheduler.add_task(Task(url))
            else:
                print(f"\r{filename} downloaded successfully.")
            finally:
                self.main_scheduler.finish_task()

    def download_file(self, url, filepath):
        self.response = requests.get(url, stream=True, timeout=self.timeout)
        file_size = int(self.response.headers.get('Content-Length', 0))
        progress = 0
        md5_hash = hashlib.md5()
        with open(filepath, 'wb') as f:
            for chunk in self.response.iter_content(self.chunk_size):
                if chunk:
                    f.write(chunk)
                    md5_hash.update(chunk)
                    progress += len(chunk)
                    if file_size > 0:
                        percent = progress * 100 / file_size
                        print(f"\r{filepath} - {percent:.2f}% downloaded", end='')
        if 0 < file_size != progress:
            os.remove(filepath)
            raise Exception("File download incomplete.")
        if 'ETag' in self.response.headers:
            etag = self.response.headers['ETag']
            if etag[0] == etag[-1] == '"':
                etag = etag[1:-1]
            if etag != md5_hash.hexdigest():
                os.remove(filepath)
                raise Exception("File checksum does not match.")

    def __csv_task_ready(self, csv_file: str, url_col_index: int, name_col_index: int):
        try:
            with open(csv_file, "r", encoding="utf-8") as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)
                for row_index, row in enumerate(csv_reader):
                    url_list = eval(row[url_col_index - 1])
                    if name_col_index:
                        name_list = eval(row[name_col_index - 1])
                        for url, name in zip(url_list, name_list):
                            file_suffix = url.split(".")[-1]
                            default_name = f"{name}.{file_suffix}" if name else url.split("/")[-1]
                            self.csv_scheduler.add_task(CSVTask(url, default_name))
                    else:
                        file_name = f"default_{row_index + 1}"
                        for url in url_list:
                            file_suffix = url.split(".")[-1]
                            self.csv_scheduler.add_task(CSVTask(url, f"{file_name}.{file_suffix}"))
        except Exception as e:
            print(f"csv scheduler ready failed {e}")
            return False
        else:
            return True

    def csv_download(self, csv_file: str, url_col_index: int, name_col_index: int = None):
        if not os.path.exists(csv_file):
            raise StorageError("The csv file does not exist")
        if self.__csv_task_ready(csv_file, url_col_index, name_col_index):
            if not os.path.exists(self.download_dir):
                os.makedirs(self.download_dir)
            for i in range(self.thread_num):
                work_thread = threading.Thread(target=self.__csv_storage, kwargs={"folder": self.download_dir})
                work_thread.start()

    def __csv_storage(self, folder: str):
        while True:
            task = self.csv_scheduler.get_task()
            if task is None:
                break
            args = task.url, os.path.join(folder, task.name)
            try:
                self.download_file(*args)
            except Exception as e:
                print(f"\rFailed to download {task.name} ({str(e)}).")
                self.csv_scheduler.add_task(CSVTask(task.url, task.name))
            else:
                print(f"\r{task.name} downloaded successfully.")
            finally:
                self.csv_scheduler.finish_task()


class StorageType(Enum):
    JSON = "json"
    CSV = "csv"


class Storage:
    def __init__(self, file_path, storage_type: StorageType):
        self.file_path = file_path if f".{storage_type.value}" in file_path else f"{file_path}.{storage_type.value}"
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
