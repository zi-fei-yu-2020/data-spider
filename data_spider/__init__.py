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
        self.start_urls, self.rule, self.storage_func, self.thread_num = [], None, None, 1
        self.work_queue = []
        self.__data = []
        self.fetcher, self.storage = None, None
        self.__scheduler, self.__processor = None, None
        self.ua = None
        self.__downloader = None

    def set_params(self, start_urls: Iterable, rule: Rule, storage_func: Storage | StorageType = None,
                   thread_num: int = 1, use_dynamic: bool = False):
        self.start_urls, self.rule, self.thread_num = start_urls, rule, thread_num
        self.__fetcher_init(use_dynamic)
        self.__storage_init(storage_func)
        self.__scheduler, self.__processor = Scheduler(), Processor()

    def __fetcher_init(self, use_dynamic: bool):
        self.fetcher = Fetcher(use_dynamic)
        self.ua = self.fetcher.ua_tool

    def __storage_init(self, storage_func: Storage | StorageType):
        self.storage_func = storage_func
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
            self.__scheduler.add_task(Task(url))
        for i in range(self.thread_num):
            work_thread = threading.Thread(target=self.__start_thread, daemon=False)
            work_thread.start()
            self.work_queue.append(work_thread)

    def __start_thread(self):
        processed_data = None
        while True:
            task = self.__scheduler.get_task()
            if task is None:
                self.__data.append(processed_data)
                break
            try:
                response = self.fetcher.fetch(task.url)
                processed_data = self.__processor.process(response, self.rule)
                if self.storage_func:
                    self.storage.store(processed_data)
                self.__scheduler.finish_task()
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
        if not isinstance(self.ua, UserAgentPool):
            return False
        ua = ua or self.ua.get_user_agent(category, browser)
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
        return self.__data

    def get(self, *args, data=None, fuzzy: bool = True, sep: str = None):
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
                    result = [v.split(sep) if isinstance(v, str) else v for k, v in result.items() if pattern.search(k)]
                else:
                    if not result.get(arg):
                        continue
                    result = result.get(arg).split(sep)
        return result

    def download_all(self, dir_: str, thread_num: int = None):
        thread_num = thread_num or self.thread_num
        self.__downloader = BatchDownloader(dir_, thread_num)
        for item in self.__get_data():
            if not item:
                continue
            self.__downloader.download(item)

    def download_single(self, url: str, filepath: str):
        self.__downloader = BatchDownloader("./", thread_num=1)
        self.__downloader.download_file(url, filepath)

    def download_csv(self, csv_file: str, dir_: str, url_col_index: int, name_col_index: int = None,
                     thread_num: int = None):
        self.join()
        thread_num = thread_num or self.thread_num
        self.__downloader = BatchDownloader(dir_, thread_num)
        self.__downloader.csv_download(csv_file, url_col_index, name_col_index)
