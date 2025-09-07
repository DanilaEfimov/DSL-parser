from typing import Any


class RawData:
    """
    Universal data container that can convert strings, numbers, and sequences
    to a bytearray representation.

    Used in parser trigger callbacks to initialize serialized views over data.
    Supports types: str, int, float, list, tuple, bytes, bytearray.
    """

    def __init__(self, data: Any):
        self._data = data
        self.type = type(data)

        try:
            self.size = len(self._data)
        except TypeError:
            self.size = None

    def __len__(self) -> int:
        if self.size is not None:
            return self.size
        raise TypeError(f"RawData.__len__: object of type '{self.type.__name__}' has no len()")

    def __repr__(self) -> str:
        return f"RawData(type={self.type.__name__}, size={self.size})"

    def as_bytearray(self) -> bytearray:
        """ supported types of self.type:
        bytearray, bytes, str, int, float, list, tuple"""
        data = self._data
        if isinstance(data, bytearray):
            return self._data

        elif isinstance(data, bytes):
            return bytearray(data)

        elif isinstance(data, str):
            return bytearray(data.encode('utf-8'))

        elif isinstance(data, int):
            length = (data.bit_length() + 7) // 8 or 1
            return bytearray(data.to_bytes(length, byteorder='big', signed=True))

        elif isinstance(data, float):
            import struct
            return bytearray(struct.pack("d", data))    # 64-bit float

        elif isinstance(data, (list, tuple)):
            res = bytearray()
            for item in data:
                res.extend(RawData(item).as_bytearray())
            return res

        else:
            try:
                return bytearray(data)
            except TypeError:
                raise TypeError(f"RawData.as_bytearray: object of type '{self.type.__name__}' has no bytearray()")

    def len_in_bytes(self) -> int:
        return len(self.as_bytearray())

    def byte_slice(self,
                   start: int,
                   stop: int,
                   step: int=1) -> bytearray:
        data = self.as_bytearray()
        return data[start:stop:step]



if __name__ == "__main__":
    print("RawData class usage example")

    raw1 = RawData("hello world")
    print("String as bytearray:", raw1.as_bytearray())
    print("Byte slice [0:5]:", raw1.byte_slice(0, 5))
    print("Byte slice [::2]:", raw1.byte_slice(0, len(raw1), 2))

    print()

    raw2 = RawData(123456)
    print("Integer as bytearray:", raw2.as_bytearray())
    print("Byte slice [1:]:", raw2.byte_slice(1, -1))

    print()

    raw3 = RawData([1, 2, 3, 4])
    print("️List as bytearray:", raw3.as_bytearray())
    print("Byte slice [::2]:", raw3.byte_slice(0, len(raw3), 2))
