from auth.domain.entities import User
from auth.domain.services import IdGeneratorService, PasswordService
from auth.domain.repositories import (
    UserRepository,
    
)
from auth.application.result import Result

# Authentication
class RegisterUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        id_generator_service: IdGeneratorService,
        password_service: PasswordService,
    ):
        self.user_repository = user_repository
        self.id_generator_service = id_generator_service
        self.password_service = password_service

    def execute(self, username: str, password: str) -> Result:
        id = self.id_generator_service.generate_id()
        password = self.password_service.hash_password(password)
        status = "active"
        user = User(id=id, username=username, password=password, status=status)
        hasil = self.user_repository.add(user)
        return Result.ok()
    
class LoginUserUseCase:
    def __init__(self, user_repository: UserRepository, password_service: PasswordService):
        self.user_repository = user_repository
        self.password_service = password_service

    def execute(self, username: str, password: str) -> Result:
        user = self.user_repository.get_by_username(username)
        if user is None:
            return Result.error("User tidak ditemukan")
        if not self.password_service.check_password(password, user.password):
            return Result.error("Password salah")
        return Result.ok(user)
    
class LogoutUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        
    def execute(self, username: str) -> Result:
        user = self.user_repository.get_by_username(username)
        if user is None:
            return Result.error("User tidak ditemukan")
        return Result.ok(user)

class CheckUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        
    def execute(self, id: str) -> Result:
        user = self.user_repository.get_by_id(id)
        if user is None:
            return Result.error("User tidak ditemukan")
        return Result.ok(user)

