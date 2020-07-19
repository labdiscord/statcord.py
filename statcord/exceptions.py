class StatcordException(Exception):
    """Base exception for all statcord exceptions"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RequestFailure(StatcordException):
    """Raised when a request to the statcord api fails"""
    def __init__(self, status: int, response: str):
        super().__init__("{}: {}".format(status, response))
