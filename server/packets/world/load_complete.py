from pyraknet.bitstream import WriteStream, ReadStream, c_uint16, c_uint32

from server.enums import ConnectionType
from server.packet import Packet


class ClientsideLoadCompletePacket(Packet):
    connection_type = ConnectionType.Client
    packet_id = 0x13

    zone_id: int
    instance: int
    clone: int

    def __init__(self, zone_id: int, instance: int, clone: int):
        self.zone_id = zone_id
        self.instance = instance
        self.clone = clone

    def serialize(self, stream: WriteStream):
        pass

    @classmethod
    def deserialize(cls, stream: ReadStream):
        return cls(stream.read(c_uint16), stream.read(c_uint16), stream.read(c_uint32))