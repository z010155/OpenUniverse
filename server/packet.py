from abc import ABC

from pyraknet.bitstream import Serializable, WriteStream, c_uint8, c_uint16, c_uint32, ReadStream

from server.enums import ConnectionType


class PacketHeader(Serializable):
    connection_type: ConnectionType
    packet_id: int

    def __init__(self, connection_type: ConnectionType, packet_id: int):
        self.connection_type = connection_type
        self.packet_id = packet_id

    def serialize(self, stream: WriteStream):
        stream.write(c_uint8(0x53))
        stream.write(c_uint16(self.connection_type.value))
        stream.write(c_uint32(self.packet_id))
        stream.write(c_uint8(0))

    @classmethod
    def deserialize(cls, stream: ReadStream) -> "PacketHeader":
        assert stream.read(c_uint8) == 0x53
        connection_type = stream.read(c_uint16)
        packet_id = stream.read(c_uint32)
        assert stream.read(c_uint8) == 0

        return cls(connection_type=connection_type, packet_id=packet_id)


class Packet(Serializable, ABC):
    connection_type: ConnectionType
    packet_id: int

    def serialize(self, stream: WriteStream):
        stream.write(PacketHeader(self.connection_type, self.packet_id))
