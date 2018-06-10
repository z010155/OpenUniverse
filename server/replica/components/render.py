from typing import List

from pyraknet.bitstream import WriteStream, c_uint32, Serializable, c_uint8, c_float, c_int64, ReadStream

from server.replica.component import Component


class FXEffect(Serializable):
    name: str
    effect_id: int
    effect_type: str
    scale: float
    secondary: int

    def __init__(self, name: str, effect_id: int, effect_type: str, scale: float, secondary: int):
        self.name = name
        self.effect_id = effect_id
        self.effect_type = effect_type
        self.scale = scale
        self.secondary = secondary

    def serialize(self, stream: WriteStream):
        stream.write(self.name.encode('latin1'), length_type=c_uint8)
        stream.write(c_uint32(self.effect_id))
        stream.write(self.effect_type, length_type=c_uint8)
        stream.write(c_float(self.scale))
        stream.write(c_int64(self.secondary))

    @classmethod
    def deserialize(cls, stream: ReadStream):
        pass


class RenderComponent(Component):
    disabled: bool
    effects: List[FXEffect]

    def __init__(self, disabled: bool=False, effects: List[FXEffect]=[]):
        self.disabled = disabled
        self.effects = effects

    def construct(self, stream: WriteStream):
        if not self.disabled:
            stream.write(c_uint32(len(self.effects)))
            for effect in self.effects:
                stream.write(effect)

    def serialize(self, stream: WriteStream):
        pass

    def destruct(self):
        pass
