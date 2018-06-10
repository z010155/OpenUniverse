from pyraknet.bitstream import WriteStream, ReadStream, c_uint32, c_uint8

from server.enums import ConnectionType
from server.packet import Packet


class CharacterCreateRequestPacket(Packet):
    connection_type = ConnectionType.Client
    packet_id = 0x03

    name: str
    predef1: int
    predef2: int
    predef3: int
    shirt_color: int
    shirt_style: int
    pants_color: int
    hair_style: int
    hair_color: int
    lh: int
    rh: int
    eyebrow_style: int
    eye_style: int
    mouth_style: int

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.predef1 = kwargs['predef1']
        self.predef2 = kwargs['predef2']
        self.predef3 = kwargs['predef3']

        self.shirt_color = kwargs['shirt_color']
        self.shirt_style = kwargs['shirt_style']
        self.pants_color = kwargs['pants_color']
        self.hair_style = kwargs['hair_style']
        self.hair_color = kwargs['hair_color']
        self.lh = kwargs['lh']
        self.rh = kwargs['rh']
        self.eyebrow_style = kwargs['eyebrow_style']
        self.eye_style = kwargs['eye_style']
        self.mouth_style = kwargs['mouth_style']

    def serialize(self, stream: WriteStream) -> None:
        pass

    @classmethod
    def deserialize(cls, stream: ReadStream) -> "CharacterCreateRequest":
        return cls(name=stream.read(str, allocated_length=33), predef1=stream.read(c_uint32),
                   predef2=stream.read(c_uint32), predef3=stream.read(c_uint32),
                   unknown1=stream.read(bytes, allocated_length=9), shirt_color=stream.read(c_uint32),
                   shirt_style=stream.read(c_uint32), pants_color=stream.read(c_uint32),
                   hair_style=stream.read(c_uint32), hair_color=stream.read(c_uint32), lh=stream.read(c_uint32),
                   rh=stream.read(c_uint32), eyebrow_style=stream.read(c_uint32), eye_style=stream.read(c_uint32),
                   mouth_style=stream.read(c_uint32), unknown2=stream.read(c_uint8))


class CharacterCreateResponsePacket(Packet):
    connection_type = ConnectionType.Server
    packet_id = 0x07

    response_code: int

    def __init__(self, response_code: int):
        self.response_code = response_code

    def serialize(self, stream: WriteStream) -> None:
        super().serialize(stream)

        stream.write(c_uint8(self.response_code))

    @classmethod
    def deserialize(cls, stream: "ReadStream") -> "CharacterCreateResponse":
        pass
