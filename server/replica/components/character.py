from typing import Optional

from pyraknet.bitstream import WriteStream, c_bit, c_int64, c_uint8, c_uint32, c_int32, c_uint64, c_uint16

from server.replica.component import Component


class CharacterComponent(Component):
    vehicle_id: Optional[int]
    level: Optional[int]
    hair_color: int
    hair_style: int
    shirt_color: int
    pants_color: int
    shirt_style: int
    eyebrow_style: int
    eye_style: int
    mouth_style: int
    account_id: int
    llog: int
    lego_score: int
    free_to_play: bool
    currency_collected: int
    bricks_collected: int
    smashables_smashed: int
    quickbuilds_completed: int
    enemies_smashed: int
    rockets_used: int
    missions_completed: int
    pets_tamed: int
    imagination_powerups_collected: int
    life_powerups_collected: int
    armor_powerups_collected: int
    distance_traveled: int
    times_smashed: int
    damage_taken: int
    damage_healed: int
    armor_repaired: int
    imagination_restored: int
    imagination_used: int
    distance_driven: int
    time_airborne_racecar: int
    racing_imagination_powerups_collected: int
    racing_imagination_crates_smashed: int
    racecar_boosts_activated: int
    racecar_wrecks: int
    racing_smashables_smashed: int
    races_finished: int
    first_place_finishes: int
    landing_rocket: bool
    rocket_modules: str
    pvp: bool
    gm: bool
    gm_level: int
    glowing_head: bool
    guild: bool
    guild_id: int
    guild_name: str

    def __init__(self, **kwargs):
        self.vehicle_id = kwargs.get('vehicle_id')
        self.level = kwargs.get('level')
        self.hair_color = kwargs['hair_color']
        self.hair_style = kwargs['hair_style']
        self.shirt_color = kwargs['shirt_color']
        self.pants_color = kwargs['pants_color']
        self.shirt_style = kwargs['shirt_style']
        self.eyebrow_style = kwargs['eyebrow_style']
        self.eye_style = kwargs['eye_style']
        self.mouth_style = kwargs['mouth_style']
        self.account_id = kwargs['account_id']
        self.llog = kwargs.get('llog', 0)
        self.lego_score = kwargs.get('lego_score', 0)
        self.free_to_play = kwargs.get('free_to_play', False)
        self.currency_collected = kwargs.get('currency_collected', 0)
        self.bricks_collected = kwargs.get('bricks_collected', 0)
        self.smashables_smashed = kwargs.get('smashables_smashed', 0)
        self.quickbuilds_completed = kwargs.get('quickbuilds_completed', 0)
        self.enemies_smashed = kwargs.get('enemies_smashed', 0)
        self.rockets_used = kwargs.get('rockets_used', 0)
        self.missions_completed = kwargs.get('missions_completed', 0)
        self.pets_tamed = kwargs.get('pets_tamed', 0)
        self.imagination_powerups_collected = kwargs.get('imagination_powerups_collected', 0)
        self.life_powerups_collected = kwargs.get('life_powerups_collected', 0)
        self.armor_powerups_collected = kwargs.get('armor_powerups_collected', 0)
        self.distance_traveled = kwargs.get('distance_traveled', 0)
        self.times_smashed = kwargs.get('times_smashed', 0)
        self.damage_taken = kwargs.get('damage_taken', 0)
        self.damage_healed = kwargs.get('damage_healed', 0)
        self.armor_repaired = kwargs.get('armor_repaired', 0)
        self.imagination_restored = kwargs.get('imagination_restored', 0)
        self.imagination_used = kwargs.get('imagination_used', 0)
        self.distance_driven = kwargs.get('distance_driven', 0)
        self.time_airborne_racecar = kwargs.get('time_airborne_racecar', 0)
        self.racing_imagination_powerups_collected = kwargs.get('racing_imagination_powerups_collected', 0)
        self.racing_imagination_crates_smashed = kwargs.get('racing_imagination_crates_smashed', 0)
        self.racecar_boosts_activated = kwargs.get('racecar_boosts_activated', 0)
        self.racecar_wrecks = kwargs.get('racecar_wrecks', 0)
        self.racing_smashables_smashed = kwargs.get('racing_smashables_smashed', 0)
        self.races_finished = kwargs.get('races_finished', 0)
        self.first_place_finishes = kwargs.get('first_place_finishes', 0)
        self.landing_rocket = kwargs.get('landing_rocket', False)
        self.rocket_modules = kwargs.get('rocket_modules', '')
        self.pvp = kwargs.get('pvp', False)
        self.gm = kwargs.get('gm', False)
        self.gm_level = kwargs.get('gm_level', 0)
        self.glowing_head = kwargs.get('glowing_head', False)
        self.guild = kwargs.get('guild', True)
        self.guild_id = kwargs.get('guild_id', 0)
        self.guild_name = kwargs.get('guild_name', '')

    def _write_part1(self, stream: WriteStream):
        stream.write(c_bit(True))
        stream.write(c_bit(self.vehicle_id is not None))
        if self.vehicle_id is not None:
            stream.write(c_int64(self.vehicle_id))
        stream.write(c_uint8(0))

        stream.write(c_bit(self.level is not None))
        if self.level is not None:
            stream.write(c_uint32(self.level))

        stream.write(c_bit(True))
        stream.write(c_bit(False))
        stream.write(c_bit(True))

    def _write_part2(self, stream: WriteStream):
        stream.write(c_bit(True))
        stream.write(c_bit(self.pvp))
        stream.write(c_bit(self.gm))
        stream.write(c_uint8(self.gm_level))
        stream.write(c_bit(False))
        stream.write(c_uint8(0))

        stream.write(c_bit(True))
        stream.write(c_uint32(1 if self.glowing_head else 0))

        stream.write(c_bit(self.guild))
        if self.guild:
            stream.write(c_int64(self.guild_id))
            stream.write(self.guild_name, allocated_length=33)
            stream.write(c_bit(True))
            stream.write(c_int32(-1))

    def construct(self, stream: WriteStream):
        self._write_part1(stream)

        stream.write(c_bit(False))
        stream.write(c_bit(False))
        stream.write(c_bit(False))
        stream.write(c_bit(False))

        stream.write(c_uint32(self.hair_color))
        stream.write(c_uint32(self.hair_style))
        stream.write(c_uint32(0))
        stream.write(c_uint32(self.shirt_color))
        stream.write(c_uint32(self.pants_color))
        stream.write(c_uint32(self.shirt_style))
        stream.write(c_uint32(0))
        stream.write(c_uint32(self.eyebrow_style))
        stream.write(c_uint32(self.eye_style))
        stream.write(c_uint32(self.mouth_style))

        stream.write(c_uint64(self.account_id))
        stream.write(c_uint64(self.llog))
        stream.write(c_uint64(0))
        stream.write(c_uint64(self.lego_score))

        stream.write(c_bit(self.free_to_play))

        stream.write(c_uint64(self.currency_collected))
        stream.write(c_uint64(self.bricks_collected))
        stream.write(c_uint64(self.smashables_smashed))
        stream.write(c_uint64(self.quickbuilds_completed))
        stream.write(c_uint64(self.enemies_smashed))
        stream.write(c_uint64(self.rockets_used))
        stream.write(c_uint64(self.missions_completed))
        stream.write(c_uint64(self.pets_tamed))
        stream.write(c_uint64(self.imagination_powerups_collected))
        stream.write(c_uint64(self.life_powerups_collected))
        stream.write(c_uint64(self.armor_powerups_collected))
        stream.write(c_uint64(self.distance_traveled))
        stream.write(c_uint64(self.times_smashed))
        stream.write(c_uint64(self.damage_taken))
        stream.write(c_uint64(self.damage_healed))
        stream.write(c_uint64(self.armor_repaired))
        stream.write(c_uint64(self.imagination_restored))
        stream.write(c_uint64(self.imagination_used))
        stream.write(c_uint64(self.distance_driven))
        stream.write(c_uint64(self.time_airborne_racecar))
        stream.write(c_uint64(self.racing_imagination_powerups_collected))
        stream.write(c_uint64(self.racing_imagination_crates_smashed))
        stream.write(c_uint64(self.racecar_boosts_activated))
        stream.write(c_uint64(self.racecar_wrecks))
        stream.write(c_uint64(self.racing_smashables_smashed))
        stream.write(c_uint64(self.races_finished))
        stream.write(c_uint64(self.first_place_finishes))

        stream.write(c_bit(False))

        stream.write(c_bit(self.landing_rocket))
        if self.landing_rocket:
            stream.write(self.rocket_modules, length_type=c_uint16)

        self._write_part2(stream)

    def serialize(self, stream: WriteStream):
        self._write_part1(stream)
        self._write_part2(stream)

    def destruct(self):
        pass
