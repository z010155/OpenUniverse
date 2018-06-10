from xml.etree import ElementTree

from peewee import DoesNotExist
from pyraknet.messages import Address

from server.asset_loader import AssetLoader
from server.clone_manager import CloneManager
from server.database.database import Database, Character
from server.database.session_manager import SessionManager
from server.enums import ZONE_CHECKSUMS
from server.legodata import LegoData
from server.module import Module
from server.packets.world.character.character_create import CharacterCreateRequestPacket, CharacterCreateResponsePacket
from server.packets.world.character.character_delete import CharacterDeleteRequestPacket, CharacterDeleteResponsePacket
from server.packets.world.character.character_list import CharacterListPacket
from server.packets.world.detailed_info import DetailedUserInfoPacket
from server.packets.world.game_message import ServerGameMessage
from server.packets.world.load_complete import ClientsideLoadCompletePacket
from server.packets.world.world_info import WorldInfoPacket
from server.packets.world.world_join import WorldJoinRequestPacket
from server.replica.base_data import BaseData
from server.replica.components.character import CharacterComponent
from server.replica.components.component107 import Component107
from server.replica.components.controllable_physics import ControllablePhysicsComponent
from server.replica.components.destructible import DestructibleComponent
from server.replica.components.inventory import InventoryComponent
from server.replica.components.render import RenderComponent
from server.replica.components.script import ScriptComponent
from server.replica.components.skill import SkillComponent
from server.replica.components.stats import StatsComponent
from server.zone_reader import ZoneReader


class CharacterModule(Module):
    def character_list(self, packet: CharacterListPacket, address: Address):
        session = SessionManager.get_session(address)
        user = Database.get_user(session['user_id'])

        self.server.send(CharacterListPacket(user.front_character, user.characters), address)

    def character_create(self, packet: CharacterCreateRequestPacket, address: Address):
        session = SessionManager.get_session(address)
        user = Database.get_user(session['user_id'])

        names = AssetLoader.load_names()
        name = names[0][packet.predef1].strip() + names[1][packet.predef2].strip() + names[2][packet.predef3].strip()

        # TODO: generate starter kit

        char = Character(user=user, name=name, unapproved_name=packet.name, shirt_color=packet.shirt_color,
                         shirt_style=packet.shirt_style, pants_color=packet.pants_color, hair_style=packet.hair_style,
                         hair_color=packet.hair_color, lh=packet.lh, rh=packet.rh, eyebrow_style=packet.eyebrow_style,
                         eye_style=packet.eye_style, mouth_style=packet.mouth_style)
        char.save()

        self.server.send(CharacterCreateResponsePacket(0x00), address)
        self.character_list(CharacterListPacket(), address)

    def character_delete(self, packet: CharacterDeleteRequestPacket, address: Address):
        Character.delete_by_id(packet.character_id)

        self.server.send(CharacterDeleteResponsePacket(), address)

    def join_world(self, packet: WorldJoinRequestPacket, address: Address):
        try:
            char: Character = Character.get_by_id(packet.character_id)
            cm: CloneManager = self.server.clone_manager

            clone = cm.join_zone(char, char.last_zone, address, False)
            clone_id = cm.get_clone_id(clone)

            SessionManager.update_session(address, clone=clone_id)

            zone_id = 1000 if char.last_zone == 0 else char.last_zone
            zone = ZoneReader.parse_zone(zone_id)

            res = WorldInfoPacket(zone_id, 0, clone_id, ZONE_CHECKSUMS[zone_id], zone.spawnpoint, False)

            self.server.send(res, address)
        except DoesNotExist:
            raise RuntimeError("Character wasn't found but tried to join a world")

    def load_complete(self, packet: ClientsideLoadCompletePacket, address: Address):
        cm: CloneManager = self.server.clone_manager
        clone = cm.get_clone(packet.clone)
        session = SessionManager.get_session(address)
        char = [x for x in clone.players if x.user.user_id == session['user_id']][0]
        zone = ZoneReader.parse_zone(packet.zone_id)

        ldf = LegoData()

        ldf.set('chatmode', 1, 0)
        ldf.set('editor_enabled', 7, False)
        ldf.set('editor_level', 1, 0)
        ldf.set('gmlevel', 1, 0)
        ldf.set('levelid', 8, packet.zone_id)
        ldf.set('name', 0, char.name)
        ldf.set('objid', 9, char.character_id)
        ldf.set('reputation', 8, 0)
        ldf.set('template', 1, 1)
        ldf.set('accountID', 8, char.user.user_id)

        xml = ElementTree.TreeBuilder()

        xml.start('obj', {'v': '1'})

        xml.start('buff', {})
        xml.end('buff')

        xml.start('skill', {})
        xml.end('skill')

        xml.start('inv', {})
        xml.start('bag', {})
        xml.start('b', {
            't': '0',
            'm': '5'  # TODO: set using var from db
        })
        xml.end('b')
        xml.end('bag')

        xml.start('items', {})
        xml.start('in', {})

        # TODO: items here

        xml.end('in')
        xml.end('items')
        xml.end('inv')

        xml.start('mf', {})
        xml.end('mf')

        xml.start('char', {
            'cc': '0'  # TODO: set using var from db
        })
        xml.end('char')

        xml.start('lvl', {
            'l': '1'  # TODO: set using var from db
        })
        xml.end('lvl')

        xml.start('flag', {})
        xml.end('flag')

        xml.start('pet', {})
        xml.end('pet')

        xml.start('mis', {})
        xml.start('cur', {})

        # TODO: in progress missions here

        xml.end('cur')
        xml.start('done', {})

        # TODO: completed missions here

        xml.end('done')
        xml.end('mis')

        xml.start('mnt', {})
        xml.end('mnt')

        xml.start('dest', {})
        xml.end('dest')

        xml.end('obj')

        ldf.set('xmlData', 13, xml.close())

        res = DetailedUserInfoPacket(ldf)

        self.server.send(res, address)

        components = [
            ControllablePhysicsComponent(player=True, position=zone.spawnpoint, rotation=zone.spawnpoint_rotation),
            DestructibleComponent(),
            StatsComponent(),
            CharacterComponent(shirt_color=char.shirt_color, shirt_style=char.shirt_style, hair_style=char.hair_style,
                               hair_color=char.hair_color, pants_color=char.pants_color,
                               eyebrow_style=char.eyebrow_style, eye_style=char.eye_style, mouth_style=char.mouth_style,
                               account_id=char.user.user_id),
            InventoryComponent(items=[]),
            ScriptComponent(),
            SkillComponent(),
            RenderComponent(),
            Component107(),
        ]

        player = BaseData(char.character_id, 1, char.name, 0, components)

        clone.rm.construct(player, True)

        self.server.send(ServerGameMessage(char.character_id, 0x066a, b''), address)
        self.server.send(ServerGameMessage(char.character_id, 0x01fd, b''), address)
