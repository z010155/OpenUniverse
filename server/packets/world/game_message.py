from pyraknet.bitstream import WriteStream, ReadStream, c_int64, c_uint16

from server.enums import ConnectionType
from server.packet import Packet


class ClientGameMessage(Packet):
    connection_type = ConnectionType.Client
    packet_id = 0x05

    object_id: int
    message_id: int
    data: bytes

    def __init__(self, object_id: int, message_id: int, data: bytes):
        self.object_id = object_id
        self.message_id = message_id
        self.data = data

    def serialize(self, stream: WriteStream):
        pass

    @classmethod
    def deserialize(cls, stream: ReadStream):
        return cls(stream.read(c_int64), stream.read(c_uint16), stream.read_remaining())


class ServerGameMessage(Packet):
    connection_type = ConnectionType.Server
    packet_id = 0x0c

    object_id: int
    message_id: int
    data: bytes

    def __init__(self, object_id: int, message_id: int, data: bytes):
        self.object_id = object_id
        self.message_id = message_id
        self.data = data

    def serialize(self, stream: WriteStream):
        super().serialize(stream)

        stream.write(c_int64(self.object_id))
        stream.write(c_uint16(self.message_id))
        stream.write(self.data)

    @classmethod
    def deserialize(cls, stream: ReadStream):
        pass
