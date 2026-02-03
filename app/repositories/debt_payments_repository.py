from abc import ABC, abstractmethod
from typing import Optional, List


class DebtPaymentsRepository(ABC):
    """Repository interface for DebtPayments related operations."""

    @abstractmethod
    def save(self, entity) -> object:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[object]:
        pass

    @abstractmethod
    def get_by_id_and_userid(self, entity_id: int, user_id: int) -> Optional[object]:
        pass

    @abstractmethod
    def get_all(self) -> List[object]:
        pass

    @abstractmethod
    def get_all_by_user(self, user_id: int) -> List[object]:
        pass

    @abstractmethod
    def update(self, entity) -> object:
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        pass
