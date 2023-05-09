from __future__ import annotations

import re
import threading

from .fetcher import Fetcher
from .processor import Processor, Rule
from .scheduler import Scheduler, Task
from .storage import Storage, StorageType, BatchDownloader
from .exceptions import FetchError, ProcessError, StorageError, TaskError
from .utils import UserAgentPool
from typing import Iterable


class Spider:
    def __init__(self):
        self.start_urls = []
        self.work_queue = []
        self.rule = None
        self.storage_func = None
        self.thread_num = 1
        self.scheduler = None
        self.fetcher = None
        self.ua_tool = None
        self.processor = None
        self.storage = None
        self.data = []
        self.downloader = None

    def set_params(self, start_urls: Iterable, rule: Rule, storage_func: Storage | StorageType = None,
                   thread_num: int = 1):
        self.start_urls = start_urls
        self.rule = rule
        self.storage_func = storage_func
        self.thread_num = thread_num
        self.scheduler = Scheduler()
        self.fetcher = Fetcher()
        self.ua_tool = self.fetcher.ua_tool
        self.processor = Processor()
        try:
            if isinstance(storage_func, StorageType):
                self.storage = Storage("./default", storage_func)
            elif isinstance(storage_func, Storage):
                self.storage = storage_func
            elif storage_func is None:
                pass
            else:
                raise StorageError("Non-standard. Storage objects or StorageType enumerators are recommended")
        except StorageError as e:
            print(e)

    def start(self):
        for url in self.start_urls:
            self.scheduler.add_task(Task(url))
        for i in range(self.thread_num):
            work_thread = threading.Thread(target=self._start_thread, daemon=False)
            work_thread.start()
            self.work_queue.append(work_thread)

    def _start_thread(self):
        processed_data = None
        while True:
            task = self.scheduler.get_task()
            if task is None:
                self.data.append(processed_data)
                break
            try:
                response = self.fetcher.fetch(task.url)
                processed_data = self.processor.process(response, self.rule)
                if self.storage_func:
                    self.storage.store(processed_data)
                self.scheduler.finish_task()
            except FetchError as e:
                print(e)
            except ProcessError as e:
                print(e)
            except StorageError as e:
                print(e)
            except TaskError as e:
                print(e)
            except AttributeError as e:
                print(e)

    def set_ua(self, category: str, browser: str, ua: str = None):
        if not isinstance(self.ua_tool, UserAgentPool):
            return False
        ua = ua or self.ua_tool.get_user_agent(category, browser)
        self.fetcher.update_headers({"User-Agent": ua})
        return ua

    def set_headers(self, headers: dict, is_override: bool = False):
        if is_override:
            self.fetcher.override_headers(headers)
        self.fetcher.update_headers(headers)

    def join(self):
        for work_thread in self.work_queue:
            work_thread.join()

    def __get_data(self):
        self.join()
        return self.data

    def get(self, *args, data=None, fuzzy: bool = True):
        data = data or self.__get_data()
        if not args:
            return data
        result = data
        for arg in args:
            if isinstance(result, list):
                result = result[arg]
            elif isinstance(result, dict):
                if fuzzy:
                    pattern = re.compile(arg, re.IGNORECASE)
                    result = [v.split("|") if isinstance(v, str) else v for k, v in result.items() if pattern.search(k)]
                else:
                    if not result.get(arg):
                        continue
                    result = result.get(arg).split("|")
        return result

    def download_all(self, dir_: str, thread_num: int = None):
        thread_num = thread_num or self.thread_num
        self.downloader = BatchDownloader(dir_, thread_num)
        for item in self.__get_data():
            if not item:
                continue
            self.downloader.download(item)

    def download_single(self, url: str, filepath: str):
        self.downloader = BatchDownloader("./", thread_num=1)
        self.downloader.download_file(url, filepath)

    def download_csv(self, csv_file: str, dir_: str, url_col_index: int, name_col_index: int = None, thread_num: int = None):
        self.join()
        thread_num = thread_num or self.thread_num
        self.downloader = BatchDownloader(dir_, thread_num)
        self.downloader.csv_download(csv_file, url_col_index, name_col_index)
