import uuid
from katalog.domain.services import IdGeneratorService

class UuidGeneratorService(IdGeneratorService):
    def generate_id(self) -> str:
        return str(uuid.uuid4())