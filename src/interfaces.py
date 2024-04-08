from typing import List, Any, Tuple
import json, os
import logging


class Interfaces:
    def __init__(self, protocol: str = None, interfaces_location: str = 'interfaces.json') -> None:
        """
        Initialize the Interfaces class.

        Args:
            protocol (str, optional): The protocol to use. Defaults to None.
            interfaces_location (str, optional): The location of the interfaces file. Defaults to 'interfaces.json'.
        """
        self.interfaces_location = interfaces_location
        self._protocol = protocol
        self.__interfaces__ = []
        self.load_interfaces()

    def get_interfaces(self) -> List[Any]:
        """
        Get the list of interfaces.

        Returns:
            List[Any]: The list of interfaces.
        """
        return self.__interfaces__

    def add_interface(self, interface: Any) -> Tuple[List[Any], int]:
        """
        Add an interface to the list.

        Args:
            interface (Any): The interface to add.

        Returns:
            Tuple[List[Any], int]: The updated list of interfaces and the status code.
        """
        self.__interfaces__.append(interface)
        self.save_interfaces()
        return self.__interfaces__, 200

    def get_protocol(self) -> str:
        """
        Get the protocol.

        Returns:
            str: The protocol.
        """
        return self._protocol

    def get_interfaces_location(self) -> str:
        """
        Get the interfaces location.

        Returns:
            str: The interfaces location.
        """
        return self.interfaces_location

    def load_interfaces(self) -> None:
        """
        Load the interfaces from the file.
        """
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        try:
            with open("{}/{}".format(BASE_DIR, self.interfaces_location), 'r') as f:
                interfaces = json.load(f)
                for interface in interfaces:
                    self.add_interface(interface)
        except FileNotFoundError:
            # Handle the case when the file is not found
            logging.error("Interfaces file not found.")
        except json.JSONDecodeError:
            # Handle the case when the file is not valid JSON
            logging.error("Invalid JSON format in interfaces file.")
        except Exception as e:
            # Handle any other exceptions
            logging.error(f"An error occurred while loading interfaces: {str(e)}")
        finally:
            f.close()

    def save_interfaces(self) -> None:
        """
        Save the interfaces to the file.
        """
        try:
            with open(self.interfaces_location, 'w') as f:
                json.dump(self.__interfaces__, f)
        except Exception as e:
            # Handle any exceptions
            logging.error(f"An error occurred while saving interfaces: {str(e)}")
        finally:
            f.close()
