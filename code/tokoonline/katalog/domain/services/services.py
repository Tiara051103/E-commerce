from abc import ABC, abstractmethod

class IdGeneratorService(ABC):
    @staticmethod
    def generate_id() -> str:
        pass