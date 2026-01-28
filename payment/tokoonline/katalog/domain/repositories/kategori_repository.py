from abc import ABC, abstractmethod
from katalog.domain.entities import Kategori


class KategoriRepository(ABC):

    @abstractmethod
    def add(self, kategori: Kategori) -> None:
        pass

    @abstractmethod
    def update(self, kategori: Kategori) -> None:
        pass

    @abstractmethod
    def delete_by_id(self, id) -> None:
        pass

    @abstractmethod
    def get_all(self) -> list[Kategori]:
        pass

    @abstractmethod
    def get_by_id(self, id) -> Kategori | None:
        pass
