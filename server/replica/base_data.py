from typing import List

from pyraknet.bitstream import WriteStream, c_int64, c_int32, c_uint8, c_uint32, c_bit, c_float
from pyraknet.replicamanager import Replica

from server.replica.component import Component


class BaseData(Replica):
    object_id: int
    lot: int
    name: str
    time_since_created: int
    trigger: bool
    spawner_id: int
    spawner_node_id: int
    scale: float
    components: List[Component]

    def __init__(self, object_id: int, lot: int, name: str, time_since_created: int, components: List[Component],
                 trigger: bool=False, spawner_id: int=None, spawner_node_id: int=None, scale: float=None):
        self.object_id = object_id
        self.lot = lot
        self.name = name
        self.time_since_created = time_since_created
        self.trigger= trigger
        self.spawner_id = spawner_id
        self.spawner_node_id = spawner_node_id
        self.scale = scale
        self.components = components

    def write_construction(self, stream: WriteStream):
        stream.write(c_int64(self.object_id))
        stream.write(c_int32(self.lot))
        stream.write(self.name, length_type=c_uint8)
        stream.write(c_uint32(self.time_since_created))
        stream.write(c_bit(False))
        stream.write(c_bit(self.trigger))

        stream.write(c_bit(self.spawner_id is not None))
        if self.spawner_id is not None:
            stream.write(c_int64(self.spawner_id))

        stream.write(c_bit(self.spawner_node_id is not None))
        if self.spawner_node_id is not None:
            stream.write(c_uint32(self.spawner_node_id))

        stream.write(c_bit(self.scale is not None))
        if self.scale is not None:
            stream.write(c_float(self.scale))

        stream.write(c_bit(False))
        stream.write(c_bit(False))

        stream.write(c_bit(True))
        stream.write(c_bit(False))
        stream.write(c_bit(False))

        for c in self.components:
            c.construct(stream)

    def serialize(self, stream: WriteStream):
        stream.write(c_bit(True))
        stream.write(c_bit(False))
        stream.write(c_bit(False))

        for c in self.components:
            c.serialize(stream)

    def on_destruction(self):
        pass
