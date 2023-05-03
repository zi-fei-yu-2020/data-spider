import queue


class Task:
    def __init__(self, url):
        self.url = url


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

    def finish_task(self, task):
        self.task_queue.task_done()
