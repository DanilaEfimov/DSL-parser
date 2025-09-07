from abc import ABC, abstractmethod


class BaseDslEntity(ABC):
    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def get_value(self):
        pass
    