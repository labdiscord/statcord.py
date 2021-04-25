# coding=utf-8
class StatcordException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)


class RequestFailure(StatcordException):
    def __init__(self, status: int, response: str):
        self.status = status
        self.response = response
        super().__init__("{}: {}".format(status, response))


class TooManyRequests(RequestFailure):
    def __init__(self, status: int, response: str, wait: int):
        self.wait = wait
        super().__init__(status, response)
