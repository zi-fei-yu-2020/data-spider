import sys
import threading

from .fetcher import Fetcher
from .processor import Processor, Rule
from .scheduler import Scheduler, Task
from .storage import Storage, StorageType
from .exceptions import FetchError, ProcessError, StorageError, TaskError
from .utils import UserAgentPool


class Spider:
    def __init__(self):
        self.start_urls = []
        self.rule = None
        self.storage_func = None
        self.thread_num = 1
        self.scheduler = None
        self.fetcher = None
        self.ua_tool = None
        self.processor = None
        self.storage = None

    def set_params(self, start_urls: list, rule: Rule, storage_func, thread_num: int = 1):
        self.start_urls = start_urls
        self.rule = rule
        self.storage_func = storage_func
        self.thread_num = thread_num
        self.scheduler = Scheduler()
        self.fetcher = Fetcher()
        self.ua_tool = self.fetcher.ua_tool
        self.processor = Processor()
        if isinstance(storage_func, StorageType):
            self.storage = storage_func()
        else:
            self.storage = storage_func

    def start(self):
        for url in self.start_urls:
            self.scheduler.add_task(Task(url))
        for i in range(self.thread_num):
            work = threading.Thread(target=self._start_thread, daemon=False)
            work.start()

    def _start_thread(self):
        while True:
            task = self.scheduler.get_task()
            if task is None:
                break
            try:
                response = self.fetcher.fetch(task.url)
                processed_data = self.processor.process(response, self.rule)
                self.storage.store(processed_data)
                self.scheduler.finish_task(task)
            except FetchError as e:
                print(e)
            except ProcessError as e:
                print(e)
            except StorageError as e:
                print(e)
            except TaskError as e:
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

