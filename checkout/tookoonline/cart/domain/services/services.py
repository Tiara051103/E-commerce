import uuid
from abc import ABC, abstractmethod

class IdGeneratorService(ABC):
    @abstractmethod
    def generate_id(self) -> str:
        pass


class UUIDGeneratorService(IdGeneratorService):
    def generate_id(self) -> str:
        return str(uuid.uuid4())
