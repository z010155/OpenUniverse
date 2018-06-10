from pyraknet.bitstream import WriteStream, c_bit

from server.replica.component import Component


class SkillComponent(Component):
    def construct(self, stream: WriteStream):
        stream.write(c_bit(False))

    def serialize(self, stream: WriteStream):
        pass

    def destruct(self):
        pass
