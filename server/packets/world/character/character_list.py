from typing import List

from pyraknet.bitstream import ReadStream, WriteStream, c_uint8, c_uint16, c_uint32, c_int64, c_bool, c_uint64

from server.database.database import Character
from server.enums import ConnectionType
from server.packet import Packet


class CharacterListPacket(Packet):
    connection_type = ConnectionType.Client
    packet_id = 0x02

    front: int
    characters: List[Character]

    def __init__(self, front: int=None, characters: List[Character]=None):
        self.front = front
        self.characters = characters

    def serialize(self, stream: WriteStream) -> None:
        stream.write(c_uint8(0x53))
        stream.write(c_uint16(0x05))
        stream.write(c_uint32(0x06))
        stream.write(c_uint8(0))

        stream.write(c_uint8(len(self.characters)))
        stream.write(c_uint8(self.front))

        for char in self.characters:
            stream.write(c_int64(char.character_id))
            stream.write(c_uint32(0))

            stream.write(char.name, allocated_length=33)
            stream.write(char.unapproved_name, allocated_length=33)

            stream.write(c_bool(char.name_rejected))
            stream.write(c_bool(char.free_to_play))

            stream.write(b'', allocated_length=10)

            stream.write(c_uint32(char.shirt_color))
            stream.write(c_uint32(char.shirt_style))
            stream.write(c_uint32(char.pants_color))
            stream.write(c_uint32(char.hair_style))
            stream.write(c_uint32(char.hair_color))
            stream.write(c_uint32(char.lh))
            stream.write(c_uint32(char.rh))
            stream.write(c_uint32(char.eyebrow_style))
            stream.write(c_uint32(char.eye_style))
            stream.write(c_uint32(char.mouth_style))

            stream.write(c_uint32(0))

            stream.write(c_uint16(char.last_zone))
            stream.write(c_uint32(char.last_clone))
            stream.write(c_uint64(char.last_login.second * 1000))

            stream.write(c_uint16(len(char.items)))
            for item in char.items:
                stream.write(c_uint32(item))

    @classmethod
    def deserialize(cls, stream: ReadStream) -> "CharacterListPacket":
        return cls()
