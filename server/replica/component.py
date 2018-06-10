from abc import ABC, abstractmethod

from pyraknet.bitstream import Serializable, WriteStream, ReadStream


class Component(Serializable, ABC):
    @abstractmethod
    def construct(self, stream: WriteStream):
        pass

    @abstractmethod
    def serialize(self, stream: WriteStream):
        pass

    @abstractmethod
    def destruct(self):
        pass

    @classmethod
    def deserialize(cls, stream: ReadStream) -> "Component":
        return cls()
