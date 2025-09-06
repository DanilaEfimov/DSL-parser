from abc import ABC, abstractmethod

from basedataview import BaseDataView
from dslentities.basetrigger import BaseTrigger

class BaseParser(ABC):

    def __init__(self):
        self._cursor: int = 0
        self._triggers: list[BaseTrigger] = []

    @abstractmethod
    def process(self, data, *,
                start:int=0) -> BaseDataView:
        """
        must be overloaded
        :param data: it can be text or byte array
        :param start: integer point, where parser start to processing
        :return: object as BaseDataView oriented class
        """
        pass

    def get_cursor(self) -> int:
        return self._cursor

    @abstractmethod
    def peek(self) -> str:
        """
        :return: next char for cursor
        """
        pass

    def add_trigger(self, trigger: BaseTrigger) -> None:
        self._triggers.append(trigger)

    def get_triggers(self) -> list[BaseTrigger]:
        return self._triggers
    