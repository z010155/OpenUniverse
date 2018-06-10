import datetime
import secrets
from typing import Dict, Any

import redis
import ujson
from pyraknet.messages import Address


class SessionManager:
    db = redis.StrictRedis()

    @staticmethod
    def create_session(address: Address, user_id: int) -> str:
        addr_str = address[0] + ':' + str(address[1])

        key = secrets.token_urlsafe(24)

        SessionManager.db.set(addr_str, ujson.dumps({
            'address': address[0],
            'port': address[1],
            'user_id': user_id,
            'clone': None,
            'key': key
        }))

        SessionManager.db.expire(addr_str, int(datetime.timedelta(days=1).total_seconds() * 1000))

        return key

    @staticmethod
    def get_session(address: Address) -> Dict[str, Any]:
        return ujson.loads(SessionManager.db.get(address[0] + ':' + str(address[1])))

    @staticmethod
    def update_session(address: Address, user_id: int=None, clone: int=None) -> None:
        session = SessionManager.get_session(address)

        SessionManager.db.set(address[0] + ':' + str(address[1]), ujson.dumps({
            'address': address[0],
            'port': address[1],
            'user_id': user_id or session['user_id'],
            'clone': clone or session['clone'],
            'key': session['key']
        }))
