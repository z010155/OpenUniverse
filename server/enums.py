from enum import Enum, IntEnum


class ServerType(Enum):
    Auth = 0
    World = 1
    Chat = 2


class ConnectionType(IntEnum):
    General = 0
    Auth = 1
    Client = 4
    Server = 5


class ZoneChecksums:
    VentureExplorer = 0x20b8087c
    ReturnToVentureExplorer = 0x26680a3c
    AvantGardens = 0x49525511
    AvantGardensSurvival = 0x538214e2
    SpiderQueenBattle = 0x0fd403da
    BlockYard = 0x0fd403da
    AvantGrove = 0x0a890303
    NimbusStation = 0xda1e6b30
    PetCove = 0x476e1330
    VertigoLoop = 0x10fc0502
    BattleOfNimbusStation = 0x07d40258
    NimbusRock = 0x058d0191
    NimbusIsle = 0x094f045d
    GnarledForest = 0x12eac290
    CanyonCove = 0x0b7702ef
    KeelhaulCanyon = 0x152e078a
    ChanteyShantey = 0x04b6015c
    ForbiddenValley = 0x8519760d
    ForbiddenValleyDragon = 0x02f50187
    DragonmawChasm = 0x81850f4e
    RavenBluff = 0x03f00126
    Starbase3001 = 0x07c202ee
    DeepFreeze = 0x02320106
    RobotCity = 0x0793037f
    MoonBase = 0x043b01ad
    Portabello = 0x181507dd
    LegoClub = 0x02040138
    CruxPrime = 0x4b17a399
    NexusTower = 0x9e4af43c
    Ninjago = 0x4d692c74
    FrakjawBattle = 0x09eb00ef


ZONE_CHECKSUMS = {
    1000: ZoneChecksums.VentureExplorer,
    1001: ZoneChecksums.ReturnToVentureExplorer,
    1100: ZoneChecksums.AvantGardens,
    1101: ZoneChecksums.AvantGardensSurvival,
    1102: ZoneChecksums.SpiderQueenBattle,
    1150: ZoneChecksums.BlockYard,
    1151: ZoneChecksums.AvantGrove,
    1200: ZoneChecksums.NimbusStation,
    1201: ZoneChecksums.PetCove,
    1203: ZoneChecksums.VertigoLoop,
    1204: ZoneChecksums.BattleOfNimbusStation,
    1250: ZoneChecksums.NimbusRock,
    1251: ZoneChecksums.NimbusIsle,
    1260: None,  # Frostburgh
    1300: ZoneChecksums.GnarledForest,
    1302: ZoneChecksums.CanyonCove,
    1303: ZoneChecksums.KeelhaulCanyon,
    1350: ZoneChecksums.ChanteyShantey,
    1400: ZoneChecksums.ForbiddenValley,
    1402: ZoneChecksums.ForbiddenValleyDragon,
    1403: ZoneChecksums.DragonmawChasm,
    1450: ZoneChecksums.RavenBluff,
    1600: ZoneChecksums.Starbase3001,
    1601: ZoneChecksums.DeepFreeze,
    1602: ZoneChecksums.RobotCity,
    1603: ZoneChecksums.MoonBase,
    1604: ZoneChecksums.Portabello,
    1700: ZoneChecksums.LegoClub,
    1800: ZoneChecksums.CruxPrime,
    1900: ZoneChecksums.NexusTower,
    2000: ZoneChecksums.Ninjago,
    2001: ZoneChecksums.FrakjawBattle
}
