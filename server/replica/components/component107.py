from pyraknet.bitstream import WriteStream, c_bit, c_int64

from server.replica.component import Component


class Component107(Component):
    def construct(self, stream: WriteStream):
        self.serialize(stream)

    def serialize(self, stream: WriteStream):
        stream.write(c_bit(True))
        stream.write(c_int64(0))

    def destruct(self):
        pass
