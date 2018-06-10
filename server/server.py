"""Server related stuff"""
import importlib
import inspect
import logging
import pkgutil
from typing import Union, SupportsBytes, overload, Dict, Callable, Tuple, Type, Any

from pyraknet.bitstream import WriteStream, ReadStream
from pyraknet.messages import Address
from pyraknet.server import Server as RakServer, Event

from server.clone_manager import CloneManager
from server.enums import ServerType
from server.module import Module
from server.packet import Packet, PacketHeader

SERVER_MODULES = {
    ServerType.Auth: ['server.modules.auth'],
    ServerType.World: ['server.modules.world'],
    ServerType.Chat: ['server.modules.chat']
}

logging.basicConfig(level=logging.DEBUG)


class Server:
    """LEGO Universe server"""

    server_type: ServerType
    config: Dict[str, Union[int, str]]
    log: logging.Logger
    clone_manager: CloneManager
    _address: Address
    _server: RakServer
    _handlers: Dict[int, Dict[int, Tuple[Type[Packet], Callable[..., None]]]]

    def __init__(self, server_type: ServerType, config: Dict[str, Any]):
        self.server_type = server_type
        self.config = config
        self.log = logging.getLogger(f'OpenLU ({server_type.name})')
        self._address = ('127.0.0.1', config[server_type.name.lower()]['port'])
        self._server = RakServer(self._address, 8, b'3.25 ND1')
        self._server.add_handler(Event.UserPacket, self._on_packet)
        self._handlers = {}

        self.load_modules('server.modules.general')

        for m in SERVER_MODULES[server_type]:
            self.load_modules(m)

        if server_type == ServerType.World:
            self.clone_manager = CloneManager(self._server)

        self.log.info(f'Server started on {self._address[0]}:{self._address[1]}')

    def load_modules(self, path: str):
        package = importlib.import_module(path)

        for _, name, pkg in pkgutil.walk_packages(package.__path__):
            full_name = package.__name__ + '.' + name
            module = importlib.import_module(full_name)

            if pkg:
                self.load_modules(full_name)
            else:
                for _, Mod in inspect.getmembers(module, lambda x: inspect.isclass(x) and issubclass(x, Module)
                                                 and x is not Module):
                    m: Module = Mod(self)

                    for _, mem in inspect.getmembers(m, lambda x: inspect.ismethod(x)):
                        if 'packet' not in mem.__annotations__:
                            continue

                        pkt: Type[Packet] = mem.__annotations__['packet']

                        if not issubclass(pkt, Packet):
                            continue

                        self.log.info(f'Loaded handler for packet {pkt.__name__}')

                        self._handlers.setdefault(pkt.connection_type, {})[pkt.packet_id] = (pkt, mem)

    def _on_packet(self, data: bytes, address: Address):
        stream = ReadStream(data)
        header = stream.read(PacketHeader)

        if header.connection_type in self._handlers and header.packet_id in self._handlers[header.connection_type]:
            tup = self._handlers[header.connection_type][header.packet_id]
            pkt = tup[0]

            self.log.info(f'Received packet {pkt.__name__}')

            tup[1](stream.read(pkt), address)
        else:
            self.log.warning(f'Unhandled packet ({header.connection_type}, {header.packet_id})')

    def send(self, packet: Packet, address: Address):
        stream = WriteStream()
        stream.write(packet)

        self._server.send(bytes(stream), address)

        self.log.info(f'Sent packet {packet.__class__.__name__}')

    def send_bytes(self, data: Union[bytes, SupportsBytes], address: Address):
        self._server.send(data, address)

    def close_connection(self, address: Address):
        self._server.close_connection(address)
