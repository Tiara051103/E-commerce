from pydantic import BaseModel

class UserRegisterRequestDTO(BaseModel):
    username: str
    password: str
    
    class Config:
        from_attributes = True
        
class UserLoginRequestDTO(BaseModel):
    username: str
    password: str
    
    class Config:
        from_attributes = True