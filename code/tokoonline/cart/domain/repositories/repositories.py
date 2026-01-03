from abc import ABC, abstractmethod
from cart.domain.entities import Cart, CartItem


class BaseRepository(ABC):

    @abstractmethod
    def add(self, entity):
        pass

    @abstractmethod
    def update(self, entity):
        pass

    @abstractmethod
    def delete_by_id(self, id: str):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id: str):
        pass


class CartRepository(BaseRepository):

    @abstractmethod
    def get_by_user(id_user: str) -> Cart | None:
        pass

class CartItemRepository(BaseRepository):

    @abstractmethod
    def get_by_cart(id_cart: str) -> list[CartItem]:
        pass

    @abstractmethod
    def get_by_cart_and_produk(id_cart: str, id_produk: str
    ) -> CartItem | None:
        pass
