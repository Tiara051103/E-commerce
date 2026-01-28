import uuid
from payment.domain.services import IdGeneratorService

class UuidGeneratorService:
    def generate(self) -> str:
        return str(uuid.uuid4())
