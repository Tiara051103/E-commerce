from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class Result:
    is_success: bool
    data: Any = None
    error: Optional[str] = None
    
    @staticmethod
    def ok(data: Any = None):
        return Result(True, data)
    
    @staticmethod
    def error(error: str):
        return Result(False, None, error)