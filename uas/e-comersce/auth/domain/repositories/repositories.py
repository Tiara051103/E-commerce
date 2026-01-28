from abc import ABC, abstractmethod

class BaseRepository(ABC):
    @abstractmethod
    def add(self, entity): pass

    @abstractmethod
    def update(self, entity): pass
    
    @abstractmethod
    def delete_by_id(self, id: str): pass
    
    @abstractmethod
    def get_all(self): pass
    
    @abstractmethod
    def get_by_id(self, id: str): pass
    
class UserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str): pass
    