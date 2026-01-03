from abc import ABC, abstractmethod
from katalog.domain.entities import Produk, Kategori

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
    
class ProdukRepository(BaseRepository):
    def get_by_id(self, id) -> Produk | None:
        raise NotImplementedError
    
    def get_by_nama(self, nama) -> Produk | None:
        raise NotImplementedError
    
    def get_by_keyword(self, keyword) -> Produk | None:
        raise NotImplementedError
    
    def get_by_filter(self, filter: dict) -> list[Produk] | None:
        raise NotImplementedError
    
class KategoriRepository(BaseRepository):
    pass