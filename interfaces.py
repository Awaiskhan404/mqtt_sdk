from typing import List, Any, Tuple
import json, os


class Interfaces:
    def __init__(self, protocol=None, interfaces_location='interfaces.json') -> None:
        self.interfaces_location = interfaces_location
        self._protocol = protocol
        self.__interfaces__ = []
        self.load_interfaces()

    def get_interfaces(self):
        return self.__interfaces__

    def add_interface(self, interface) -> tuple[list[Any], int]:
        self.__interfaces__.append(interface)
        self.save_interfaces()
        return self.__interfaces__, 200

    def get_protocol(self):
        return self._protocol

    def get_interfaces_location(self):
        return self.interfaces_location

    def load_interfaces(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        with open("{}/{}".format(BASE_DIR, self.interfaces_location), 'r') as f:
            interfaces = json.load(f)
            for interface in interfaces:
                self.add_interface(interface)
            f.close()

    def save_interfaces(self):
        with open(self.interfaces_location, 'w') as f:
            json.dump(self.__interfaces__, f)
            f.close()
