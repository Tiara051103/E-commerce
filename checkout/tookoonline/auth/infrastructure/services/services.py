import bcrypt
import uuid

from auth.domain.services import IdGeneratorService, PasswordService

class PasswordService(PasswordService):
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

class IdGeneratorService(IdGeneratorService):
    @staticmethod
    def generate_id() -> str:
        return str(uuid.uuid4())