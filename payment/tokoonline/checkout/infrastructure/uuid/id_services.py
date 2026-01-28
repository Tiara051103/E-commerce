import uuid
from checkout.domain.services import IdGeneratorService

class UuidGeneratorService:
    def generate(self) -> str:
        return str(uuid.uuid4())
