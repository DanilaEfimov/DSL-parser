from abc import ABC, abstractmethod
from collections.abc import Callable

from core.basedataview import BaseDataView
from core.dslentities.basemetadata import BaseMetaData
from core.dslentities.basetrigger import BaseTrigger
from core.dslentities.baseparsemodel import BaseParseModel


CallbackType = Callable[[BaseParseModel, int], int]


class BaseParser(ABC):
    """
    Abstract base class for input data parsers with cursor-based state and trigger-based parsing logic.

    This class defines a generic parsing interface for reading structured data from
    raw inputs (bytes, strings, etc.) using a trigger system and callback mechanisms.

    Parsing architecture:
       Cursor points to the current position in the input stream.
       Metadata fields are parsed first; triggers and raw data follow.

       Example:
           vvv <---------  0 cursor position
           meta_i | meta_i-1 | ... | meta_1 | ***
           ***: callbacks -- vvv -- ... ----------------- vvv
           raw_data_1 | trigger_1 | ... | raw_data_i | trigger_i

    Core components:
    - _cursor: current parsing position
    - _callbacks: trigger -> callback mapping
    - _metadata: list of required metadata fields
    - _cursor_stack: for backtracking support

    To use this class, subclass it and implement:
    - description()
    - process()
    - reset()
    - check_trigger()
    - _triggers_are_prefix_free()

    Typical usage involves binding triggers with `add_trigger()`, binding a meta-reader
    with `set_meta_reader()`, and calling `process()` with input data.

    Note:
       Callback signatures must match: (data: BaseParseModel, cursor: int) -> int
    """

    def __init__(self, name: str):
        self.name: str = name
        self._cursor: int = 0
        self._cursor_stack: list[int] = [self._cursor] # for backtracking e.g.
        self._callbacks: dict[BaseTrigger, CallbackType] = {}
        self._metadata: list[BaseMetaData] = []
        self._meta_reader: CallbackType = CallbackType()

    @staticmethod
    @abstractmethod
    def description() -> str:
        """
        :return: description, hints about this
        format parser class
        """
        pass

    @abstractmethod
    def process(self, data: BaseParseModel, *, start: int = 0) -> BaseDataView:
        """
        while cursor < len(input data)
        iterative cycle: check -> process
        (at process step non explicitly _cursor moving)
        :param data: a text/bytes/.. input
        :param start: start cursor position
        :return: parsed object view
        """
        pass

    @abstractmethod
    def reset(self) -> None:
        """
        returns non running parser state
        cursor = 0 ect.
        """
        pass

    def get_cursor(self) -> int:
        return self._cursor

    def peek(self, inputted, offset: int=0):
        pos: int = self._cursor + offset
        if pos >= len(inputted):
            raise IndexError(f"BaseParser.peek: cursor out of range "
                             f"[current position: {self._cursor}; "
                             f"offset: {offset}; "
                             f"len of inputted data: {len(inputted)}]")
        return inputted[pos]

    def add_trigger(self, trigger: BaseTrigger):
        """
        bind trigger and callback action to parse
        :param trigger: a text/bytes/.. trigger to action
        :return: Callable
        """
        def callback(func: CallbackType):
            self._callbacks[trigger] = func
            return func
        return callback

    def set_meta_reader(self):
        """
        bind metadata sequence and callback action to read
        :return: Callable
        """
        def callback(func: CallbackType):
            self._meta_reader = func
            return func
        return callback

    def get_triggers(self) -> dict[BaseTrigger, CallbackType]:
        return self._callbacks

    def add_metadata(self, data: BaseMetaData) -> None:
        self._metadata.append(data)

    def get_metadata(self) -> list[BaseMetaData]:
        return self._metadata

    @abstractmethod
    def check_trigger(self, data: BaseParseModel) -> None | BaseTrigger:
        """
        this function check any matches with triggers
        at current cursor position (if such exists)
        :param data: a text/bytes/.. input
        :return: None if we haven't any
        trigger patterns; Else BaseTrigger, which
        was matched
        """
        pass

    def minimum_size(self) -> int:
        min_size: int = 0
        for field in self._metadata:
            min_size += len(field)
        return min_size

    @abstractmethod
    def _triggers_are_prefix_free(self) -> bool:
        pass

    # cursor stack can be used by callbacks
    def push_cursor(self) -> None:
        self._cursor_stack.append(self._cursor)

    def pop_cursor(self) -> None:
        if not len(self._cursor_stack):
            raise IndexError("BaseParser.pop_cursor: _cursor_stack is empty")
        self._cursor_stack.pop()

    def top_cursor(self) -> int:
        if not len(self._cursor_stack):
            raise IndexError("BaseParser.top_cursor: _cursor_stack is empty")
        return self._cursor_stack[-1]



if __name__ == "__main__":
    help(BaseParser)
