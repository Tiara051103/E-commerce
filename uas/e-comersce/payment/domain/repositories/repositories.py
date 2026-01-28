# payment/domain/repositories.py
from abc import ABC, abstractmethod
from typing import Optional, List
from payment.domain.entities import Payment

class PaymentRepository(ABC):

    @abstractmethod
    def create(self, payment: Payment) -> None:
        pass

    @abstractmethod
    def get_by_id(self, payment_id: str) -> Optional[Payment]:
        pass

    @abstractmethod
    def get_by_checkout(self, id_checkout: str) -> Optional[Payment]:
        pass

    @abstractmethod
    def get_by_user(self, id_user: int) -> List[Payment]:
        pass

    @abstractmethod
    def update_status(self, payment_id: str, status: str) -> None:
        pass
