from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class Result:
    def __init__(self, is_success: bool, data=None, message: str = None):
        self.is_success = is_success
        self.data = data
        self.message = message

    @staticmethod
    def ok(data=None, message: str = None):
        return Result(True, data=data, message=message)

    @staticmethod
    def error(message: str):
        return Result(False, data=None, message=message)
