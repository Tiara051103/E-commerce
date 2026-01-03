from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: str
    username: str
    password: str
    status: str