from pyraknet.bitstream import c_bit, WriteStream

from server.replica.component import Component


class DestructibleComponent(Component):
    def construct(self, stream: WriteStream):
        stream.write(c_bit(False))
        stream.write(c_bit(False))

    def serialize(self, stream: WriteStream):
        pass

    def destruct(self):
        pass
