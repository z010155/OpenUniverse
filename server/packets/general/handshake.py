import os

from pyraknet.bitstream import WriteStream, ReadStream, c_uint16, c_uint32

from server.packet import Packet
from server.enums import ConnectionType


class HandshakePacket(Packet):
    connection_type = ConnectionType.General
    packet_id = 0x00

    game_version: int
    remote_connection_type: int
    pid: int
    port: int
    ip: str

    def __init__(self, **kwargs):
        self.game_version = kwargs.get('game_version', 171022)
        self.remote_connection_type = kwargs.get('remote_connection_type') or 1 if kwargs.get('auth') else 4
        self.pid = kwargs.get('pid', os.getpid())
        self.port = kwargs.get('port', 0xff)
        self.ip = kwargs.get('ip', '127.0.0.1')

    def serialize(self, stream: WriteStream):
        super().serialize(stream)

        stream.write(c_uint32(self.game_version))
        stream.write(c_uint32(0x93))
        stream.write(c_uint32(self.remote_connection_type))
        stream.write(c_uint32(self.pid))
        stream.write(c_uint16(self.port))
        stream.write(self.ip.encode('latin1'), allocated_length=33)

    @classmethod
    def deserialize(cls, stream: ReadStream) -> "HandshakePacket":
        game_version = stream.read(c_uint32)
        assert stream.read(c_uint32) == 0
        remote_connection_type = stream.read(c_uint32)
        pid = stream.read(c_uint32)
        port = stream.read(c_uint16)
        ip = stream.read(bytes, allocated_length=33).decode('latin1')

        return cls(game_version=game_version, remote_connection_type=remote_connection_type, pid=pid, port=port, ip=ip)