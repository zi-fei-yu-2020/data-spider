import queue


class Task:
    def __init__(self, url):
        self.url = url


class CSVTask(Task):
    def __init__(self, url, name):
        super().__init__(url)
        self.name = name


class Scheduler:
    def __init__(self):
        self.task_queue = queue.Queue()

    def add_task(self, task):
        self.task_queue.put(task)

    def get_task(self):
        try:
            return self.task_queue.get(block=False)
        except queue.Empty:
            return None

    def finish_task(self):
        self.task_queue.task_done()


class Counter:
    def __init__(self, target_num: int = 0):
        self.current_num = 0
        self.target_num = target_num

    def add(self):
        self.current_num += 1

    def sub(self):
        self.current_num -= 1

    def zero(self):
        self.current_num = 0

    def get(self):
        return self.current_num >= self.target_num
