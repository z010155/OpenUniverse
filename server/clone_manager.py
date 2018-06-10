from typing import List

from pyraknet.messages import Address
from pyraknet.replicamanager import ReplicaManager
from pyraknet.server import Server as RakServer

from server.database.database import Character


class Clone:
    zone: int
    rm: ReplicaManager
    max_players: int
    players: List[Character]

    def __init__(self, server: RakServer, zone: int):
        self.zone = zone
        self.rm = ReplicaManager(server)
        self.max_players = 32
        self.players = []

    def join(self, char: Character, address: Address, friend_join: bool) -> bool:
        if not friend_join and len(self.players) >= self.max_players:
            return False

        self.players.append(char)
        self.rm.add_participant(address)

        return True


class CloneManager:
    clones: List[Clone]
    _server: RakServer

    def __init__(self, server: RakServer):
        self.clones = []
        self._server = server

    def join_zone(self, char: Character, zone: int, address: Address, friend_join: bool=False) -> Clone:
        for clone in [x for x in self.clones if x.zone == zone]:
            if clone.join(char, address, friend_join):
                return clone

        clone = Clone(self._server, zone)
        self.clones.append(clone)

        if not clone.join(char, address, friend_join):
            raise RuntimeError("Couldn't join a newly created clone")

        return clone

    def get_clone(self, clone: int) -> Clone:
        return self.clones[clone]

    def get_clone_id(self, clone: Clone) -> int:
        return self.clones.index(clone)
