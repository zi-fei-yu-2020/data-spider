class SpiderMonitor:
    def __init__(self):
        self.path = None
        self.__status = {
            "name": None,
            "begin": None,
            "end": None,
            "run_time": 0,
            "urls": [],
            "ua": None,
            "download_status": None,
            "parser": None,
            "thread_num": 1,
            "scarp_status": "Normal operation"
        }

    def set(self, key, value):
        self.__status[key] = value

    def get(self, key):
        return self.__status.get(key, None)

    def save(self, path: str):
        self.path = path or "./spider-monitor.log"
        with open(self.path, "a+") as fw:
            fw.write(str(self))

    def __str__(self):
        return f"Name: {self.get('name')}\n" \
               f"Begin: {self.get('begin')}    End: {self.get('end')}\n" \
               f"Urls: {self.get('urls')}\n" \
               f"Threads numbers: {self.get('thread_num')}\n" \
               f"Using Parser: {self.get('parser')}\n" \
               f"Using UA: {self.get('ua')}\n" \
               f"Run time: {self.get('run_time')} ms\n" \
               f"Scarp status: {self.get('scarp_status')}\n\n"
