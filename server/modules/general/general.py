from pyraknet.messages import Address

from server.module import Module
from server.enums import ServerType
from server.packets.general.handshake import HandshakePacket


class GeneralModule(Module):
    def handle_packet(self, packet: HandshakePacket, address: Address):
        res = HandshakePacket(auth=self.server.server_type == ServerType.Auth)

        self.server.send(res, address)
