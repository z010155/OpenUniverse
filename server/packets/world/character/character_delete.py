from pyraknet.bitstream import WriteStream, ReadStream, c_int64, c_uint8

from server.enums import ConnectionType
from server.packet import Packet


class CharacterDeleteRequestPacket(Packet):
    connection_type = ConnectionType.Client
    packet_id = 0x06

    character_id: int

    def __init__(self, character_id: int):
        self.character_id = character_id

    def serialize(self, stream: WriteStream) -> None:
        pass

    @classmethod
    def deserialize(cls, stream: ReadStream) -> "CharacterDeleteRequestPacket":
        return cls(stream.read(c_int64))


class CharacterDeleteResponsePacket(Packet):
    connection_type = ConnectionType.Server
    packet_id = 0x0b

    delete_code: int

    def __init__(self, delete_code: int=0x01):
        self.delete_code = delete_code

    def serialize(self, stream: WriteStream) -> None:
        super().serialize(stream)

        stream.write(c_uint8(self.delete_code))

    @classmethod
    def deserialize(cls, stream: ReadStream) -> "CharacterDeleteResponsePacket":
        return cls()
