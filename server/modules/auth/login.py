from pyraknet.messages import Address

from server.database.database import Database, InvalidPasswordException
from server.database.session_manager import SessionManager
from server.module import Module
from server.packets.auth.login_info import LoginInfoPacket


class LoginModule(Module):
    def login_info(self, packet: LoginInfoPacket, address: Address):
        login_code = 0x01
        user = None
        key = ''

        try:
            user = Database.authenticate(packet.username, packet.password)

            if not user:
                user = Database.create_user(packet.username, packet.password)

            key = SessionManager.create_session(address, user.user_id)
        except InvalidPasswordException:
            login_code = 0x06

        res = LoginInfoPacket(login_code=login_code, user_key=key, char_ip=self.server.config['world']['ip'],
                              char_port=self.server.config['world']['port'], chat_ip=self.server.config['chat']['ip'],
                              chat_port=self.server.config['chat']['port'], ip='127.0.0.1', locale='US',
                              first_login_sub=user.first_login_sub if user else False,
                              free_to_play=user.free_to_play if user else False, error=None)

        self.server.send(res, address)
