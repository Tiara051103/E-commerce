from abc import ABC, abstractmethod
from datetime import datetime

class IdGeneratorService(ABC):
    @staticmethod
    def generate_id() -> str:
        pass
    
class PasswordService(ABC):
    @staticmethod
    def hash_password(password: str) -> str:
        pass
    
    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        pass