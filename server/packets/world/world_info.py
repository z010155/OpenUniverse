from pyraknet.bitstream import WriteStream, ReadStream, c_uint16, c_uint32, c_float

from server.enums import ConnectionType
from server.packet import Packet
from server.zone_reader import Vector3


class WorldInfoPacket(Packet):
    connection_type = ConnectionType.Server
    packet_id = 0x02

    zone_id: int
    instance: int
    clone: int
    checksum: int
    position: Vector3
    activity: bool

    def __init__(self, zone_id: int, instance: int, clone: int, checksum: int, position: Vector3, activity: bool=False):
        self.zone_id = zone_id
        self.instance = instance
        self.clone = clone
        self.checksum = checksum
        self.position = position
        self.activity = activity

    def serialize(self, stream: WriteStream):
        super().serialize(stream)

        stream.write(c_uint16(self.zone_id))
        stream.write(c_uint16(self.instance))
        stream.write(c_uint32(self.clone))
        stream.write(c_uint32(self.checksum))
        stream.write(c_uint16(0))
        stream.write(c_float(self.position.x))
        stream.write(c_float(self.position.y))
        stream.write(c_float(self.position.z))
        stream.write(c_uint32(4 if self.activity else 0))

    @classmethod
    def deserialize(cls, stream: ReadStream) -> "WorldInfoPacket":
        pass