from auth.domain.entities import User

def user_to_dict(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "password": user.password,
        "status": user.status,
    }
    
def user_from_dict(user_dict: dict) -> User:
    return User(
        id=user_dict["id"],
        username=user_dict["username"],
        password=user_dict["password"],
        status=user_dict["status"],
    )