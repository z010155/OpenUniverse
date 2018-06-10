from pyraknet.bitstream import WriteStream, ReadStream

from server.enums import ConnectionType
from server.packet import Packet


class SessionInfoPacket(Packet):
    connection_type = ConnectionType.Server
    packet_id = 0x01

    username: str
    user_key: str
    hashed: str

    def __init__(self, username: str, user_key: str, hashed: str):
        self.username = username
        self.user_key = user_key
        self.hashed = hashed

    def serialize(self, stream: WriteStream):
        pass

    @classmethod
    def deserialize(cls, stream: ReadStream) -> "SessionInfoPacket":
        return cls(stream.read(str, allocated_length=33), stream.read(str, allocated_length=33),
                   stream.read(bytes, allocated_length=33).decode('latin1'))
