import asyncio

import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from server.enums import ServerType
from server.server import Server

if __name__ == '__main__':
    with open('config.yml', 'r') as f:
        config = yaml.load(f, Loader=Loader)

    Server(ServerType.Auth, config)
    Server(ServerType.World, config)

    loop = asyncio.get_event_loop()
    loop.run_forever()
    loop.close()
