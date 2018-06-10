from abc import ABC


class Module(ABC):
    server: "Server"

    def __init__(self, server: "Server"):
        self.server = server
