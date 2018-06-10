from pyraknet.bitstream import WriteStream, ReadStream, c_uint16, c_uint8, c_uint32, c_bool, c_uint64

from server.enums import ConnectionType
from server.packet import Packet


class LoginInfoPacket(Packet):
    connection_type = ConnectionType.Auth
    packet_id = 0x00

    username: str
    password: str
    lang_id: int
    platform_type: int
    memory_info: str
    gpu_info: str
    cpu_cores: int
    cpu_type: int
    cpu_lvl: int
    cpu_rev: int
    os_major_ver: int
    os_minor_ver: int
    os_build_num: int
    os_platform_id: int

    login_code: int
    user_key: str
    char_ip: str
    chat_ip: str
    char_port: int
    chat_port: int
    ip: str
    locale: str
    first_login_sub: bool
    free_to_play: bool
    error: str

    def __init__(self, **kwargs):
        if kwargs.get('username'):
            self.username = kwargs['username']
            self.password = kwargs['password']
            self.lang_id = kwargs['lang_id']
            self.platform_type = kwargs['platform_type']
            self.memory_info = kwargs['memory_info']
            self.gpu_info = kwargs['gpu_info']
            self.cpu_cores = kwargs['cpu_cores']
            self.cpu_type = kwargs['cpu_type']
            self.cpu_lvl = kwargs['cpu_lvl']
            self.cpu_rev = kwargs['cpu_rev']
            self.os_major_ver = kwargs['os_major_ver']
            self.os_minor_ver = kwargs['os_minor_ver']
            self.os_build_num = kwargs['os_build_num']
            self.os_platform_id = kwargs['os_platform_id']
        else:
            self.login_code = kwargs.get('login_code', 0x01)
            self.user_key = kwargs['user_key']
            self.char_ip = kwargs.get('char_ip', '127.0.0.1')
            self.chat_ip = kwargs.get('chat_ip', '127.0.0.1')
            self.char_port = kwargs.get('char_port', 2002)
            self.chat_port = kwargs.get('chat_port', 2001)
            self.ip = kwargs.get('ip', '127.0.0.1')
            self.locale = kwargs.get('locale', 'US')
            self.first_login_sub = kwargs.get('first_login_sub', False)
            self.free_to_play = kwargs.get('free_to_play', False)
            self.error = kwargs.get('error')

    def serialize(self, stream: WriteStream):
        stream.write(c_uint8(0x53))
        stream.write(c_uint16(0x05))
        stream.write(c_uint32(0x00))
        stream.write(c_uint8(0))

        stream.write(c_uint8(self.login_code))
        stream.write(b'Talk_Like_A_Pirate', allocated_length=33)

        for _ in range(7):
            stream.write(b'', allocated_length=33)

        stream.write(c_uint16(1))
        stream.write(c_uint16(10))
        stream.write(c_uint16(64))

        stream.write(self.user_key, allocated_length=33)

        stream.write(self.char_ip.encode('latin1'), allocated_length=33)
        stream.write(self.chat_ip.encode('latin1'), allocated_length=33)

        stream.write(c_uint16(self.char_port))
        stream.write(c_uint16(self.chat_port))

        stream.write(self.ip.encode('latin1'), allocated_length=33)

        stream.write(b'00000000-0000-0000-0000-000000000000', allocated_length=37)

        stream.write(c_uint32(0))

        stream.write(self.locale.encode('latin1'), allocated_length=3)

        stream.write(c_bool(self.first_login_sub))
        stream.write(c_bool(self.free_to_play))

        stream.write(c_uint64(0))

        if self.error:
            stream.write(c_uint16(len(self.error)))
            stream.write(self.error, allocated_length=len(self.error))
        else:
            stream.write(c_uint16(0))

        stream.write(c_uint32(4))

    @classmethod
    def deserialize(cls, stream: ReadStream) -> "LoginInfoPacket":
        return cls(username=stream.read(str, allocated_length=33), password=stream.read(str, allocated_length=41),
                   lang_id=stream.read(c_uint16), platform_type=stream.read(c_uint8),
                   memory_info=stream.read(str, allocated_length=256), gpu_info=stream.read(str, allocated_length=128),
                   cpu_cores=stream.read(c_uint32), cpu_type=stream.read(c_uint32), cpu_lvl=stream.read(c_uint16),
                   cpu_rev=stream.read(c_uint16), unknown1=stream.read(c_uint32), os_major_ver=stream.read(c_uint32),
                   os_minor_ver=stream.read(c_uint32), os_build_num=stream.read(c_uint32),
                   os_platform_id=stream.read(c_uint32))