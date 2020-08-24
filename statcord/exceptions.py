class StatcordException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RequestFailure(StatcordException):
    def __init__(self, status: int, response: str):
        super().__init__("{}: {}".format(status, response))
