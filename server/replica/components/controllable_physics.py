from typing import Optional

from pyraknet.bitstream import WriteStream, c_bit, c_float, c_uint32

from server.replica.component import Component
from server.zone_reader import Vector3, Quaternion


class ControllablePhysicsComponent(Component):
    jetpack_effect: Optional[int]
    player: bool
    position: Vector3
    rotation: Quaternion
    on_ground: bool
    on_rail: bool
    velocity: Optional[Vector3]
    angular_velocity: Optional[Vector3]
    on_platform: bool

    def __init__(self, **kwargs):
        self.jetpack_effect = kwargs.get('jetpack_effect')
        self.player = kwargs.get('player', False)
        self.position = kwargs.get('position', Vector3.zero())
        self.rotation = kwargs.get('rotation', Quaternion.zero())
        self.on_ground = kwargs.get('on_ground', True)
        self.on_rail = kwargs.get('on_rail', False)
        self.velocity = kwargs.get('velocity')
        self.angular_velocity = kwargs.get('angular_velocity')
        self.on_platform = kwargs.get('on_platform', False)

    def _write_data(self, stream: WriteStream):
        stream.write(c_bit(False))

        stream.write(c_bit(True))
        stream.write(c_float(0))
        stream.write(c_bit(False))

        stream.write(c_bit(True))
        stream.write(c_bit(False))

        stream.write(c_bit(self.player))
        if self.player:
            stream.write(c_float(self.position.x))
            stream.write(c_float(self.position.y))
            stream.write(c_float(self.position.z))

            stream.write(c_float(self.rotation.x))
            stream.write(c_float(self.rotation.y))
            stream.write(c_float(self.rotation.z))
            stream.write(c_float(self.rotation.w))

            stream.write(c_bit(self.on_ground))
            stream.write(c_bit(self.on_rail))

            stream.write(c_bit(self.velocity is not None))
            if self.velocity is not None:
                stream.write(c_float(self.velocity.x))
                stream.write(c_float(self.velocity.y))
                stream.write(c_float(self.velocity.z))

            stream.write(c_bit(self.angular_velocity is not None))
            if self.angular_velocity is not None:
                stream.write(c_float(self.angular_velocity.x))
                stream.write(c_float(self.angular_velocity.y))
                stream.write(c_float(self.angular_velocity.z))

            stream.write(c_bit(False))

    def construct(self, stream: WriteStream):
        stream.write(c_bit(self.jetpack_effect is not None))
        if self.jetpack_effect is not None:
            stream.write(c_uint32(self.jetpack_effect))
            stream.write(c_bit(False))

        stream.write(c_bit(True))
        for _ in range(7):
            stream.write(c_uint32(0))

        self._write_data(stream)

    def serialize(self, stream: WriteStream):
        self._write_data(stream)

        stream.write(c_bit(True))

    def destruct(self):
        pass
