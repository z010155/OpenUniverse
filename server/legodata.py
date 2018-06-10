from typing import Any, List
from xml.etree import ElementTree

from pyraknet.bitstream import ReadStream, Serializable, WriteStream, c_bool, c_double, c_float, c_int32, c_int64, \
    c_uint32, c_uint8

LDF_VALUE_TYPES = {
    0: str,
    1: c_int32,
    2: c_int32,
    3: c_float,
    4: c_double,
    5: c_uint32,
    6: c_uint32,
    7: c_bool,
    8: c_int64,
    9: c_int64,
    13: str
}


class LegoDataNode(Serializable):
    key: str
    value_type: int
    value: Any

    def __init__(self, key: str, value_type: int, value: Any):
        self.key = key
        self.value_type = value_type
        self.value = value

    def serialize(self, stream: WriteStream):
        stream.write(c_uint8(len(self.key) * 2))

        for c in self.key:
            stream.write(c.encode('latin1'))
            stream.write(b'\0')

        stream.write(c_uint8(self.value_type))

        if self.value_type == 0:
            if isinstance(self.value, bytes):
                stream.write(self.value.decode('latin1'), length_type=c_uint32)
            else:
                stream.write(self.value, length_type=c_uint32)
        elif self.value_type == 13:
            if isinstance(self.value, ElementTree.Element):
                stream.write(b'<?xml version="1.0">' + ElementTree.tostring(self.value), length_type=c_uint32)
            elif isinstance(self.value, bytes):
                stream.write(self.value, length_type=c_uint32)
            else:
                stream.write(self.value.encode('latin1'), length_type=c_uint32)
        else:
            stream.write(LDF_VALUE_TYPES[self.value_type](self.value))

    @classmethod
    def deserialize(cls, stream: ReadStream):
        pass


class LegoData(Serializable):
    _nodes: List[LegoDataNode]

    def __init__(self, nodes: List[LegoDataNode]=[]):
        self._nodes = nodes

    def set(self, key: str, value_type: int, value: Any):
        self._nodes.append(LegoDataNode(key, value_type, value))

    def serialize(self, stream: WriteStream):
        stream.write(c_uint32(len(self._nodes)))
        for node in self._nodes:
            stream.write(node)

    @classmethod
    def deserialize(cls, stream: ReadStream) -> "LegoData":
        pass
