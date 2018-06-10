from typing import Optional, List

from pyraknet.bitstream import WriteStream, Serializable, c_int64, c_int32, c_uint32, c_uint16, c_bit

from server.replica.component import Component


class InventoryItem(Serializable):
    object_id: int
    lot: int
    amount: Optional[int]
    slot: Optional[int]

    def __init__(self, object_id: int, lot: int, amount: int=None, slot: int=None):
        self.object_id = object_id
        self.lot = lot
        self.amount = amount
        self.slot = slot

    def serialize(self, stream: WriteStream):
        stream.write(c_int64(self.object_id))
        stream.write(c_int32(self.lot))

        stream.write(c_bit(False))

        stream.write(c_bit(self.amount is not None))
        if self.amount is not None:
            stream.write(c_uint32(self.amount))

        stream.write(c_bit(self.slot is not None))
        if self.slot is not None:
            stream.write(c_uint16(self.slot))

        stream.write(c_bit(True))
        stream.write(c_uint32(4))

        stream.write(c_bit(False))  # TODO: implement metadata

        stream.write(c_bit(False))


class InventoryComponent(Component):
    items: List[InventoryItem]

    def __init__(self, items: List[InventoryItem]):
        self.items = items

    def construct(self, stream: WriteStream):
        self.serialize(stream)

    def serialize(self, stream: WriteStream):
        stream.write(c_bit(True))
        stream.write(c_uint32(len(self.items)))
        for item in self.items:
            stream.write(item)

        stream.write(c_bit(True))
        stream.write(c_uint32(0))

    def destruct(self):
        pass