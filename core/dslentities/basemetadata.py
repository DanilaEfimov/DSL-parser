from abc import abstractmethod
from typing import Any

from core.basedslentity import BaseDslEntity


class BaseMetaData(BaseDslEntity):
    def __init__(self, value: Any, size: int):
        self.value = value
        self.size = size

    @abstractmethod
    def __len__(self):
        return self.size
