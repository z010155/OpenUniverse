from typing import List

from pyraknet.bitstream import WriteStream, c_bit, c_uint32, c_float, c_int32

from server.replica.component import Component


class StatsComponent(Component):
    health: int
    max_health: int
    armor: int
    max_armor: int
    imagination: int
    max_imagination: int
    factions: List[int]
    smashable: bool

    def __init__(self, health: int=4, max_health: int=4, armor: int=0, max_armor: int=0, imagination: int=0,
                 max_imagination: int=0, factions: List[int]=[1], smashable: bool=False):
        self.health = health
        self.max_health = max_health
        self.armor = armor
        self.max_armor = max_armor
        self.imagination = imagination
        self.max_imagination = max_imagination
        self.factions = factions
        self.smashable = smashable

    def _write_data(self, stream: WriteStream):
        stream.write(c_bit(True))

        stream.write(c_uint32(self.health))
        stream.write(c_float(self.max_health))

        stream.write(c_uint32(self.armor))
        stream.write(c_float(self.max_armor))

        stream.write(c_uint32(self.imagination))
        stream.write(c_float(self.max_imagination))

        stream.write(c_uint32(0))
        stream.write(c_bit(True))
        stream.write(c_bit(False))
        stream.write(c_bit(False))

        stream.write(c_float(self.max_health))
        stream.write(c_float(self.max_armor))
        stream.write(c_float(self.max_imagination))

        stream.write(c_uint32(len(self.factions)))
        for faction in self.factions:
            stream.write(c_int32(faction))

        stream.write(c_bit(self.smashable))

    def construct(self, stream: WriteStream):
        stream.write(c_bit(True))
        for _ in range(9):
            stream.write(c_uint32(0))

        self._write_data(stream)

        stream.write(c_bit(False))
        stream.write(c_bit(False))

        if self.smashable:
            stream.write(c_bit(False))
            stream.write(c_bit(False))

        stream.write(c_bit(True))
        stream.write(c_bit(False))

    def serialize(self, stream: WriteStream):
        self._write_data(stream)

        stream.write(c_bit(True))
        stream.write(c_bit(False))

    def destruct(self):
        pass
