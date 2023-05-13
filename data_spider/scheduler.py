import queue
import time
import threading


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


class TimerTask(object):
    def __init__(self):
        self.timers = []

    def add_timer(self, timer):
        self.timers.append(timer)

    def start(self):
        try:
            processes = []
            for timer in self.timers:
                p = threading.Thread(target=self.__run_timer, args=(timer,))
                p.start()
                processes.append(p)
            for p in processes:
                p.join()
        except KeyboardInterrupt:
            print("Task termination")

    def __run_timer(self, timer):
        while True:
            # 等待时间到达
            current_time = time.time()
            next_time = current_time + timer.interval
            try:
                time.sleep(max(0, next_time - current_time))
            except KeyboardInterrupt:
                break
            else:
                # 执行任务
                for func in timer.functions:
                    func()
                # 更新定时器下次执行时间
                if timer.once:
                    break


class Timer(object):
    def __init__(self, interval, once=True, time_type: str = "second"):
        self.time_table = {
            "second": 1,
            "minute": 60,
            "hour": 60 * 60,
            "day": 60 * 60 * 24,
            "week": 60 * 60 * 24 * 7,
            "month": 60 * 60 * 24 * 30
        }
        self.interval = interval * self.time_table.get(time_type, self.time_table["second"])
        self.functions = []
        self.once = once  # 只执行一次

    def add_function(self, func):
        self.functions.append(func)


def func1():
    print('func1')


def func2():
    print('func2')


def func3():
    print('func3')


if __name__ == '__main__':
    task = TimerTask()
    timer1 = Timer(0.5, False, time_type="minute")
    timer1.add_function(func1)
    timer1.add_function(func2)
    timer2 = Timer(5, True)
    timer2.add_function(func3)
    task.add_timer(timer1)
    task.add_timer(timer2)
    task.start()
