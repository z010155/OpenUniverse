from pyraknet.bitstream import ReadStream, WriteStream, c_int64

from server.enums import ConnectionType
from server.packet import Packet


class WorldJoinRequestPacket(Packet):
    connection_type = ConnectionType.Client
    packet_id = 0x04

    character_id: int

    def __init__(self, character_id: int):
        self.character_id = character_id

    def serialize(self, stream: WriteStream):
        pass

    @classmethod
    def deserialize(cls, stream: ReadStream) -> "WorldJoinRequestPacket":
        return cls(stream.read(c_int64))