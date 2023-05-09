import traceback
import sys


class FetchError(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"Fetch error: {self.msg}"


class ProcessError(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"Process error: {self.msg}"


class StorageError(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"Storage error: {self.msg}"


class TaskError(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"Task error: {self.msg}"
