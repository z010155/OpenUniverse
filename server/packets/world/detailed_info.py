import zlib

from pyraknet.bitstream import WriteStream, ReadStream, c_uint32, c_bit, c_bool

from server.enums import ConnectionType
from server.legodata import LegoData
from server.packet import Packet


class DetailedUserInfoPacket(Packet):
    connection_type = ConnectionType.Server
    packet_id = 0x04

    ldf: LegoData

    def __init__(self, ldf: LegoData):
        self.ldf = ldf

    def serialize(self, stream: WriteStream):
        super().serialize(stream)

        wstr = WriteStream()
        wstr.write(self.ldf)
        data = bytes(wstr)
        compressed_data = zlib.compress(data)

        stream.write(c_uint32(len(compressed_data) + 9))
        stream.write(c_bool(True))
        stream.write(c_uint32(len(data)))
        stream.write(c_uint32(len(compressed_data)))
        stream.write(compressed_data)

    @classmethod
    def deserialize(cls, stream: ReadStream):
        pass
