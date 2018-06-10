from pyraknet.messages import Address

from server.database.session_manager import SessionManager
from server.module import Module
from server.packets.world.session_info import SessionInfoPacket


class SessionModule(Module):
    def session_info(self, packet: SessionInfoPacket, address: Address):
        session = SessionManager.get_session(address)

        if session['key'] != packet.user_key:
            self.server.close_connection(address)
