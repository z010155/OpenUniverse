import os
import sqlite3
from typing import Dict, List, Any

from pyraknet.bitstream import ReadStream, c_uint32, c_float, c_uint8, c_bool, c_uint16, c_uint64, c_int32

ZONE_FILES = {
    1000: os.path.join(os.path.realpath(''), 'assets', 'zones', 'nd_space_ship.luz'),
    1100: os.path.join(os.path.realpath(''), 'assets', 'zones', 'nd_avant_gardens.luz'),
    1200: os.path.join(os.path.realpath(''), 'assets', 'zones', 'nd_nimbus_station.luz')
}


LDF_TYPES = {
    0: str,
    1: int,
    2: int,
    3: float,
    4: float,
    5: int,
    6: int,
    7: bool,
    8: int,
    9: int,
    13: str
}


class Vector3:
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def zero(cls) -> "Vector3":
        return cls(0, 0, 0)


class Quaternion:
    x: float
    y: float
    z: float
    w: float

    def __init__(self, x: float, y: float, z: float, w: float):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    @classmethod
    def zero(cls) -> "Quaternion":
        return cls(0, 0, 0, 0)


class LegoObject:
    object_id: int
    lot: int
    position: Vector3
    rotation: Quaternion
    scale: float
    config: Dict[str, any]

    def __init__(self, object_id: int, lot: int, position: Vector3, rotation: Quaternion, scale: float, config: Dict[str, Any]):
        self.object_id = object_id
        self.lot = lot
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.config = config


class LegoScene:
    scene_id: int
    name: str
    objects: List[LegoObject]

    def __init__(self, scene_id: int, name: str, objects: List[LegoObject]):
        self.scene_id = scene_id
        self.name = name
        self.objects = objects


class LegoZone:
    zone_id: int
    spawnpoint: Vector3
    spawnpoint_rotation: Quaternion
    scenes: List[LegoScene]

    def __init__(self, zone_id: int, spawnpoint: Vector3, spawnpoint_rotation: Quaternion, scenes: List[LegoScene]):
        self.zone_id = zone_id
        self.spawnpoint = spawnpoint
        self.spawnpoint_rotation = spawnpoint_rotation
        self.scenes = scenes


def parse_ldf(ldf: str) -> Dict[str, Any]:
    pts = [x.strip() for x in ldf.strip().splitlines()]

    d = {}

    for pt in pts:
        k, _, tv = pt.partition('=')
        t, _, uv = tv.partition(':')

        if not t or not uv:
            continue

        pt = LDF_TYPES[int(t)]

        d[k] = int(uv) == 1 if pt == bool else pt(uv)

    return d


class ZoneReader:
    conn: sqlite3.Connection = sqlite3.connect(os.path.join(os.path.realpath(''), 'assets', 'CDClient.sqlite'))
    _cache: Dict[int, LegoZone] = {}

    @staticmethod
    def _parse_chunk_2001(stream: ReadStream) -> List[LegoObject]:
        objects = []

        object_count = stream.read(c_uint32)

        for _ in range(object_count):
            object_id = stream.read(c_uint64)
            lot = stream.read(c_int32)

            stream.read(c_uint32)
            stream.read(c_uint32)

            position = Vector3(stream.read(c_float), stream.read(c_float), stream.read(c_float))
            rotation = Quaternion(w=stream.read(c_float), x=stream.read(c_float), y=stream.read(c_float),\
                                  z=stream.read(c_float))
            scale = stream.read(c_float)

            ldf_config = stream.read(str, length_type=c_uint32)
            config = parse_ldf(ldf_config)

            assert stream.read(c_uint32) == 0

            if lot != 176:
                continue

            spawntemplate = config['spawntemplate']

            objects.append(LegoObject(object_id, spawntemplate, position, rotation, scale, config))

        return objects

    @staticmethod
    def _parse_level(stream: ReadStream) -> List[LegoObject]:
        header = stream.read(bytes, length=4)

        stream.read_offset = 0

        objects = []

        if header == b'CHNK':
            while not stream.all_read():
                assert stream.read_offset // 8 % 16 == 0

                start_pos = stream.read_offset // 8

                assert stream.read(bytes, length=4) == b'CHNK'

                chunk_type = stream.read(c_uint32)

                stream.read(c_uint16)
                stream.read(c_uint16)

                chunk_length = stream.read(c_uint32)
                data_pos = stream.read(c_uint32)

                stream.read_offset = data_pos * 8

                assert stream.read_offset // 8 % 16 == 0

                if chunk_type == 2001:
                    objects.extend(ZoneReader._parse_chunk_2001(stream))

                stream.read_offset = (start_pos + chunk_length) * 8

        return objects

    @staticmethod
    def parse_zone(zone: int) -> LegoZone:
        if zone in ZoneReader._cache:
            return ZoneReader._cache[zone]

        with open(ZONE_FILES[zone], 'rb') as f:
            stream = ReadStream(f.read(), unlocked=True)

        version = stream.read(c_uint32)

        assert 0x30 > version > 0x24

        stream.read(c_uint32)

        world_id = stream.read(c_uint32)

        spawnpoint_pos = Vector3(stream.read(c_float), stream.read(c_float), stream.read(c_float))
        spawnpoint_rot = Quaternion(stream.read(c_float), stream.read(c_float), stream.read(c_float),
                                    stream.read(c_float))

        scene_count = stream.read(c_uint32)
        scenes = []

        for _ in range(scene_count):
            filename = stream.read(bytes, length_type=c_uint8).decode('latin1')

            scene_id = stream.read(c_uint64)

            scene_name = stream.read(bytes, length_type=c_uint8).decode('latin1')

            stream.read(bytes, length=3)

            pth = os.path.join(os.path.realpath(''), 'assets', 'levels', filename)

            objects = []

            if os.path.exists(pth):
                with open(pth, 'rb') as f:
                    objects = ZoneReader._parse_level(ReadStream(f.read(), unlocked=True))

            scenes.append(LegoScene(scene_id,scene_name, objects))

        return LegoZone(world_id, spawnpoint_pos, spawnpoint_rot, scenes)
