from abc import ABC, abstractmethod
from typing import List, Optional
from checkout.domain.entities import Checkout, CheckoutItem

class CheckoutRepository(ABC):

    @abstractmethod
    def create(self, checkout: Checkout) -> None:
        pass

    @abstractmethod
    def get_by_id(self, checkout_id: str) -> Optional[Checkout]:
        pass

    @abstractmethod
    def get_by_user(self, id_user: int) -> List[Checkout]:
        pass

    @abstractmethod
    def update_status(self, checkout_id: str, status: str) -> None:
        pass

    @abstractmethod
    def delete_by_checkout(self, checkout_id: str) -> None:
        pass

    @abstractmethod
    def add_many(self, items: List[CheckoutItem]) -> None:
        pass

class CheckoutItemRepository(ABC):

    @abstractmethod
    def add(self, item: CheckoutItem) -> None:
        pass

    @abstractmethod
    def get_by_checkout(self, checkout_id: str) -> List[CheckoutItem]:
        pass
