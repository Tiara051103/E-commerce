from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class Result:
    def __init__(self, is_success: bool, data=None, message: str = ""):
        self.is_success = is_success
        self.data = data
        self.message = message

