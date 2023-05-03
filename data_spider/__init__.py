import sys

from .fetcher import Fetcher, Rule
from .processor import Processor
from .scheduler import Scheduler, Task
from .storage import Storage, StorageType
from .exceptions import FetchError, ProcessError, StorageError, TaskError


class Spider:
    def __init__(self):
        self.start_urls = []
        self.parse_func = None
        self.storage_func = None
        self.thread_num = 1
        self.scheduler = None
        self.fetcher = None
        self.processor = None
        self.storage = None

    def set_params(self, start_urls, parse_func, storage_func, thread_num=1):
        self.start_urls = start_urls
        self.parse_func = parse_func
        self.storage_func = storage_func
        self.thread_num = thread_num
        self.scheduler = Scheduler()
        self.fetcher = Fetcher()
        self.processor = Processor()
        if isinstance(storage_func, StorageType):
            self.storage = storage_func()
        else:
            self.storage = storage_func

    def start(self):
        for url in self.start_urls:
            self.scheduler.add_task(Task(url))
        for i in range(self.thread_num):
            self._start_thread()

    def _start_thread(self):
        while True:
            task = self.scheduler.get_task()
            if task is None:
                break
            try:
                response = self.fetcher.fetch(task.url)
                data = self.parse_func(response)
                processed_data = self.processor.process(data)
                self.storage.store(processed_data)
                self.scheduler.finish_task(task)
            except FetchError as e:
                self.scheduler.add_task(task)
                print(f"Fetch error: {e}")
                sys.exit("蜘蛛运行遇到问题啦，现在终止！")
            except ProcessError as e:
                self.scheduler.add_task(task)
                print(f"Process error: {e}")
                sys.exit("蜘蛛运行遇到问题啦，现在终止！")
            except StorageError as e:
                self.scheduler.add_task(task)
                print(f"Storage error: {e}")
                sys.exit("蜘蛛运行遇到问题啦，现在终止！")
            except TaskError as e:
                self.scheduler.add_task(task)
                print(f"Task error: {e}")
                sys.exit("蜘蛛运行遇到问题啦，现在终止！")
